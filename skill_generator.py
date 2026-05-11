import json
import os
import requests

APPROVALS_FILE = 'approvals.json'
SKILLS_DIR = '.claude/skills'

def ensure_skills_dir():
    if not os.path.exists(SKILLS_DIR):
        os.makedirs(SKILLS_DIR)

def generate_skill_file(repo_data):
    # Create a clean filename from the repo title
    safe_title = repo_data['title'].replace('/', '-').replace('\\', '-').lower()
    filename = f"{safe_title}.md"
    filepath = os.path.join(SKILLS_DIR, filename)
    
    # We could theoretically hit the GitHub API for the README here,
    # but to avoid rate limits during testing, we'll draft a solid template
    # based on the Context Engineering framework.
    
    content = f"""---
name: {safe_title}-integration
description: This skill should be used when the user asks to implement, discuss, or integrate {repo_data['title']} into Project Treecloud.
---

# {repo_data['title']} Integration Skill

You (the AI Agent) are currently analyzing an integration request for **{repo_data['title']}**.
The user "Sparked" this idea from their Treecloud Hub because they found it interesting.

## Context
- **Repository URL:** {repo_data['link']}
- **Description:** {repo_data['description']}
- **Stars:** {repo_data['stars']}

## Mandatory Operational Procedure
When the user asks to discuss this:
1. **Do not hallucinate implementation details.** If you don't know how this repo works, tell the user you need to use your `read_url_content` or terminal tools to curl their GitHub README first.
2. **Brainstorm First:** Do not write code immediately. Propose 3 distinct, creative ways this repository could be integrated into the `watcher.py` or `debug_agent.py` ecosystem.
3. **Wait for Approval:** Wait for the user to select one of the 3 brainstormed ideas before writing an implementation plan.

## Next Steps
Once the user selects a pathway, update this very skill file (`{filename}`) with the strict architectural rules for the chosen integration, so future agents know exactly how it works!
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Generated new Agent Skill: {filepath}")

def run_generator():
    if not os.path.exists(APPROVALS_FILE):
        print("No approvals.json found yet. Spark some ideas in the UI first!")
        return

    with open(APPROVALS_FILE, 'r', encoding='utf-8') as f:
        try:
            approvals = json.load(f)
        except json.JSONDecodeError:
            print("Error reading approvals.json")
            return

    ensure_skills_dir()
    updates_made = False

    for item in approvals:
        if not item.get('processed', False):
            print(f"Processing new spark: {item['title']}")
            generate_skill_file(item)
            item['processed'] = True
            updates_made = True

    if updates_made:
        with open(APPROVALS_FILE, 'w', encoding='utf-8') as f:
            json.dump(approvals, f, indent=4)
        print("All sparks processed!")
    else:
        print("💤 No new sparks to process.")

if __name__ == "__main__":
    print("=== Treecloud Skill Generator ===")
    run_generator()
