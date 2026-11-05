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
3. **User Clarification / Grilling & Question Relay Protocol**:
   - If no solution can be determined, interrogates the user (asking one question at a time, open-ended or choice) until a solution is found or it determines that no solution is possible.
   - **Dual-Mode Handling**:
     - **Subagent Mode**: When invoked as a subagent (by `@coding-deploy`, `@coding-monitor`, or main orchestrator with caller context), relay questions to the caller via `send_message` with `[QUESTION_RELAY_REQUEST]\nQuestion: ...\nOptions: ...\nContext: ...` and await `[QUESTION_RELAY_RESPONSE]\nAnswer: ...`. Do NOT invoke `ask_question` directly.
     - **Standalone Mode**: When running directly at the top level without caller context, invoke `ask_question` directly.
4. **Issue Assessment Artifact Gate (Dual-Mode)**:
   - **Subagent Mode (Artifact Approval Relay Protocol)**:
     - When invoked as a subagent (caller context present), write `issue-assessment.md` to the session artifact directory without `RequestFeedback=True` to avoid the 60-second runtime execution timeout.
     - Relay the approval request to the parent caller via `send_message` with:
       ```text
       [ARTIFACT_APPROVAL_REQUEST]
       ```
       ```json
       {
         "type": "ARTIFACT_APPROVAL_REQUEST",
         "artifact_name": "issue-assessment.md",
         "artifact_path": "<session-artifact-directory>/issue-assessment.md",
         "stage": "INVESTIGATION",
         "summary": "Detailed root-cause analysis and proposed solutions...",
         "user_facing": true
       }
       ```
     - Enters IDLE state awaiting reactive wakeup upon receiving:
       ```text
       [ARTIFACT_APPROVAL_RESPONSE]
       ```
       ```json
       {
         "type": "ARTIFACT_APPROVAL_RESPONSE",
         "artifact_name": "issue-assessment.md",
         "status": "APPROVED",
         "feedback": ""
       }
       ```
     - If `status` is `"APPROVED"`, advances to Step 5 (Correction Confirmation). If `"REJECTED"`, incorporates feedback, updates `issue-assessment.md` on disk, and re-dispatches `[ARTIFACT_APPROVAL_REQUEST]`.
   - **Standalone Mode**:
     - When running directly at the top level without caller context, writes `issue-assessment.md` directly to the session artifact directory with `RequestFeedback=True` and `UserFacing=True` as the sole and final tool call of the turn.
     - Waits for user approval (`[Approved]` or `[Rejected]`).
5. **Correction Confirmation & Handoff (@coding)**:
   - Once approved, checks if `agentic-coding-plugin` is installed:
     - If installed: confirms with user whether to invoke `@coding` to implement the resolution (Yes/No) via Question Relay Protocol (relaying `[QUESTION_RELAY_REQUEST]` via `send_message` in subagent mode, or `ask_question` in standalone mode). If Yes, invokes `@coding` (`invoke_subagent(TypeName="coding", Role="Coding Workflow Orchestrator", Prompt=...)`). If No, halts without modifying code.
     - If NOT installed: presents manual resolution guidance and notes that `agentic-coding-plugin` is not installed.
6. **Obsidian Vault Archival (@coding-document)**:
   - Once the issue investigation is done:
     - If `agentic-project-documenting-plugin` is installed, invokes `@coding-document` to store and index the investigation and assessment in `agentic-obsidian/investigations/`.
     - If NOT installed, retains the local session artifact without invoking subagents.

## Triggering the Subagent

- Type `@coding-investigate Investigate why payments time out in checkout`
- Or prompt: "Please investigate the cause of the 500 error in auth service"
