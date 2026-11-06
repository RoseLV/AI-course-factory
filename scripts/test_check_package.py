"""Tests for check_package.py. Run: python -m unittest scripts/test_check_package.py -v

Each test copies courses/_fixture, breaks one thing, and asserts the checker
reports the expected finding code. A mutation that changes nothing fails the test,
so a test can never pass by testing nothing.
"""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_package as cp  # noqa: E402

FIXTURE = cp.REPO / "courses" / "_fixture"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="cpkg-"))
        self.course = self.tmp / "_fixture"
        shutil.copytree(FIXTURE, self.course, ignore=shutil.ignore_patterns("dist"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def edit(self, rel, old, new, count=1):
        p = self.course / rel
        text = p.read_text(encoding="utf-8")
        self.assertIn(old, text, f"mutation target not found in {rel}")
        p.write_text(text.replace(old, new, count), encoding="utf-8", newline="\n")

    def run_check(self, through="package", pdf=False):
        return cp.check_course(self.course, through, pdf)

    def codes(self, **kw):
        return {f.code for f in self.run_check(**kw).findings}

    def assertFinds(self, code, **kw):
        found = self.codes(**kw)
        self.assertIn(code, found, f"expected {code}, got {sorted(found)}")


class FixtureIsClean(Base):
    def test_no_findings(self):
        report = self.run_check()
        self.assertEqual([], [f"{f.code} {f.path}" for f in report.findings])

    def test_metrics(self):
        m = self.run_check().metrics
        self.assertEqual(2, m["claims"])
        self.assertEqual(0, m["alignment_empty_cells"])
        self.assertEqual(6, m["decks"]["m01"]["slides"])


class Generic(Base):
    def test_em_dash(self):
        self.edit("04-labs/lab-m01.md", "Set up and verify", "Set up — and verify")
        self.assertFinds("EM-DASH")

    def test_em_dash_allowed_in_approvals(self):
        self.edit("APPROVALS.md", '"yes, good to go"', '"yes — good to go"')
        self.assertNotIn("EM-DASH", self.codes())

    def test_template_brace(self):
        self.edit("01-syllabus/syllabus.md", "FIXTURE: sample content for tooling tests.", "{topic} goes here")
        self.assertFinds("TEMPLATE-BRACE")

    def test_placeholder_text(self):
        self.edit("qa/qa-report.md", "None.", "TBD")
        self.assertFinds("PLACEHOLDER-TEXT")

    def test_front_matter_missing_key(self):
        self.edit("qa/qa-report.md", "author: qa-reviewer\n", "")
        self.assertFinds("FRONT-MATTER")

    def test_front_matter_wrong_course(self):
        self.edit("qa/qa-report.md", "course: _fixture", "course: other")
        self.assertFinds("FRONT-MATTER")

    def test_status_length(self):
        p = self.course / "STATUS.md"
        p.write_text(p.read_text(encoding="utf-8") + "\nx" * 70, encoding="utf-8")
        self.assertFinds("STATUS-LENGTH")

    def test_heading_case(self):
        self.edit("01-syllabus/syllabus.md", "## Out of scope", "## Out Of Scope Items Here")
        self.assertFinds("HEADING-CASE")


class Manifest(Base):
    def test_missing_lab(self):
        (self.course / "04-labs/lab-m01.md").unlink()
        self.assertFinds("MANIFEST-MISSING")

    def test_through_viability_ignores_later_stages(self):
        for d in ("01-syllabus", "02-deck", "03-assessments", "04-labs", "qa"):
            shutil.rmtree(self.course / d)
        report = self.run_check(through="viability")
        self.assertEqual([], [f"{f.code} {f.path}" for f in report.findings])

    def test_through_production_does_not_need_qa(self):
        shutil.rmtree(self.course / "qa")
        self.assertEqual([], [f.code for f in self.run_check(through="production").findings])

    def test_published_needs_manifest(self):
        self.assertFinds("MANIFEST-MISSING", through="published")


class Syllabus(Base):
    def test_budget_does_not_sum(self):
        self.edit("01-syllabus/syllabus.md", "Total 35 min", "Total 40 min")
        self.assertFinds("TIME-BUDGET")

    def test_no_practise_topic(self):
        self.edit("01-syllabus/syllabus.md", "| practise |", "| explain |", count=2)
        self.assertFinds("DEPTH-MARK")

    def test_extra_table_in_module_section_is_not_a_topic_table(self):
        self.edit("01-syllabus/syllabus.md", "**Assessment:** quiz-m01. **Lab:** lab-m01.",
                  "| Item | Outcome | Difficulty |\n| --- | --- | --- |\n| Q1 | LO-2 | basic |\n\n"
                  "**Assessment:** quiz-m01. **Lab:** lab-m01.")
        self.assertNotIn("DEPTH-MARK", self.codes())

    def test_invalid_depth(self):
        self.edit("01-syllabus/syllabus.md", "| mention |", "| skim |")
        self.assertFinds("DEPTH-MARK")

    def test_too_few_outcomes(self):
        self.edit("01-syllabus/syllabus.md", "| LO-3 | Explain why `>` and `>=` give different results at the boundary | no |\n", "")
        self.assertFinds("OUTCOMES-COUNT")

    def test_lo1_not_applied(self):
        self.edit("01-syllabus/syllabus.md", "by score | yes |", "by score | no |")
        self.assertFinds("OUTCOMES-APPLIED")

    def test_alignment_row_missing(self):
        self.edit("01-syllabus/syllabus.md", "| LO-3 | M01 | Boundary values | Q2, Q4 | step 2 |\n", "")
        self.assertFinds("SYLLABUS-ALIGNMENT")


class Decks(Base):
    def test_five_bullets(self):
        self.edit("02-deck/deck-m01.md", "- End: a list of passing students\n",
                  "- End: a list of passing students\n- One\n- Two\n- Three\n")
        self.assertFinds("SLIDE-BULLETS")

    def test_long_bullet(self):
        self.edit("02-deck/deck-m01.md", "- Start: a table of grades", "- Start: a table of grades with a great many extra words")
        self.assertFinds("SLIDE-BULLET-WORDS")

    def test_missing_covers(self):
        self.edit("02-deck/deck-m01.md", "Covers: LO-1\n\n## Slide 2", "\n## Slide 2")
        self.assertFinds("SLIDE-COVERS")

    def test_unknown_outcome(self):
        self.edit("02-deck/deck-m01.md", "Covers: LO-1\n\n## Slide 2", "Covers: LO-9\n\n## Slide 2")
        self.assertFinds("OUTCOME-UNKNOWN")

    def test_placeholder_visual(self):
        p = self.course / "02-deck/deck-m01.md"
        text = p.read_text(encoding="utf-8")
        start = text.index("```svg")
        end = text.index("```", start + 6) + 3
        p.write_text(text[:start] + text[end:], encoding="utf-8", newline="\n")
        self.assertFinds("VISUAL-PLACEHOLDER")

    def test_missing_visual_src(self):
        self.edit("02-deck/deck-m01.md", "Visual: Three rows pass", "Visual-src: assets/none.png\nVisual: Three rows pass")
        self.assertFinds("VISUAL-MISSING")

    def test_svg_without_viewbox(self):
        self.edit("02-deck/deck-m01.md", '<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">\n  <rect x="30" y="80"',
                  '<svg xmlns="http://www.w3.org/2000/svg">\n  <rect x="30" y="80"')
        self.assertFinds("SVG-VIEWBOX")

    def test_svg_script(self):
        self.edit("02-deck/deck-m01.md", "</svg>", "<script>1</script></svg>")
        self.assertFinds("SVG-FORBIDDEN")

    def test_svg_literal_colour(self):
        self.edit("02-deck/deck-m01.md", '<rect x="30" y="80" width="200"', '<rect fill="#ff0000" x="30" y="80" width="200"')
        self.assertFinds("SVG-COLOUR")

    def test_short_notes(self):
        self.edit("02-deck/deck-m01.md", "Notes: A WHERE clause is a test", "Notes: Short. A test")
        p = self.course / "02-deck/deck-m01.md"
        text = p.read_text(encoding="utf-8")
        i = text.index("Notes: Short.")
        j = text.index("Covers:", i)
        p.write_text(text[:i] + "Notes: Far too short.\n" + text[j:], encoding="utf-8", newline="\n")
        self.assertFinds("NOTES-LENGTH")

    def test_narration_gap(self):
        self.edit("01-syllabus/syllabus.md", "Narration word budget: 650", "Narration word budget: 1300")
        self.assertFinds("TIME-BUDGET")  # 1300 is not 5 x 130
        self.assertFinds("NARRATION-GAP")

    def test_unresolved_citation(self):
        self.edit("02-deck/deck-m01.md", "(SP-1.2)", "(SP-9.99)")
        self.assertFinds("SP-UNRESOLVED")

    def test_missing_mechanism_slide(self):
        self.edit("02-deck/deck-m01.md", "## Slide 2: Mechanism: a WHERE", "## Slide 2: How a WHERE")
        self.assertFinds("DECK-REQUIRED")

    def test_worked_example_without_requirement(self):
        self.edit("02-deck/deck-m01.md", "-- Requirement (the teacher's request): students with a score over 60", "-- students with a score over 60")
        self.edit("02-deck/deck-m01.md", "- Requirement: scores over 60 pass", "- Scores over 60 pass")
        self.assertFinds("WORKED-EXAMPLE-SOURCE")

    def test_worked_example_requirement_may_be_called_a_spec(self):
        self.edit("02-deck/deck-m01.md", "- Requirement: scores over 60 pass", "- Spec: scores over 60 pass")
        self.edit("02-deck/deck-m01.md", "-- Requirement (the teacher's request): students with a score over 60",
                  "-- students with a score over 60")
        self.assertNotIn("WORKED-EXAMPLE-SOURCE", self.codes())

    def test_worked_example_requirement_may_sit_in_the_diagram_text(self):
        # Slide 2 stands in for a worked example here: retitle it and move the words into its diagram.
        self.edit("02-deck/deck-m01.md", "## Slide 3: Worked example:", "## Slide 3: Result:")
        self.edit("02-deck/deck-m01.md", "## Slide 2: Mechanism: a WHERE", "## Slide 2: Worked example: a WHERE")
        self.edit("02-deck/deck-m01.md", '<text x="435" y="245" text-anchor="middle" class="label label-strong">WHERE</text>',
                  '<text x="435" y="245" text-anchor="middle" class="label label-strong">Spec: WHERE</text>')
        found = [f for f in self.run_check().findings if f.code == "WORKED-EXAMPLE-SOURCE"]
        self.assertEqual([], found)

    def test_heading_line_numbers_are_real_file_lines(self):
        self.edit("01-syllabus/syllabus.md", "## Out of scope", "## Out Of Scope Items Here")
        lines = (self.course / "01-syllabus/syllabus.md").read_text(encoding="utf-8").splitlines()
        want = next(i for i, ln in enumerate(lines, 1) if ln.startswith("## Out Of Scope"))
        hits = [f for f in self.run_check().findings if f.code == "HEADING-CASE"]
        self.assertEqual(f"01-syllabus/syllabus.md:{want}", hits[0].path)

    def test_three_abstract_slides_in_a_row(self):
        self.edit("02-deck/deck-m01.md", "Diagnostic sequence: a missing", "A missing")
        self.edit("02-deck/deck-m01.md", "(SP-1.2)", "")
        self.assertFinds("DECK-DENSITY")

    def test_code_too_long(self):
        lines = "\n".join(f"SELECT {i};" for i in range(13))
        self.edit("02-deck/deck-m01.md", "SELECT name, score FROM grades WHERE score > 60;", lines)
        self.assertFinds("CODE-LENGTH")


class Assessments(Base):
    def test_missing_key_entry(self):
        p = self.course / "03-assessments/instructor/quiz-m01-key.md"
        text = p.read_text(encoding="utf-8")
        i = text.index("## Q3 - Answer")
        j = text.index("## Q4 - Answer")
        p.write_text(text[:i] + text[j:], encoding="utf-8", newline="\n")
        self.assertFinds("KEY-MISSING")

    def test_orphan_key_entry(self):
        p = self.course / "03-assessments/instructor/quiz-m01-key.md"
        p.write_text(p.read_text(encoding="utf-8") + "\n## Q99 - Answer: A\n", encoding="utf-8", newline="\n")
        self.assertFinds("KEY-ORPHAN")

    def test_key_answer_not_an_option(self):
        self.edit("03-assessments/instructor/quiz-m01-key.md", "## Q1 - Answer: B", "## Q1 - Answer: E")
        self.assertFinds("KEY-ANSWER")

    def test_missing_distractor_line(self):
        self.edit("03-assessments/instructor/quiz-m01-key.md", "- C: a student choosing this confuses sorting with filtering.\n", "")
        self.assertFinds("KEY-DISTRACTOR")

    def test_seven_items(self):
        p = self.course / "03-assessments/student/quiz-m01.md"
        text = p.read_text(encoding="utf-8")
        i = text.index("## Question 8")
        j = text.index("## Predict and reflect")
        p.write_text(text[:i] + text[j:], encoding="utf-8", newline="\n")
        self.assertFinds("QUIZ-COUNT")

    def test_unknown_outcome_in_item(self):
        self.edit("03-assessments/student/quiz-m01.md", "item: Q1 | outcome: LO-2", "item: Q1 | outcome: LO-9")
        self.assertFinds("OUTCOME-UNKNOWN")

    def test_bad_difficulty(self):
        self.edit("03-assessments/student/quiz-m01.md", "difficulty: stretch", "difficulty: hard")
        self.assertFinds("QUIZ-TAGS")

    def test_no_predict_reflect(self):
        self.edit("03-assessments/student/quiz-m01.md", "**Predict.**", "Predict:")
        self.assertFinds("QUIZ-PREDICT")

    def test_instructor_reference_in_student_file(self):
        self.edit("03-assessments/student/quiz-m01.md", "Answer every question.", "Answer every question. See instructor/ for hints.")
        self.assertFinds("WALL-LEAK")

    def test_ta_pack_answer_leak(self):
        p = self.course / "03-assessments/instructor/ta-feedback-pack-m01.md"
        p.write_text(p.read_text(encoding="utf-8") + "\nQ2 Answer: B\n", encoding="utf-8", newline="\n")
        self.assertFinds("TA-ANSWER-LEAK")


class Labs(Base):
    def test_time_sum_over(self):
        self.edit("04-labs/lab-m01.md", "**Time:** 8 minutes", "**Time:** 12 minutes")
        self.assertFinds("LAB-TIME-SUM")

    def test_time_sum_far_under(self):
        self.edit("04-labs/lab-m01.md", "**Time:** 8 minutes", "**Time:** 1 minutes")
        self.assertFinds("LAB-TIME-SUM")

    def test_missing_debrief(self):
        self.edit("04-labs/lab-m01.md", "### Step 3 - Debrief", "### Step 3 - Wrap up")
        self.assertFinds("LAB-STEPS")

    def test_step_missing_field(self):
        self.edit("04-labs/lab-m01.md", "**Recovery:** If you see an error, check the semicolon and the column names.\n", "")
        self.assertFinds("LAB-STEP-FIELDS")

    def test_no_planted_defect(self):
        self.edit("04-labs/lab-m01.md", "**Planted defect:**", "**Defect note:**")
        self.assertFinds("LAB-DEFECT")

    def test_no_troubleshooting(self):
        self.edit("04-labs/lab-m01.md", "## Troubleshooting", "## Notes")
        self.assertFinds("LAB-TROUBLESHOOTING")

    def test_long_step_zero(self):
        self.edit("04-labs/lab-m01.md", "**Time:** 5 minutes", "**Time:** 15 minutes")
        self.assertFinds("LAB-STEP0")


class Qa(Base):
    def test_empty_alignment_cell(self):
        self.edit("qa/alignment-matrix.md", "m01 Q3, Q7", "")
        self.assertFinds("ALIGN-EMPTY")

    def test_missing_alignment_row(self):
        self.edit("qa/alignment-matrix.md", "| LO-3 | m01 slides 3, 4, 6 | m01 Q2, Q4, Q8 | m01 step 2 |\n", "")
        self.assertFinds("ALIGN-MISSING")

    def test_ta_manifest_lists_instructor_key(self):
        shutil.copy(cp.REPO / "templates" / "ta-grounding-manifest.md", self.course / "qa" / "ta-grounding-manifest.md")
        p = self.course / "qa/ta-grounding-manifest.md"
        text = p.read_text(encoding="utf-8").replace("{slug}", "_fixture")
        text = text.replace("{YYYY-MM-DD}", "2026-11-03")
        text += "\n- `courses/_fixture/03-assessments/instructor/quiz-m01-key.md`\n"
        p.write_text(text, encoding="utf-8", newline="\n")
        self.assertFinds("TA-MANIFEST", through="published")


class SourcePack(Base):
    def test_missing_mechanism(self):
        self.edit("00-viability/source-pack.md", "- **Mechanism:** The database sorts the result set by the named column after filtering, in descending order when `DESC` is given.\n", "")
        self.assertFinds("SP-FIELD")

    def test_source_without_url(self):
        self.edit("00-viability/source-pack.md", "- **Source:** https://www.sqlite.org/lang_select.html, the ORDER BY clause section", "- **Source:** the docs")
        self.assertFinds("SP-SOURCE")

    def test_duplicate_id(self):
        self.edit("00-viability/source-pack.md", "### SP-1.2", "### SP-1.1")
        self.assertFinds("SP-DUPLICATE")

    def test_brief_without_verdict(self):
        self.edit("00-viability/viability-brief.md", "GO. Confidence", "Probably fine. Confidence")
        self.assertFinds("BRIEF-VERDICT")


class Pdfs(Base):
    def make_pdfs(self):
        dist = self.course / "dist"
        for p in self.course.rglob("*.md"):
            rel = p.relative_to(self.course)
            if rel.parts[0] == "dist":
                continue
            if rel.parts[0] == "02-deck":
                outs = [dist / "02-deck" / f"{p.stem}.pdf", dist / "02-deck" / f"{p.stem}-instructor.pdf"]
            else:
                outs = [dist / rel.with_suffix(".pdf")]
            for out in outs:
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(b"%PDF-1.4 fake")
                os.utime(out, (p.stat().st_mtime + 10, p.stat().st_mtime + 10))

    def test_missing(self):
        self.assertFinds("PDF-MISSING", pdf=True)

    def test_all_present_is_clean(self):
        self.make_pdfs()
        self.assertEqual([], [f"{f.code} {f.path}" for f in self.run_check(pdf=True).findings])

    def test_stale(self):
        self.make_pdfs()
        p = self.course / "01-syllabus/syllabus.md"
        os.utime(p, (p.stat().st_mtime + 60, p.stat().st_mtime + 60))
        self.assertFinds("PDF-STALE", pdf=True)

    def test_deck_needs_both_pdfs(self):
        self.make_pdfs()
        (self.course / "dist/02-deck/deck-m01-instructor.pdf").unlink()
        self.assertFinds("PDF-MISSING", pdf=True)


class DataFiles(Base):
    def add_log(self):
        d = self.course / "maintenance"
        d.mkdir(exist_ok=True)
        (d / "ta-log.md").write_text("# TA log\n\ndate | theme | where | outcome\n2026-11-03 | t | p | answered\n",
                                     encoding="utf-8")

    def test_ta_log_needs_no_front_matter(self):
        self.add_log()
        self.assertNotIn("FRONT-MATTER", self.codes())

    def test_ta_log_needs_no_pdf(self):
        self.add_log()
        pdfs = Pdfs.make_pdfs  # reuse the helper that fabricates every expected PDF
        pdfs(self)
        self.assertFalse(any(f.path.endswith("ta-log.md") for f in self.run_check(pdf=True).findings))


class Cli(Base):
    def test_exit_codes(self):
        base = ["_fixture", "--no-pdf", "--courses-dir", str(self.tmp)]
        self.assertEqual(0, cp.main(base))
        self.edit("04-labs/lab-m01.md", "Set up and verify", "Set up — and verify")
        self.assertEqual(1, cp.main(base))
        self.assertEqual(2, cp.main(["nope", "--courses-dir", str(self.tmp)]))


if __name__ == "__main__":
    unittest.main()
