import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

# Configuration
RSS_FEED_URL = "https://hnrss.org/newest?points=50" # Hacker News stories with >50 points
DATA_FILE = "data.json"

def fetch_data():
    """Fetches the latest items from the RSS feed."""
    print(f"📡 Fetching data from {RSS_FEED_URL}...")
    try:
        response = requests.get(RSS_FEED_URL, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return None

def clean_data(xml_content):
    """Parses the XML and cleans the data."""
    print("🧹 Cleaning data...")
    soup = BeautifulSoup(xml_content, "xml")
    items = soup.find_all("item")
    
    cleaned_items = []
    for item in items:
        # 1. Standardize Title
        title = item.title.text if item.title else "Untitled"
        
        # 2. Clean Link
        link = item.link.text if item.link else "#"
        
        # 3. Clean and Standardize Date
        raw_date = item.pubDate.text if item.pubDate else ""
        try:
            # RSS dates are often: 'Fri, 09 May 2026 13:45:00 +0000'
            date_obj = datetime.strptime(raw_date, "%a, %d %b %Y %H:%M:%S %z")
            iso_date = date_obj.isoformat()
        except:
            iso_date = datetime.now().isoformat()
            
        # 4. Extract Category (using a simple keyword filter)
        category = "General"
        if "AI" in title.upper() or "GPT" in title.upper():
            category = "Artificial Intelligence"
        elif "WEB" in title.upper() or "CSS" in title.upper():
            category = "Web Development"
        
        cleaned_items.append({
            "title": title,
            "link": link,
            "date": iso_date,
            "category": category,
            "source": "Hacker News"
        })
        
    return cleaned_items[:10] # Keep only top 10 for the dashboard

def save_data(data):
    """Saves the cleaned data to a JSON file."""
    print(f"💾 Saving {len(data)} items to {DATA_FILE}...")
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "last_updated": datetime.now().isoformat(),
            "items": data
        }, f, indent=4)

def main():
    xml_content = fetch_data()
    if xml_content:
        cleaned_data = clean_data(xml_content)
        save_data(cleaned_data)
        print("✅ Agent task complete!")

if __name__ == "__main__":
    main()
