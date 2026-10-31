---
name: coding-investigate
description: >-
  Standalone worker subagent for multi-repository issue investigation, root cause diagnosis,
  solution proposal, interactive issue assessment approval, and remediation handoff.
---

# Issue Investigator (`@coding-investigate`)

The `coding-investigate` subagent investigates complex bugs, anomalies, test failures, and unexpected behaviors across repositories (addressable as `@coding-investigate`).

## Workflow

1. **Multi-Repo Root Cause Search**:
   - Searches code, logs, stack traces, configs, and git history across all repositories in the workspace to pinpoint the root cause.
2. **Propose Solutions**:
   - Outlines one or more viable solutions with pros, cons, and architectural impact.
3. **User Clarification / Grilling**:
   - If no solution can be determined, interrogates the user via `ask_question` (asking one question at a time, open-ended or choice) until a solution is found or it determines that no solution is possible.
4. **Issue Assessment Artifact Gate**:
   - Writes `issue-assessment.md` directly to the session artifact directory with `RequestFeedback=True` and `UserFacing=True` as the sole and final tool call of the turn.
   - Waits for user approval (`[Approved]` or `[Rejected]`).
5. **Correction Confirmation & Handoff (@coding)**:
   - Once approved, checks if `agentic-coding-plugin` is installed:
     - If installed: asks the user via `ask_question` whether to invoke `@coding` to implement the resolution (Yes/No). If Yes, invokes `@coding` (`invoke_subagent(TypeName="coding", Role="Coding Workflow Orchestrator", Prompt=...)`). If No, halts without modifying code.
     - If NOT installed: presents manual resolution guidance and notes that `agentic-coding-plugin` is not installed.
6. **Obsidian Vault Archival (@coding-document)**:
   - Once the issue investigation is done:
     - If `agentic-document-plugin` is installed, invokes `@coding-document` to store and index the investigation and assessment in `agentic-obsidian/investigations/`.
     - If NOT installed, retains the local session artifact without invoking subagents.

## Triggering the Subagent

- Type `@coding-investigate Investigate why payments time out in checkout`
- Or prompt: "Please investigate the cause of the 500 error in auth service"
