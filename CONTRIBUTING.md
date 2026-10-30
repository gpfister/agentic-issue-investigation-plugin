# Contributing to agentic-investigate-plugin

Thank you for contributing to **`agentic-investigate-plugin`**! This plugin provides multi-repository root cause investigation capabilities for Google Antigravity.

---

## 1. Core Guidelines
- Adhere to the standards defined in [`rules/AGENTS.md`](file:///Users/gpfister/Development/Projects/gpfister/agentic/agentic-investigate-plugin/rules/AGENTS.md).
- Keep subagent definitions modular, declarative, and isolated in `agents/<agent>/agent.md`.
- Skills must include valid YAML frontmatter (`name`, `description`) matching the skill directory name.

---

## 2. Directory Structure

```text
agentic-investigate-plugin/
├── plugin.json         # Plugin manifest
├── pyproject.toml      # Project metadata & test dependencies
├── README.md           # Documentation
├── LICENSE             # MIT License
├── CONTRIBUTING.md     # Contribution guidelines
├── agents/             # Subagent definitions
│   ├── agent.md        # Central subagent & architecture specification
│   └── coding-investigate/ # Autonomous root cause investigator (@coding-investigate)
│       └── agent.md
├── skills/             # Progressive-disclosure skills
│   └── coding-investigate/ # Diagnostic runbooks & user grilling workflows
│       └── SKILL.md
├── rules/              # Plugin-scoped rules
│   └── AGENTS.md
└── tests/              # Test suite
    └── test_plugin.py
```

---

## 3. Testing
Run tests using `uv`:

```bash
uv run pytest
```

Validate plugin structure with `agy`:

```bash
agy plugin validate .
```
