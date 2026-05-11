---
name: vectifyai - pageindex-integration
description: This skill should be used when the user asks to implement, discuss, or integrate VectifyAI / PageIndex into Project Treecloud.
---

# VectifyAI / PageIndex Integration Skill

You (the AI Agent) are currently analyzing an integration request for **VectifyAI / PageIndex**.
The user "Sparked" this idea from their Treecloud Hub because they found it interesting.

## Context
- **Repository URL:** https://github.com/VectifyAI/PageIndex
- **Description:** 📑 PageIndex: Document Index for Vectorless, Reasoning-based RAG
- **Stars:** 30,232

## Chosen Architecture: Treecloud Intelligence Vault & Deep Repo Indexer

The user has selected a **Hybrid of Pathway 1 and Pathway 3** for integrating PageIndex into Project Treecloud.

### 1. Deep-Context Repo Indexer (`watcher.py`)
- **Trigger:** When `watcher.py` detects a new "sparked" repository (or an existing one requires deep analysis).
- **Action:** Instead of just summarizing a README, `watcher.py` will utilize the PageIndex framework to parse the repository's documentation directory (`docs/`, `wiki/`, or structured markdown files) to generate a hierarchical JSON tree representing the repo's knowledge structure.
- **Storage:** The generated tree structures should be saved locally, perhaps in a `data/pageindex/repos/` directory, and linked to the repository's metadata in `data.json`.

### 2. The Hub's "Intelligence Vault" (Frontend & `app.py`)
- **Frontend UI (`index.html`):** Add an "Intelligence Vault" section allowing users to upload complex documents (PDFs, lengthy markdown files).
- **Backend API (`app.py`):** Add endpoints to receive these uploads.
- **Action:** The backend uses the PageIndex Python package to process these documents in the background, creating semantic tree structures for them.
- **Storage:** Indexed vault documents should be stored in a `data/pageindex/vault/` directory.
- **Retrieval interface:** The UI must provide a way to ask questions against the vault or indexed repos, querying the backend which then uses the PageIndex tree search to reason and return precise, referenced answers.

## Next Steps for Agents
If an agent is asked to *implement* this, they should:
1. Research the current state of `app.py`, `watcher.py`, and `index.html`.
2. Create an implementation plan proposing the exact code changes and endpoints required to support this hybrid architecture.
3. Ensure the implementation respects the existing lightweight, agentic nature of Treecloud.
