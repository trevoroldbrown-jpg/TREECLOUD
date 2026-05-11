import json
import os
from datetime import datetime

# Configuration
DATA_FILE = "data.json"
PROPOSALS_DIR = "proposals"

def ensure_dirs():
    if not os.path.exists(PROPOSALS_DIR):
        os.makedirs(PROPOSALS_DIR)

def load_data():
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_proposal(item):
    """
    Simulates an LLM brainstorming session based on a repo.
    In a live environment, this would hit an LLM API.
    """
    repo_title = item['title']
    description = item['description']
    
    # Brainstorming logic (Heuristic-based for now)
    potential_feature = f"Integration with {repo_title}"
    if "agent" in description.lower() or "agent" in repo_title.lower():
        potential_feature = f"Multi-Agent Subsystem: {repo_title.split('/')[-1]}"
    elif "rag" in description.lower() or "index" in description.lower():
        potential_feature = f"Advanced Knowledge Retrieval using {repo_title.split('/')[-1]}"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = repo_title.replace("/", "_").lower()
    filename = f"proposal_{safe_name}_{timestamp}.md"
    filepath = os.path.join(PROPOSALS_DIR, filename)
    
    content = f"""# Proposal: {potential_feature}

## Source Inspiration
- **Repository:** {repo_title}
- **Link:** {item['link']}
- **Description:** {description}

## Why this is valuable
Based on my autonomous analysis of your curated feed, this repository aligns with your interest in "{item.get('why_interesting', 'General AI')}". 

## Proposed Implementation Pathway
1. **Research Phase:** Analyze the {repo_title} architecture for compatibility with our existing `watcher.py`.
2. **Skill Creation:** Generate a new `.claude/skills` file specifically for this tool.
3. **Prototype:** Build a standalone script `research_{safe_name}.py` to test core functionality.

## Action Required
Reply with "Approve {repo_title}" to initiate the research phase for this feature.
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    return filepath

def main():
    print("[INFO] Treecloud Auto-Evolver: Scanning for evolution opportunities...")
    ensure_dirs()
    data = load_data()
    
    if not data:
        print("[ERROR] No data.json found. Run watcher.py first.")
        return
        
    items = data.get("items", [])
    # Filter for items that look like they have high potential (e.g. "Agentic Architecture")
    evolution_targets = [i for i in items if "Agentic" in i.get("why_interesting", "")]
    
    if not evolution_targets:
        # Fallback to top starred
        evolution_targets = items[:2]
        
    for target in evolution_targets[:2]: # Only generate 2 proposals at a time to avoid spam
        print(f"[IDEA] Brainstorming proposal for: {target['title']}")
        path = generate_proposal(target)
        print(f"[OK] Proposal generated: {path}")

if __name__ == "__main__":
    main()
