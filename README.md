# agentic-issue-investigation-plugin

Autonomous multi-repository issue investigation plugin for [Google Antigravity](https://antigravity.google).

## Overview
`agentic-issue-investigation-plugin` provides dedicated subagents and progressive-disclosure skills to diagnose root causes across repositories, interrogate users for missing context, produce structured `issue-assessment.md` artifacts, and hand off approved remediation plans to `@coding`.

## Features
- **Declarative Subagent (`@coding-investigate`)**: Autonomous root cause investigator defined in [`agents/coding-investigate/agent.md`](file:///Users/gpfister/Development/Projects/gpfister/agentic/agentic-issue-investigation-plugin/agents/coding-investigate/) (alias: `@coding-investigate`).
- **Progressive Skill (`coding-investigate`)**: Diagnostic workflow and user clarification procedures in [`skills/coding-investigate/SKILL.md`](file:///Users/gpfister/Development/Projects/gpfister/agentic/agentic-issue-investigation-plugin/skills/coding-investigate/SKILL.md).
- **Interactive Approval Gates & Artifact Approval Relay (Dual-Mode)**: Requires explicit user approval for `issue-assessment.md`. When running under a parent caller (`caller_id` present), writes the artifact to disk without feedback metadata and dispatches `[ARTIFACT_APPROVAL_REQUEST]` via `send_message` to eliminate 60s host execution timeouts; falls back to direct `write_file(RequestFeedback=True)` as the sole and final tool call when running standalone at session root.
- **Question Relay Protocol (Dual-Mode)**: Supports dual-mode user clarification and remediation confirmation gates: when running under a parent caller (`caller_id` present), dispatches `[QUESTION_RELAY_REQUEST]` via `send_message` to avoid 60s host execution timeouts; falls back to direct `ask_question` when running standalone at session root.
- **Remediation Confirmation & Standardized Orchestration Prompt (@coding)**: If `agentic-coding-plugin` is installed, asks user confirmation before handing off fixes to `@coding` using the standardized orchestration template (`Orchestrate the 7-stage software development lifecycle to implement the following feature / correction based on the approved assessment: <details/path>. Do not implement directly; delegate all phases through worker subagents.`), ensuring strict enforcement of anti-direct-coding guardrails.
- **Vault Documentation Archival (@coding-document)**: If `agentic-project-documenting-plugin` is installed, documents approved issues in `agentic-obsidian/investigations/`.

## Installation & Activation

```bash
# Enable in Antigravity session:
agy plugin enable agentic-issue-investigation-plugin
```

## Contributing
See [CONTRIBUTING.md](file:///Users/gpfister/Development/Projects/gpfister/agentic/agentic-issue-investigation-plugin/CONTRIBUTING.md) for contribution guidelines and testing practices.

## License
This project is licensed under the [MIT License](file:///Users/gpfister/Development/Projects/gpfister/agentic/agentic-issue-investigation-plugin/LICENSE).
