import os
import json
import requests
from datetime import datetime, timedelta

# Configuration
DATA_FILE = "data.json"
INTERESTS_FILE = "interests.json"

def check_file_exists(filepath):
    if os.path.exists(filepath):
        print(f"[OK] {filepath} exists.")
        return True
    else:
        print(f"[MISSING] {filepath} is MISSING!")
        return False

def validate_data_json():
    if not check_file_exists(DATA_FILE):
        return
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Check staleness
        last_updated_str = data.get("last_updated")
        if last_updated_str:
            last_updated = datetime.fromisoformat(last_updated_str)
            if datetime.now() - last_updated > timedelta(hours=24):
                print(f"[WARNING] Data is STALE (Last updated: {last_updated_str})")
            else:
                print(f"[OK] Data is fresh (Last updated: {last_updated_str})")
        
        # Check items
        items = data.get("items", [])
        if not items:
            print("[ERROR] 'items' array is EMPTY in data.json!")
        else:
            print(f"[OK] Found {len(items)} items in data.json.")
            # Validate first item structure
            required_keys = ["title", "link", "description", "stars"]
            first_item = items[0]
            missing = [k for k in required_keys if k not in first_item]
            if missing:
                print(f"[ERROR] Data schema error! Missing keys: {missing}")
            else:
                print("[OK] Data schema looks valid.")

    except Exception as e:
        print(f"[ERROR] Error validating data.json: {e}")

def test_github_api():
    print("[INFO] Testing GitHub API connectivity...")
    try:
        # Simple search for 'python' to check if API is reachable
        url = "https://api.github.com/search/repositories?q=python&per_page=1"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("[OK] GitHub API is reachable.")
        elif response.status_code == 403:
            print("[WARNING] GitHub API Rate Limited.")
        else:
            print(f"[ERROR] GitHub API returned status: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Network error testing GitHub API: {e}")

def run_diagnostics():
    print("=== Treecloud Debugging Agent Diagnostics ===")
    check_file_exists(INTERESTS_FILE)
    validate_data_json()
    test_github_api()
    print("=============================================")

if __name__ == "__main__":
    run_diagnostics()
