import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
import re

# Configuration
TRENDING_URL = "https://github.com/trending/python?since=weekly"
DATA_FILE = "data.json"

def fetch_data():
    """Fetches the HTML from GitHub Trending."""
    print(f"📡 Fetching data from {TRENDING_URL}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(TRENDING_URL, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return None

def clean_data(html_content):
    """Parses the HTML and extracts repository insights."""
    print("🧹 Extracting repositories...")
    soup = BeautifulSoup(html_content, "html.parser")
    articles = soup.find_all("article", class_="Box-row")
    
    cleaned_items = []
    for article in articles:
        # 1. Title and Link
        h2 = article.find("h2", class_="h3")
        if not h2 or not h2.a:
            continue
        
        rel_link = h2.a.get("href", "")
        link = f"https://github.com{rel_link}"
        # The text inside h2.a is usually "username / repo_name", separated by newlines/spaces
        raw_title = h2.a.text.strip()
        # Clean up whitespace/newlines: "username \n / \n repo" -> "username / repo"
        title = re.sub(r'\s+', ' ', raw_title)
        
        # 2. Description ("What got built")
        desc_p = article.find("p", class_="col-9")
        description = desc_p.text.strip() if desc_p else "No description provided."
        
        # 3. Stars ("How popular is it")
        # Stars are usually in a Link--muted class
        links_muted = article.find_all("a", class_="Link--muted")
        stars = "0"
        for lm in links_muted:
            text = lm.text.strip()
            # If the text has numbers and maybe a comma, it's likely stars or forks. The first one is usually stars.
            # But let's look for the SVG icon if we can't be sure, or just grab the first one that looks like a number
            if re.match(r'^[\d,]+$', text):
                stars = text
                break
                
        # 4. Determine "Why it's interesting" based on keywords
        desc_lower = description.lower()
        interest_points = []
        if any(kw in desc_lower for kw in ["agent", "autonomous", "auto"]):
            interest_points.append("Agentic Architecture")
        if any(kw in desc_lower for kw in ["llm", "language model", "gpt", "claude"]):
            interest_points.append("LLM Integration")
        if any(kw in desc_lower for kw in ["scraper", "crawl", "data"]):
            interest_points.append("Data Processing")
        if any(kw in desc_lower for kw in ["framework", "tool", "library"]):
            interest_points.append("Developer Tooling")
            
        why_interesting = ", ".join(interest_points) if interest_points else "Trending Community Choice"

        cleaned_items.append({
            "title": title,
            "link": link,
            "description": description,
            "stars": stars,
            "why_interesting": why_interesting,
            "source": "GitHub Trending (Python)"
        })
        
    return cleaned_items[:12] # Keep top 12 for a nice grid

def save_data(data):
    """Saves the cleaned data to a JSON file."""
    print(f"💾 Saving {len(data)} items to {DATA_FILE}...")
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "last_updated": datetime.now().isoformat(),
            "items": data
        }, f, indent=4)

def main():
    html_content = fetch_data()
    if html_content:
        cleaned_data = clean_data(html_content)
        if cleaned_data:
            save_data(cleaned_data)
            print("✅ Agent task complete!")
        else:
            print("⚠️ No items extracted. The page layout might have changed.")

if __name__ == "__main__":
    main()
