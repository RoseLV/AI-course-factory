"""Keeps CLAUDE.md, the slash commands, and the scripts consistent.
Run: python -m unittest scripts/test_orchestration.py -v"""

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CLAUDE = (REPO / "CLAUDE.md").read_text(encoding="utf-8")
COMMANDS = REPO / ".claude" / "commands"
AGENTS = {p.stem for p in (REPO / ".claude" / "agents").glob("*.md")}
EXPECTED_COMMANDS = {"new-course", "continue", "status", "render", "qa", "ask-ta", "ta-digest"}


class Orchestration(unittest.TestCase):
    def test_commands_exist_and_have_descriptions(self):
        found = {p.stem for p in COMMANDS.glob("*.md")}
        self.assertEqual(EXPECTED_COMMANDS, found)
        for p in COMMANDS.glob("*.md"):
            text = p.read_text(encoding="utf-8")
            self.assertRegex(text, r"^---\ndescription: .{15,}\n", p.name)

    def test_arguments_commands_use_arguments_placeholder(self):
        for name in EXPECTED_COMMANDS:
            text = (COMMANDS / f"{name}.md").read_text(encoding="utf-8")
            self.assertIn("$ARGUMENTS", text, name)

    def test_claude_md_documents_every_command(self):
        for name in EXPECTED_COMMANDS:
            self.assertIn(f"`/{name}", CLAUDE, name)

    def test_agents_named_in_claude_md_exist(self):
        named = set(re.findall(r"\b(course-producer|research-analyst|curriculum-architect|deck-writer|"
                               r"assessment-designer|lab-engineer|qa-reviewer|ta-agent|[a-z]+-[a-z]+-agent)\b", CLAUDE))
        self.assertTrue(named <= AGENTS, f"CLAUDE.md names agents that do not exist: {named - AGENTS}")

    def test_every_pipeline_agent_is_used_in_claude_md(self):
        for agent in AGENTS:
            self.assertIn(agent, CLAUDE, agent)

    def test_scripts_named_in_claude_md_exist(self):
        for script in set(re.findall(r"scripts/([a-z_]+\.py)", CLAUDE)):
            self.assertTrue((REPO / "scripts" / script).is_file(), script)
        self.assertTrue((REPO / "build" / "render.py").is_file())

    def test_ask_ta_records_the_log_through_the_script(self):
        text = (COMMANDS / "ask-ta.md").read_text(encoding="utf-8")
        self.assertIn("scripts/ta_log.py", text)
        self.assertIn("Never write the log file by hand", text)

    def test_readme_documents_every_command_and_script(self):
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        for name in EXPECTED_COMMANDS:
            self.assertIn(f"`/{name}", readme, name)
        for needed in ("scripts/approve.py", "scripts/check_package.py", "readiness-check", "STYLE.md",
                       "PLAN.md", "dry-run-1.md", "Troubleshooting", "Gate 0", "Gate 1", "Gate 2"):
            self.assertIn(needed, readme, needed)
        self.assertNotIn("—", readme)

    def test_readme_paths_exist(self):
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        for rel in ("PLAN.md", "STYLE.md", "docs/dry-run-1.md", "scripts/readiness-check.ps1",
                    "scripts/readiness-check.sh", "templates", "build", "courses/_fixture"):
            self.assertTrue((REPO / rel).exists(), rel)
            self.assertIn(rel.split("/")[-1], readme, rel)

    def test_all_check_stages_are_named(self):
        for stage in ("viability", "syllabus", "production", "package", "published"):
            self.assertIn(stage, CLAUDE)

    def test_gate_rules_are_stated(self):
        lowered = CLAUDE.lower()
        for phrase in ("never approve for the human", "approve.py", "plain language", "is never an approval"):
            self.assertIn(phrase, lowered, phrase)

    def test_no_em_dashes(self):
        self.assertNotIn("\u2014", CLAUDE)
        for p in COMMANDS.glob("*.md"):
            self.assertNotIn("\u2014", p.read_text(encoding="utf-8"), p.name)

    def test_claude_md_stays_short(self):
        self.assertLess(len(CLAUDE.splitlines()), 200, "CLAUDE.md loads every session; keep it lean")


if __name__ == "__main__":
    unittest.main()
