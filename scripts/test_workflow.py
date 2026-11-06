"""Tests for approve.py, course_status.py, courselib.py, and finding owners.
Run: python -m unittest scripts/test_workflow.py -v"""

import contextlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import approve  # noqa: E402
import check_package as cp  # noqa: E402
import course_status  # noqa: E402
import courselib as cl  # noqa: E402

STATUS = """# Status: demo

- **Course:** Demo
- **State:** {state}
- **Awaiting:** {awaiting}

## Next step

{nxt}
"""


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="wf-"))
        self.course = self.tmp / "demo"
        self.course.mkdir()
        self.set_status("proposed", "nothing")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def set_status(self, state, awaiting, nxt="Do the thing."):
        (self.course / "STATUS.md").write_text(STATUS.format(state=state, awaiting=awaiting, nxt=nxt), encoding="utf-8")

    def run_approve(self, *args):
        err, out = io.StringIO(), io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
            code = approve.main(["demo", "--courses-dir", str(self.tmp), "--date", "2026-11-03", *args])
        return code, out.getvalue(), err.getvalue()

    def approvals(self):
        return (self.course / "APPROVALS.md").read_text(encoding="utf-8")


class Init(Base):
    def test_init_creates_file_once(self):
        self.assertEqual(0, self.run_approve("--init")[0])
        self.assertIn("Approvals: demo", self.approvals())
        self.assertEqual(1, self.run_approve("--init")[0])


class Approve(Base):
    def setUp(self):
        super().setUp()
        self.run_approve("--init")

    def test_refuses_when_no_gate_pending(self):
        code, _, err = self.run_approve("approve", "yes")
        self.assertEqual(1, code)
        self.assertIn("no gate pending", err)

    def test_logs_plain_yes_at_gate_0(self):
        self.set_status("awaiting-gate-0", "gate-0")
        code, out, _ = self.run_approve("approve", "yes, good to go")
        self.assertEqual(0, code, out)
        self.assertIn('2026-11-03 | viability | APPROVED | "yes, good to go"', self.approvals())
        self.assertTrue(cl.approved(self.course, "viability"))

    def test_positive_phrases_accepted(self):
        for phrase in ("yes", "good to go", "looks great", "ship it", "approved", "go ahead", "Yes please proceed"):
            self.set_status("awaiting-gate-0", "gate-0")
            self.assertEqual(0, self.run_approve("approve", phrase)[0], phrase)

    def test_hedged_replies_refused(self):
        self.set_status("awaiting-gate-0", "gate-0")
        for phrase in ("yes but change the title", "looks good, however fix slide 3", "is this ok?",
                       "not bad", "no", "wait, hold on", "good except the capstone", "maybe"):
            code, _, err = self.run_approve("approve", phrase)
            self.assertEqual(1, code, phrase)
            self.assertIn("hedged", err)
        self.assertEqual({}, cl.read_approvals(self.course))

    def test_long_reply_refused(self):
        self.set_status("awaiting-gate-0", "gate-0")
        self.assertEqual(1, self.run_approve("approve", "yes " + "great " * 80)[0])

    def test_empty_reply_refused(self):
        self.set_status("awaiting-gate-0", "gate-0")
        self.assertEqual(1, self.run_approve("approve", "   ")[0])

    def test_gates_must_go_in_order(self):
        self.set_status("awaiting-gate-1", "gate-1")
        code, _, err = self.run_approve("approve", "yes")
        self.assertEqual(1, code)
        self.assertIn("before gate 0", err)
        self.set_status("awaiting-gate-0", "gate-0")
        self.run_approve("approve", "yes")
        self.set_status("awaiting-gate-1", "gate-1")
        self.assertEqual(0, self.run_approve("approve", "good to go")[0])
        self.set_status("awaiting-gate-2", "gate-2")
        self.assertEqual(0, self.run_approve("approve", "yes")[0])
        self.assertEqual({"viability": "APPROVED", "syllabus": "APPROVED", "package": "APPROVED"},
                         cl.read_approvals(self.course))

    def test_reject_logs_notes_verbatim_even_when_hedged(self):
        self.set_status("awaiting-gate-0", "gate-0")
        code, out, _ = self.run_approve("reject", 'no, the "capstone" is too big')
        self.assertEqual(0, code)
        self.assertIn("REJECTED", self.approvals())
        self.assertFalse(cl.approved(self.course, "viability"))
        self.assertIn("notes verbatim", out)

    def test_later_decision_replaces_earlier(self):
        self.set_status("awaiting-gate-0", "gate-0")
        self.run_approve("reject", "redo it")
        self.assertEqual("REJECTED", cl.read_approvals(self.course)["viability"])
        self.run_approve("approve", "yes")
        self.assertEqual("APPROVED", cl.read_approvals(self.course)["viability"])

    def test_missing_approvals_file(self):
        (self.course / "APPROVALS.md").unlink()
        self.set_status("awaiting-gate-0", "gate-0")
        self.assertEqual(1, self.run_approve("approve", "yes")[0])

    def test_usage_errors(self):
        self.assertEqual(2, self.run_approve()[0])
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(2, approve.main(["nope", "--courses-dir", str(self.tmp), "approve", "yes"]))


