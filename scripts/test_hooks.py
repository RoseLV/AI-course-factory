"""Tests for the stage guard hook and the settings file.
Run: python -m unittest scripts/test_hooks.py -v"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GUARD = REPO / "scripts" / "hooks" / "stage_guard.py"
FIXTURE = REPO / "courses" / "_fixture"
LINE = '2026-11-03 | {stage} | APPROVED | "yes"\n'


class Guard(unittest.TestCase):
    def setUp(self):
        self.project = Path(tempfile.mkdtemp(prefix="guard-"))
        self.course = self.project / "courses" / "demo"
        self.course.mkdir(parents=True)
        (self.course / "APPROVALS.md").write_text("# Approvals\n", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.project, ignore_errors=True)

    def approve(self, *stages):
        with open(self.course / "APPROVALS.md", "a", encoding="utf-8") as f:
            for s in stages:
                f.write(LINE.format(stage=s))

    def call(self, rel, tool="Write", raw=None, cwd=None, absolute=True):
        path = str(self.course / rel) if absolute else rel
        payload = raw if raw is not None else json.dumps(
            {"tool_name": tool, "tool_input": {"file_path": path}, "cwd": cwd or str(self.project)})
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project))
        return subprocess.run([sys.executable, str(GUARD)], input=payload, capture_output=True, text=True, env=env)

    def assertBlocked(self, rel, **kw):
        r = self.call(rel, **kw)
        self.assertEqual(2, r.returncode, f"{rel}: {r.stderr}")
        self.assertIn("stage guard", r.stderr)

    def assertAllowed(self, rel, **kw):
        r = self.call(rel, **kw)
        self.assertEqual(0, r.returncode, f"{rel}: {r.stderr}")

    def full_course(self):
        shutil.rmtree(self.course)
        shutil.copytree(FIXTURE, self.course, ignore=shutil.ignore_patterns("dist"))


class Ordering(Guard):
    def test_approvals_never_writable(self):
        self.assertBlocked("APPROVALS.md")
        self.assertBlocked("APPROVALS.md", tool="Edit")
        self.approve("viability", "syllabus", "package")
        self.assertBlocked("APPROVALS.md")

    def test_first_stage_and_status_always_open(self):
        self.assertAllowed("00-viability/viability-brief.md")
        self.assertAllowed("STATUS.md")

    def test_syllabus_needs_gate_0(self):
        self.assertBlocked("01-syllabus/syllabus.md")
        self.approve("viability")
        self.assertAllowed("01-syllabus/syllabus.md")

    def test_production_needs_gate_1(self):
        self.approve("viability")
        for rel in ("02-deck/deck-m01.md", "03-assessments/student/quiz-m01.md",
                    "03-assessments/instructor/quiz-m01-key.md", "04-labs/lab-m01.md"):
            self.assertBlocked(rel)
        self.approve("syllabus")
        for rel in ("02-deck/deck-m01.md", "03-assessments/student/quiz-m01.md", "04-labs/lab-m01.md"):
            self.assertAllowed(rel)

    def test_rejection_closes_the_stage_again(self):
        self.approve("viability")
        with open(self.course / "APPROVALS.md", "a", encoding="utf-8") as f:
            f.write('2026-11-04 | viability | REJECTED | "redo"\n')
        self.assertBlocked("01-syllabus/syllabus.md")

    def test_qa_needs_complete_package(self):
        self.full_course()
        (self.course / "APPROVALS.md").write_text("# Approvals\n", encoding="utf-8")
        self.assertBlocked("qa/qa-report.md")
        self.approve("viability", "syllabus")
        self.assertAllowed("qa/qa-report.md")
        (self.course / "04-labs/lab-m01.md").unlink()
        self.assertBlocked("qa/qa-report.md")

    def test_qa_blocked_without_syllabus_gate_even_if_complete(self):
        self.full_course()
        (self.course / "APPROVALS.md").write_text("# Approvals\n", encoding="utf-8")
        self.approve("viability")
        self.assertBlocked("qa/qa-report.md")

    def test_manifest_and_maintenance_need_gate_2(self):
        self.full_course()
        (self.course / "APPROVALS.md").write_text("# Approvals\n", encoding="utf-8")
        self.approve("viability", "syllabus")
        self.assertBlocked("qa/ta-grounding-manifest.md")
        self.assertBlocked("maintenance/ta-log.md")
        self.approve("package")
        self.assertAllowed("qa/ta-grounding-manifest.md")
        self.assertAllowed("maintenance/ta-log.md")


class Passthrough(Guard):
    def test_other_tools_allowed(self):
        self.assertAllowed("01-syllabus/syllabus.md", tool="Read")
        self.assertAllowed("01-syllabus/syllabus.md", tool="Bash")

    def test_paths_outside_courses_allowed(self):
        r = subprocess.run(
            [sys.executable, str(GUARD)],
            input=json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(self.project / "STYLE.md")}}),
            capture_output=True, text=True, env=dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project)))
        self.assertEqual(0, r.returncode)

    def test_relative_path_resolves_against_cwd(self):
        self.assertBlocked("courses/demo/01-syllabus/syllabus.md", absolute=False, cwd=str(self.project))

    def test_dotdot_traversal_cannot_escape(self):
        self.assertBlocked("02-deck/../01-syllabus/syllabus.md")
        self.assertBlocked("00-viability/../APPROVALS.md")

    @unittest.skipUnless(os.name == "nt", "MSYS style paths only occur on Windows")
    def test_msys_style_paths_are_understood(self):
        drive, rest = os.path.splitdrive(str(self.course / "APPROVALS.md"))
        msys = "/" + drive[0].lower() + rest.replace("\\", "/")
        r = subprocess.run(
            [sys.executable, str(GUARD)],
            input=json.dumps({"tool_name": "Write", "tool_input": {"file_path": msys}}),
            capture_output=True, text=True, env=dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project)))
        self.assertEqual(2, r.returncode, r.stderr)

    @unittest.skipUnless(os.name == "nt", "MSYS style paths only occur on Windows")
    def test_msys_style_project_dir_is_understood(self):
        drive, rest = os.path.splitdrive(str(self.project))
        msys_project = "/" + drive[0].lower() + rest.replace("\\", "/")
        r = subprocess.run(
            [sys.executable, str(GUARD)],
            input=json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(self.course / "APPROVALS.md")}}),
            capture_output=True, text=True, env=dict(os.environ, CLAUDE_PROJECT_DIR=msys_project))
        self.assertEqual(2, r.returncode, r.stderr)

    def test_dist_is_allowed(self):
        self.assertAllowed("dist/01-syllabus/syllabus.pdf")

    def test_bad_input_warns_but_does_not_block(self):
        r = self.call("x", raw="not json")
        self.assertEqual(1, r.returncode)
        self.assertIn("allowing the call", r.stderr)

    def test_missing_file_path_allowed(self):
        r = self.call("x", raw=json.dumps({"tool_name": "Write", "tool_input": {}}))
        self.assertEqual(0, r.returncode)


class Settings(unittest.TestCase):
    def setUp(self):
        self.cfg = json.loads((REPO / ".claude" / "settings.json").read_text(encoding="utf-8"))

    def test_guard_is_registered_for_edit_tools(self):
        pre = self.cfg["hooks"]["PreToolUse"][0]
        for tool in ("Write", "Edit", "MultiEdit"):
            self.assertIn(tool, pre["matcher"])
        self.assertIn("stage_guard.py", pre["hooks"][0]["command"])

    def test_session_start_shows_status(self):
        cmd = self.cfg["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        self.assertIn("course_status.py", cmd)

    def test_hook_scripts_exist(self):
        self.assertTrue(GUARD.is_file())
        self.assertTrue((REPO / "scripts" / "course_status.py").is_file())

    def test_no_blanket_bash_or_push_permission(self):
        allow = self.cfg["permissions"]["allow"]
        self.assertNotIn("Bash", allow)
        self.assertFalse([a for a in allow if "git push" in a])


if __name__ == "__main__":
    unittest.main()
