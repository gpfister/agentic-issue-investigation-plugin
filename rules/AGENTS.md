# Issue Investigation Standards — agentic-investigate-plugin

This rule set applies whenever the `agentic-investigate-plugin` is active in an Antigravity session.

---

## 1. Investigation Principles
- **Evidence-Based Diagnosis**: Never speculate or propose code modifications without tangible evidence (stack traces, logs, git commits, reproducible steps).
- **Multi-Repository Discipline**: Trace cross-service RPCs, REST calls, shared libraries, and schema contracts across all repositories before concluding root causes.
- **Read-Only Investigation**: During the diagnostic phase, do not alter application source code or tests. If `agentic-coding-plugin` is installed, modifying code occurs only after human approval through the coding orchestrator (`@coding`).

---

## 2. Interactive User Interrogation & Approval Gates
- **One Question at a Time**: When asking for user clarification, always use `ask_question` asking one question at a time.
- **Sole and Final Tool Call Rule**:
  - Writing `issue-assessment.md` with `RequestFeedback=True` must be the sole and final tool call of that turn.
  - Never batch secondary tool calls after authoring the artifact so Antigravity renders the interactive Approve / Reject buttons.
- **Remediation Confirmation Gate**:
  - If `agentic-coding-plugin` is installed: ask the user via `ask_question` whether they want to invoke `@coding` to work on the resolution. If Yes, invoke `@coding`.
  - If `agentic-coding-plugin` is NOT installed: provide manual remediation steps without invoking `@coding`.

---

## 3. Communication & Links
- Keep reports structured, concise, and high-signal.
- Always generate clickable markdown links using the `file://` scheme when referencing affected files, functions, and configuration files.

---

## 4. Documentation Archival with @coding-document
- When `agentic-document-plugin` is installed, once the issue investigation is done, invoke `@coding-document` to store and archive the root-cause diagnosis, evidence, and remediation assessment in `agentic-obsidian/investigations/`.
- If `agentic-document-plugin` is not installed, preserve the local `issue-assessment.md` artifact without invoking subagents.
