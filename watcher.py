import requests
import json
from datetime import datetime
import os

# Configuration
DATA_FILE = "data.json"
INTERESTS_FILE = "interests.json"

def get_interests():
    """Reads the user's interests from the config file."""
    try:
        with open(INTERESTS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ interests.json not found. Using default interests.")
        return ["AI Agents"]
    except Exception as e:
        print(f"❌ Error reading interests: {e}")
        return ["Python Automation"]

def fetch_repos_for_interest(interest):
    """Fetches top 3 repositories for a specific interest using GitHub API."""
    print(f"📡 Searching GitHub for: '{interest}'...")
    url = f"https://api.github.com/search/repositories?q={requests.utils.quote(interest)}&sort=stars&order=desc"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Project-Treecloud-Agent"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        cleaned_items = []
        for item in data.get("items", [])[:3]: # Get top 3 per interest
            cleaned_items.append({
                "title": item.get("full_name"),
                "link": item.get("html_url"),
                "description": item.get("description") or "No description provided.",
                "stars": str(item.get("stargazers_count")),
                "why_interesting": f"Top matched for '{interest}'",
                "source": "GitHub Search API"
            })
        return cleaned_items
        
    except Exception as e:
        print(f"❌ Error fetching data for {interest}: {e}")
        return []

def main():
    interests = get_interests()
    all_data = []
    
    for interest in interests:
        repos = fetch_repos_for_interest(interest)
        all_data.extend(repos)
        
    if all_data:
        print(f"💾 Saving {len(all_data)} curated items to {DATA_FILE}...")
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "last_updated": datetime.now().isoformat(),
                "items": all_data
            }, f, indent=4)
        print("✅ Agent task complete!")
    else:
        print("⚠️ No items extracted.")

if __name__ == "__main__":
    main()