class Lib(Base):
    def test_status_field_and_awaiting(self):
        self.assertEqual("proposed", cl.status_field(self.course, "State"))
        self.assertIsNone(cl.awaiting_gate(self.course))
        self.set_status("awaiting-gate-2", "gate-2")
        self.assertEqual(2, cl.awaiting_gate(self.course))
        self.set_status("awaiting-gate-2", "Gate-1")
        self.assertEqual(1, cl.awaiting_gate(self.course))
        self.set_status("x", "gate-7")
        self.assertIsNone(cl.awaiting_gate(self.course))


class Status(Base):
    def test_lists_active_courses_only(self):
        self.set_status("awaiting-gate-1", "gate-1", "Read the syllabus.")
        done = self.tmp / "done"
        done.mkdir()
        (done / "STATUS.md").write_text(STATUS.format(state="published", awaiting="nothing", nxt="none"), encoding="utf-8")
        fixture = self.tmp / "_fixture"
        fixture.mkdir()
        (fixture / "STATUS.md").write_text(STATUS.format(state="proposed", awaiting="nothing", nxt="x"), encoding="utf-8")
        lines = course_status.summarise(self.tmp, include_done=False)
        self.assertEqual(1, len(lines))
        self.assertIn("demo", lines[0])
        self.assertIn("gate 1 (syllabus)", lines[0])
        self.assertIn("Read the syllabus.", lines[0])
        self.assertEqual(2, len(course_status.summarise(self.tmp, include_done=True)))

    def test_hook_is_silent_with_no_courses(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            course_status.main(["--hook", "--courses-dir", str(self.tmp / "empty")])
        self.assertEqual("", out.getvalue())

    def test_hook_prints_header_when_active(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            course_status.main(["--hook", "--courses-dir", str(self.tmp)])
        self.assertIn("courses in progress", out.getvalue())


class Owners(unittest.TestCase):
    def test_by_folder(self):
        cases = {
            "02-deck/deck-m01.md slide 3": "deck-writer",
            "03-assessments/student/quiz-m01.md": "assessment-designer",
            "03-assessments/instructor/quiz-m01-key.md": "assessment-designer",
            "04-labs/lab-m01.md": "lab-engineer",
            "01-syllabus/syllabus.md": "curriculum-architect",
            "00-viability/source-pack.md": "research-analyst",
            "qa/alignment-matrix.md": "qa-reviewer",
            "STATUS.md": "course-producer",
            "APPROVALS.md": "main session",
            "maintenance/ta-log.md": "ta-agent",
        }
        for path, owner in cases.items():
            self.assertEqual(owner, cp.owner_for("EM-DASH", path), path)
        self.assertEqual("deck-writer", cp.owner_for("EM-DASH", "02-deck/deck-m01.md:14"))

    def test_pdf_findings_belong_to_the_main_session(self):
        self.assertEqual("main session (render)", cp.owner_for("PDF-STALE", "01-syllabus/syllabus.md"))

    def test_every_finding_has_an_owner(self):
        tmp = Path(tempfile.mkdtemp(prefix="own-"))
        try:
            course = tmp / "_fixture"
            shutil.copytree(cp.REPO / "courses" / "_fixture", course, ignore=shutil.ignore_patterns("dist"))
            (course / "04-labs/lab-m01.md").unlink()
            report = cp.check_course(course, "package", True)
            self.assertTrue(report.findings)
            for f in report.findings:
                self.assertTrue(f.owner, f.code)
            by_code = {f.code: f.owner for f in report.findings}
            self.assertEqual("lab-engineer", by_code["MANIFEST-MISSING"])
            self.assertEqual("main session (render)", by_code["PDF-MISSING"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
