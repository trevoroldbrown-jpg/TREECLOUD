import requests
import json
from datetime import datetime
import os
import argparse
from dotenv import load_dotenv

try:
    import opik
    opik_enabled = True
except ImportError:
    opik_enabled = False

load_dotenv()

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

def track_if_enabled(func):
    if opik_enabled:
        return opik.track()(func)
    return func

@track_if_enabled
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

@track_if_enabled
def deep_index_repo(repo_full_name, pi_client, repos_dir):
    """Downloads README and indexes it with PageIndex."""
    print(f"🧠 Deep Indexing {repo_full_name}...")
    # Try main then master
    urls = [
        f"https://raw.githubusercontent.com/{repo_full_name}/main/README.md",
        f"https://raw.githubusercontent.com/{repo_full_name}/master/README.md"
    ]
    
    readme_content = None
    for url in urls:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            readme_content = resp.text
            break
            
    if not readme_content:
        print(f"  ⚠️ Could not fetch README for {repo_full_name}")
        return None
        
    safe_name = repo_full_name.replace("/", "_") + "_readme.md"
    filepath = os.path.join(repos_dir, safe_name)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(readme_content)
        
    try:
        doc_id = pi_client.index(filepath)
        print(f"  ✅ Indexed successfully. Doc ID: {doc_id}")
        return doc_id
    except Exception as e:
        print(f"  ❌ Indexing failed: {e}")
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deep-index", action="store_true", help="Run PageIndex on fetched repos")
    args = parser.parse_args()

    pi_client = None
    repos_dir = None
    if args.deep_index:
        try:
            from pageindex import PageIndexClient
            api_key = os.environ.get("DEEPSEEK_API_KEY")
            if api_key == "your_deepseek_api_key_here":
                api_key = None
            
            workspace_dir = os.path.join("data", "pageindex")
            repos_dir = os.path.join(workspace_dir, "repos")
            os.makedirs(repos_dir, exist_ok=True)
            
            try:
                pi_client = PageIndexClient(api_key=api_key)
            except TypeError:
                pi_client = PageIndexClient()
        except ImportError:
            print("⚠️ PageIndex module not installed. Run `pip install pageindex` first.")
            return
        except Exception as e:
            print(f"⚠️ PageIndex initialization failed: {e}")
            return

    interests = get_interests()
    all_data = []
    
    for interest in interests:
        repos = fetch_repos_for_interest(interest)
        all_data.extend(repos)
        
    if all_data:
        # Perform deep indexing if requested
        if args.deep_index and pi_client:
            for item in all_data:
                doc_id = deep_index_repo(item['title'], pi_client, repos_dir)
                if doc_id:
                    item['pageindex_doc_id'] = doc_id

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
