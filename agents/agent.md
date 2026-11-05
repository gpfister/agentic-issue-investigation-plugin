---
name: coding-investigate-catalog
description: Architecture overview and catalog for the agentic-issue-investigation-plugin subagents.
enable_write_tools: false
enable_subagent_tools: false
enable_mcp_tools: false
tools:
  - read_file
  - list_dir
---

# Coding - Issue Investigation Subagents & Architecture (agents/agent.md)

This document defines the subagent architecture and catalog for the **`agentic-issue-investigation-plugin`**.

---

## 1. Architectural Overview

The `agentic-issue-investigation-plugin` provides autonomous root cause analysis, user interrogation, solution formulation, and remediation handoffs across multi-repository workspaces. It isolates bug hunting and defect diagnostics into a specialized subagent (`@coding-investigate`), ensuring code is never modified without evidence-backed root cause analysis and explicit human approval.

### Directory Structure
```text
agents/
├── agent.md                    # Master subagent guide (this file)
└── coding-investigate/         # Standalone Issue Investigator (@coding-investigate)
    └── agent.md
```

---

## 2. Subagent Catalog

| Agent Handle | Directory | `enable_write_tools` | `enable_subagent_tools` | `enable_mcp_tools` | Allowed Tools | Description |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **`@coding-investigate`** | [`agents/coding-investigate/`](file:///Users/gpfister/Development/Projects/gpfister/agentic/agentic-issue-investigation-plugin/agents/coding-investigate/) | `True` | `True` | `True` | `read_file`, `list_dir`, `run_command`, `search_web`, `ask_question`, `write_file`, `invoke_subagent`, `send_message`, `manage_subagents` | Dual-mode multi-repository root cause investigator producing `issue-assessment.md` artifacts, grilling users when needed (via Question Relay Protocol when invoked as a subagent, or `ask_question` directly when standalone), relaying artifact approvals via Artifact Approval Relay Protocol in subagent mode or presenting directly with `RequestFeedback=True` in standalone mode, handing off approved fixes to `@coding` (if installed), and archiving to `@coding-document` (if installed). |

---

## 3. Investigation & Remediation Protocol

```text
Multi-Repo Search ──> Solution Found? ──(No)──> Grill User (Dual-Mode) ──────┐
                            │                    * Subagent: [QUESTION_RELAY] │
                          (Yes) <──────────────── * Standalone: ask_question ─┘
                            ▼
             Write issue-assessment.md (Dual-Mode)
             * Subagent: [ARTIFACT_APPROVAL_REQUEST]
             * Standalone: RequestFeedback=True
                            │
                     [Approved by User]
                            ▼
              agentic-coding-plugin installed?
                   │                    │
                 (Yes)                 (No)
                   ▼                    ▼
        Ask Resolution Confirmation   Provide manual
        (Dual-Mode Relay / Question)  resolution steps
         │             │
       (Yes)          (No)
         ▼             ▼
   Invoke @coding     Stop
         │             │
         └──────┬──────┘
                ▼
agentic-project-documenting-plugin installed?
       │                    │
     (Yes)                 (No)
       ▼                    ▼
Invoke @coding-document    Retain local
to document issue          artifact
```

### Dual-Mode Question Handling & Question Relay Protocol
`@coding-investigate` supports dual-mode user interrogation and confirmation:
1. **Subagent Mode (Question Relay Protocol)**:
   - When invoked by a parent orchestrator (`@coding-deploy`, `@coding-monitor`, or main session orchestrator with caller context), it relays user questions via `send_message` with:
     ```text
     [QUESTION_RELAY_REQUEST]
     Question: ...
     Options: ...
     Context: ...
     ```
   - Awaits `[QUESTION_RELAY_RESPONSE]\nAnswer: ...` to receive the human decision before continuing.
2. **Standalone Mode**:
   - When running directly at the top level without parent caller context, it invokes `ask_question` directly.

### Dual-Mode Artifact Approval Handling & Relay Protocol
`@coding-investigate` supports dual-mode artifact gate approval:
1. **Subagent Mode (Artifact Approval Relay Protocol)**:
   - When invoked by a parent orchestrator, write `issue-assessment.md` directly to disk without `RequestFeedback=True` to eliminate the 60-second runtime execution timeout.
   - Dispatch `[ARTIFACT_APPROVAL_REQUEST]` to `caller_id` via `send_message`:
     ```text
     [ARTIFACT_APPROVAL_REQUEST]
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
     {
       "type": "ARTIFACT_APPROVAL_RESPONSE",
       "artifact_name": "issue-assessment.md",
       "status": "APPROVED",
       "feedback": ""
     }
     ```
   - If `"APPROVED"`, advances to resolution confirmation. If `"REJECTED"`, revises findings using `feedback`, updates the file, and re-dispatches `[ARTIFACT_APPROVAL_REQUEST]`.
2. **Standalone Mode**:
   - When running directly at top level without parent caller context, write `issue-assessment.md` with `ArtifactMetadata={"RequestFeedback": True, "UserFacing": True}`.
   - **Sole & Final Tool Call Rule**: `write_file` must be the sole and final tool call of that turn to trigger the interactive Approve / Reject buttons in Antigravity.
