---
name: q00 - ouroboros-integration
description: This skill should be used when the user asks to implement, discuss, or integrate Q00 / ouroboros into Project Treecloud.
---

# Q00 / ouroboros Integration Skill

You (the AI Agent) are currently analyzing an integration request for **Q00 / ouroboros**.
The user "Sparked" this idea from their Treecloud Hub because they found it interesting.

## Context
- **Repository URL:** https://github.com/Q00/ouroboros
- **Description:** Agent OS: Stop prompting. Start specifying.
- **Stars:** 3,784

## Mandatory Operational Procedure
When the user asks to discuss this:
1. **Do not hallucinate implementation details.** If you don't know how this repo works, tell the user you need to use your `read_url_content` or terminal tools to curl their GitHub README first.
2. **Brainstorm First:** Do not write code immediately. Propose 3 distinct, creative ways this repository could be integrated into the `watcher.py` or `debug_agent.py` ecosystem.
3. **Wait for Approval:** Wait for the user to select one of the 3 brainstormed ideas before writing an implementation plan.

## Next Steps
Once the user selects a pathway, update this very skill file (`q00 - ouroboros.md`) with the strict architectural rules for the chosen integration, so future agents know exactly how it works!
