"""Tests for agentic-issue-investigation-plugin structure and specifications."""

import json
from pathlib import Path
import re

PLUGIN_ROOT = Path(__file__).resolve().parent.parent


def extract_frontmatter_aliases(content: str) -> list[str]:
    match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return []
    fm = match.group(1)
    alias_match = re.search(r"aliases:\s*\n((?:\s*-\s+[^\n]+\n)+)", fm)
    if not alias_match:
        return []
    return [line.strip().lstrip("-").strip() for line in alias_match.group(1).strip().splitlines()]


def test_plugin_manifest_valid():
    manifest_file = PLUGIN_ROOT / "plugin.json"
    assert manifest_file.exists(), "plugin.json must exist"
    data = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert data.get("name") == "agentic-issue-investigation-plugin"
    assert data.get("license") == "MIT"


def test_license_exists():
    license_file = PLUGIN_ROOT / "LICENSE"
    assert license_file.exists(), "LICENSE must exist"
    content = license_file.read_text(encoding="utf-8")
    assert "MIT License" in content
    assert "Greg PFISTER" in content


def test_contributing_exists():
    contrib_file = PLUGIN_ROOT / "CONTRIBUTING.md"
    assert contrib_file.exists(), "CONTRIBUTING.md must exist"
    content = contrib_file.read_text(encoding="utf-8")
    assert "agentic-issue-investigation-plugin" in content


def test_investigate_agent_exists():
    agent_file = PLUGIN_ROOT / "agents" / "coding-investigate" / "agent.md"
    assert agent_file.exists(), "agents/coding-investigate/agent.md must exist"

    legacy_agent_dir = PLUGIN_ROOT / "agents" / "investigate"
    assert not legacy_agent_dir.exists(), "agents/investigate must NOT exist"

    content = agent_file.read_text(encoding="utf-8")
    assert "name: coding-investigate" in content
    assert "# Coding - Issue Investigator (@coding-investigate)" in content

    aliases = extract_frontmatter_aliases(content)
    assert aliases, "aliases must be defined in frontmatter"
    assert "investigate" not in aliases, "'investigate' alias must be excluded"
    alias_pattern = re.compile(r"^coding(-.*)?$")
    for alias in aliases:
        assert alias_pattern.match(alias), f"Alias '{alias}' does not match pattern '^coding(-.*)?$'"


def test_central_agent_guide_exists():
    central_file = PLUGIN_ROOT / "agents" / "agent.md"
    assert central_file.exists(), "agents/agent.md must exist"
    content = central_file.read_text(encoding="utf-8")
    assert "name: coding-investigate-catalog" in content
    assert "# Coding - Issue Investigation Subagents & Architecture (agents/agent.md)" in content


def test_investigate_skill_exists():
    skill_file = PLUGIN_ROOT / "skills" / "coding-investigate" / "SKILL.md"
    assert skill_file.exists(), "skills/coding-investigate/SKILL.md must exist"

    legacy_skill_dir = PLUGIN_ROOT / "skills" / "investigate"
    assert not legacy_skill_dir.exists(), "skills/investigate must NOT exist"

    content = skill_file.read_text(encoding="utf-8")
    assert "name: coding-investigate" in content
    assert "Multi-Repo Root Cause Search" in content


def test_rules_exist():
    rules_file = PLUGIN_ROOT / "rules" / "AGENTS.md"
    assert rules_file.exists(), "rules/AGENTS.md must exist"
    content = rules_file.read_text(encoding="utf-8")
    assert "Issue Investigation Standards" in content
    assert "agentic-project-documenting-plugin" in content
    assert f"agentic-{'document'}-plugin" not in content
    assert "agentic-obsidian-plugin" not in content
