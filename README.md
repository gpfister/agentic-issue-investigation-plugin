# agentic-issue-investigation-plugin

Autonomous multi-repository issue investigation plugin for [Google Antigravity](https://antigravity.google).

## Overview
`agentic-issue-investigation-plugin` provides dedicated subagents and progressive-disclosure skills to diagnose root causes across repositories, interrogate users for missing context, produce structured `issue-assessment.md` artifacts, and hand off approved remediation plans to `@coding`.

## Features
- **Declarative Subagent (`@coding-investigate`)**: Autonomous root cause investigator defined in [`agents/coding-investigate/agent.md`](file:///Users/gpfister/Development/Projects/gpfister/agentic/agentic-issue-investigation-plugin/agents/coding-investigate/) (alias: `@coding-investigate`).
- **Progressive Skill (`coding-investigate`)**: Diagnostic workflow and user clarification procedures in [`skills/coding-investigate/SKILL.md`](file:///Users/gpfister/Development/Projects/gpfister/agentic/agentic-issue-investigation-plugin/skills/coding-investigate/SKILL.md).
- **Interactive Approval Gates**: Requires explicit user approval for `issue-assessment.md` via Antigravity's interactive modal before remediation begins.
- **Remediation Confirmation (@coding)**: If `agentic-coding-plugin` is installed, asks user confirmation before handing off fixes to `@coding`.
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
