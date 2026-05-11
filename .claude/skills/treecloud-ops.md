---
name: treecloud-ops
description: This skill should be used whenever the user asks to "debug treecloud", "run diagnostics", "check watcher status", or troubleshoot any autonomous agent scripts like watcher.py or debug_agent.py.
---

# Treecloud Operations & Debugging Skill

# Treecloud Operations & Debugging Skill

## User Preferences
- **Terminal commands must always be in a fenced code block** — never inline in prose. The user clicks the copy/run button that appears on hover. This applies to every command, even simple one-liners.
- When suggesting `fcc-claude` tasks, always provide: (1) the launch command block, (2) a separate block with the prompt to paste into the REPL.

When operating on the Treecloud project, you must act as a strict Context Engineer. The primary risk in long-running agent debugging sessions is losing the "Artifact Trail" (forgetting exactly which files you modified, what errors you saw, or what the system state is).

## Mandatory Operating Procedure

1. **Diagnose First:** Before suggesting any code changes to `watcher.py` or editing JSON files, you MUST run `python debug_agent.py`.
2. **Context Compression:** When summarizing your findings to the user or compressing your context, you are FORBIDDEN from using freeform narrative summaries (e.g., "I ran the script and found some errors.").
3. **Strict Schema:** You MUST report all findings and session history using the Anchored Iterative Summarization format below. 

## Anchored Iterative Summarization Schema

Every time you provide a status update or compress context, use this exact markdown structure. Each section is a mandatory checklist item. If a section has no updates, write "None".

```markdown
## Session Intent
[What are we trying to accomplish in this specific session?]

## System State (from debug_agent.py)
[Report the exact output from the diagnostic script here, preserving critical info like timestamps, HTTP codes, or missing keys.]

## Artifact Trail
- [File Path]: [What you did (e.g. Read Only, Appended Data, Fixed Syntax)]
- [File Path]: ...

## Decisions Made
- [What did we decide to change and why?]

## Next Steps
1. [Clear, actionable next step]
```

## Gotchas & Rules
- **Do not hallucinate file paths.** Always use absolute paths or exact relative paths from the workspace root.
- **Do not compress errors.** If an API returns `403 Forbidden`, preserve the exact code, do not compress it to "an API error".
- **Tokens-per-task over Tokens-per-request.** It is better to use more tokens to strictly fill out the schema above than to save tokens and forget the artifact trail.

---

## DeepSeek / fcc-claude Workflow

Antigravity (this chat) handles planning, file edits, and quick changes. DeepSeek via `fcc-claude` is a separate Claude Code CLI session running in a terminal, powered by the free-claude-code proxy at `http://127.0.0.1:8082`.

**Prerequisites:** The proxy must be running. If it's not started, the user must run:
```powershell
$env:Path = "C:\Users\trevo\.local\bin;$env:Path"; fcc-server
```

### Model Tier Mapping
| Task complexity | Use tier | Maps to |
|---|---|---|
| Massive refactors, architecture | Opus | DeepSeek V4 Pro |
| Complex logic, multi-step reasoning | Sonnet | DeepSeek R1 |
| Quick edits, fast lookups | Haiku / default | DeepSeek V4 Flash |

### When to Suggest fcc-claude
Proactively offer a DeepSeek terminal prompt when the task involves:
- Implementing a **large new feature** end-to-end (> ~3 files)
- **Autonomous refactoring** where the user shouldn't need to approve each step
- **Debugging a complex traceback** that requires deep multi-step reasoning (suggest R1)
- **Batch processing** tasks (e.g. "index all repos", "reformat all proposals")
- Any task the user wants to **run overnight or unattended**

### Prompt Template for fcc-claude
When suggesting a DeepSeek prompt, format it as a ready-to-copy code block:

```powershell
fcc-claude
```
Then paste this as the first message in the Claude Code REPL:
```
[Task description - be specific about files, goals, and constraints]

Working directory: C:\Users\trevo\OneDrive\Documents\TREECLOUD
Do not ask for confirmation on individual file edits. Complete the full task autonomously.
```

### Tier Overrides
If the user wants a specific tier inside the REPL, they can type `/model` to pick Opus/Sonnet/Haiku.
