"""Validates the agent files. Run: python -m unittest scripts/test_agents.py -v"""

import re
import unittest
from pathlib import Path

AGENTS = Path(__file__).resolve().parent.parent / ".claude" / "agents"
EXPECTED = {
    "course-producer", "research-analyst", "curriculum-architect", "deck-writer",
    "assessment-designer", "lab-engineer", "qa-reviewer", "ta-agent",
}
VALID_TOOLS = {"Read", "Write", "Edit", "Glob", "Grep", "WebSearch", "WebFetch", "Bash"}
VALID_MODELS = {"opus", "sonnet", "haiku"}
# Subagents never run commands in this pipeline, and never get Bash.
FORBIDDEN_TOOLS = {"Bash"}


def parse(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    assert m, f"{path.name} has no front matter"
    meta = {}
    for line in m.group(1).splitlines():
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    return meta, m.group(2)


class AgentFiles(unittest.TestCase):
    def test_exactly_the_expected_agents(self):
        found = {p.stem for p in AGENTS.glob("*.md")}
        self.assertEqual(EXPECTED, found)

    def test_no_video_agent(self):
        self.assertFalse(list(AGENTS.glob("*video*")))

    def test_front_matter(self):
        for p in AGENTS.glob("*.md"):
            meta, _ = parse(p)
            self.assertEqual(p.stem, meta.get("name"), p.name)
            self.assertGreater(len(meta.get("description", "")), 40, p.name)
            self.assertIn(meta.get("model"), VALID_MODELS, p.name)
            tools = {t.strip() for t in meta.get("tools", "").split(",")}
            self.assertTrue(tools and tools <= VALID_TOOLS, f"{p.name}: {tools}")
            self.assertFalse(tools & FORBIDDEN_TOOLS, f"{p.name} has a forbidden tool")

    def test_no_em_dashes(self):
        for p in AGENTS.glob("*.md"):
            self.assertNotIn("—", p.read_text(encoding="utf-8"), p.name)

    def test_every_agent_ends_with_the_report_block(self):
        for p in AGENTS.glob("*.md"):
            body = p.read_text(encoding="utf-8")
            for key in ("DONE:", "PATHS:", "COUNTS:", "GAPS:", "NEEDS A HUMAN:"):
                self.assertIn(key, body, f"{p.name} lacks {key}")

    def test_every_agent_reads_style_and_states_its_scope(self):
        for p in AGENTS.glob("*.md"):
            body = p.read_text(encoding="utf-8")
            if p.stem == "ta-agent":
                # The ta-agent reads only its manifest files, so it must not be told to read STYLE.md.
                self.assertNotIn("Read `STYLE.md`", body)
            else:
                self.assertIn("STYLE.md", body, p.name)
            self.assertIn("What you may write", body, p.name)

    def test_no_agent_may_approve(self):
        for p in AGENTS.glob("*.md"):
            body = p.read_text(encoding="utf-8")
            self.assertIn("APPROVALS.md", body, f"{p.name} should say it never writes it")

    def test_only_researcher_has_web_tools(self):
        for p in AGENTS.glob("*.md"):
            meta, _ = parse(p)
            has_web = bool({"WebSearch", "WebFetch"} & {t.strip() for t in meta["tools"].split(",")})
            self.assertEqual(p.stem == "research-analyst", has_web, p.name)

    def test_ta_agent_cannot_search_the_repo(self):
        meta, _ = parse(AGENTS / "ta-agent.md")
        tools = {t.strip() for t in meta["tools"].split(",")}
        self.assertFalse(tools & {"Glob", "Grep"}, "ta-agent must not search beyond the manifest")

    def test_ta_agent_reports_its_log_line_instead_of_writing_the_log(self):
        body = (AGENTS / "ta-agent.md").read_text(encoding="utf-8")
        self.assertIn("`LOG: date | theme", body)
        self.assertNotIn("append one line to", body)
        self.assertIn("In ASK mode you write no file at all", body)

    def test_qa_cannot_edit(self):
        meta, _ = parse(AGENTS / "qa-reviewer.md")
        tools = {t.strip() for t in meta["tools"].split(",")}
        self.assertNotIn("Edit", tools)


if __name__ == "__main__":
    unittest.main()
