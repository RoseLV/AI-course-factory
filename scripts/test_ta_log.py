"""Tests for ta_log.py. Run: python -m unittest scripts/test_ta_log.py -v"""

import contextlib
import io
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ta_log  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "ta_log.py"
GOOD = "2026-11-03 | remove on a missing name | lab step 3 | answered"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="talog-"))
        self.course = self.tmp / "demo"
        self.course.mkdir()
        (self.course / "APPROVALS.md").write_text(
            '2026-11-03 | package | APPROVED | "yes"\n', encoding="utf-8")
        self.log = self.course / "maintenance" / "ta-log.md"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_main(self, entry):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = ta_log.main(["demo", entry, "--courses-dir", str(self.tmp)])
        return code, out.getvalue(), err.getvalue()


class Entries(Base):
    def test_first_entry_creates_the_file_with_a_header(self):
        self.assertEqual(0, self.run_main(GOOD)[0])
        text = self.log.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# TA log"))
        self.assertIn(GOOD, text)

    def test_entries_append_and_keep_order(self):
        self.run_main(GOOD)
        self.run_main("2026-11-04 | grades question | quiz-m01 | escalated: grades")
        lines = self.log.read_text(encoding="utf-8").splitlines()
        self.assertEqual(GOOD, lines[-2])
        self.assertTrue(lines[-1].endswith("escalated: grades"))

    def test_all_escalation_categories_accepted(self):
        for cat in ta_log.CATEGORIES:
            self.assertEqual(0, self.run_main(f"2026-11-03 | theme | place | escalated: {cat}")[0], cat)

    def test_refusals(self):
        bad = {
            "three fields": "2026-11-03 | theme | answered",
            "five fields": "2026-11-03 | a | b | answered | extra",
            "bad date": "Nov 3 | theme | place | answered",
            "empty theme": "2026-11-03 |  | place | answered",
            "unknown outcome": "2026-11-03 | theme | place | maybe",
            "unknown category": "2026-11-03 | theme | place | escalated: rudeness",
            "quotes": '2026-11-03 | student said "help me" | place | answered',
            "long theme": "2026-11-03 | " + "x" * 101 + " | place | answered",
            "two lines": GOOD + "\n" + GOOD,
        }
        for name, entry in bad.items():
            code, _, err = self.run_main(entry)
            self.assertEqual(1, code, name)
            self.assertIn("refused", err, name)
        self.assertFalse(self.log.exists())

    def test_refuses_before_gate_2(self):
        (self.course / "APPROVALS.md").write_text("", encoding="utf-8")
        code, _, err = self.run_main(GOOD)
        self.assertEqual(1, code)
        self.assertIn("not published", err)

    def test_unknown_course_is_a_usage_error(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(2, ta_log.main(["nope", GOOD, "--courses-dir", str(self.tmp)]))


class Concurrency(Base):
    def test_many_simultaneous_writers_lose_nothing(self):
        # This is the failure the script exists to prevent: parallel writers overwrote each other.
        n = 16
        procs = []
        barrier = threading.Barrier(n)

        def go(i):
            barrier.wait()
            procs.append(subprocess.run(
                [sys.executable, str(SCRIPT), "demo", f"2026-11-03 | question {i} | lab step {i} | answered",
                 "--courses-dir", str(self.tmp)], capture_output=True, text=True))

        threads = [threading.Thread(target=go, args=(i,)) for i in range(n)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertTrue(all(p.returncode == 0 for p in procs), [p.stderr for p in procs if p.returncode])
        lines = [ln for ln in self.log.read_text(encoding="utf-8").splitlines() if ln.startswith("2026-")]
        self.assertEqual(n, len(lines))
        self.assertEqual({f"question {i}" for i in range(n)}, {ln.split(" | ")[1] for ln in lines})
        self.assertEqual(1, self.log.read_text(encoding="utf-8").count("# TA log"))


if __name__ == "__main__":
    unittest.main()
