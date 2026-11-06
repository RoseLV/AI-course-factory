---
course: intro-python-lists-hs
stage: qa
module: n/a
author: qa-reviewer
date: 2026-11-03
outcomes: all
---

# QA report: intro-python-lists-hs

## Verdict

PASS WITH FIXES

Script checker: pass, 0 blocking findings, 1 minor (HEADING-CASE at `02-deck/deck-m01.md:276`, a false positive, QA-13). Blocking issues: 0. Minor: 2 open (QA-4, QA-13).
Previous run (run 2): FAIL, 1 blocking (QA-14), 3 minor (QA-15, QA-4, QA-13), empty alignment cells 0, 0 of 14 claims flagged, longest abstract run 2, narration gap -0.03 min.

QA-14 and QA-15 are closed. Run 3 is a fresh pass over the current files. The one open item that needs a person is QA-4 (no captured output in the quiz): a human run of the starter, or a Gate 2 waiver.

## Numbers

| Measure | This run | Previous |
| --- | --- | --- |
| Empty alignment cells | 0 | 0 |
| Uncited claims out of sampled | 0 out of 14 sampled (0 uncited, 0 mismatched) | 0 out of 14 |
| Longest abstract slide run, per deck | m01: 2 (script figure) | m01: 2 |
| Narration gap per module, minutes | m01: -0.02 (2337 words against a 2340 budget, under budget) | m01: -0.03 (2335 against 2340) |

## Issues

| ID | Location | Severity | Description | Owner |
| --- | --- | --- | --- | --- |
| QA-4 | `03-assessments/student/quiz-m01.md` Q5 and Q7 | minor | Open, unchanged. The syllabus contract says Q5 must use output someone captured by running the starter. Q5 describes the screen in words and Q7 shows a hand-traced output labelled as such. No item shows captured output. Needs a human run of the starter, or a Gate 2 waiver. | human (Gate 2) |
| QA-13 | `02-deck/deck-m01.md:276` | minor | Script HEADING-CASE flag. Slide 16's title holds song titles, which are proper nouns. No fix needed. Recorded so the script rule can be tuned. | none |

Closed this run: QA-14 (slide 11 now carries "Spec: titles fixed; four songs remain, no error", and its notes now say only the lab's four starting titles hold Blue Window), QA-15 (Source line on slides 10, 11, 12 now reads "Source: lab's starting titles and expected output", which matches lab Step 3). Closed earlier: QA-1 to QA-3, QA-5 to QA-12.

## Judgment checks

1. **Alignment:** Matrix at `qa/alignment-matrix.md`, rebuilt. Five outcomes, every cell filled, empty cells 0. No orphan slides or items. Lab Step 0 covers no outcome by design. The `mention` topic (slide 18) has no lab step or quiz item.

2. **Claim spot check:** 14 sampled, 14 supported, 0 flagged. The edits since run 2 touched no cited claim, so the run 2 sample stands, re-read against the current deck.
   - Slide 2, SP-0.12, CSTA 3A-AP-14, one list for repeated variables: supported.
   - Slide 4, SP-1.1, first index is 0: supported.
   - Slide 5, SP-1.3, `len()` is 4 for four songs: supported.
   - Slide 6, SP-1.2, index 4 raises `IndexError`: supported.
   - Slide 7, SP-1.4 and SP-0.6: supported.
   - Slide 9, SP-0.6 and SP-1.5, `remove()` by value, first match, `ValueError`: supported.
   - Slide 9 notes, SP-1.8, songs behind the removal shift left, labelled secondary: supported.
   - Slide 13, SP-0.5 and SP-1.6, items in order: supported.
   - Slide 18, SP-1.8, skip trap: supported.
   - Lab Context SP-0.12, tooling SP-0.1, SP-0.2 and SP-0.3, Step 0 SP-0.14: supported.

3. **Worked example soundness:**
   - **Slide 10, failing starter.** Requirement on the page, bullet 1: "Spec: titles fixed; four songs remain, no error". Source named on the page: "lab's starting titles and expected output", a written specification, which matches lab Step 3. Worked out: `remove("Blue Windows")` matches no item (exact equality, one extra letter), so a `ValueError` is raised on that line and neither print runs. The verdict that the starter fails the spec follows. Boundary: exact string equality, one letter off. The slide names the error type and line only and gives no message text (SP-U1 disclosed). Pass. A small wording point, not a finding: the notes say "The spec, the lab's expected-output block, wants four songs", which names only one of the two source parts that the bullet names.
   - **Slide 11, diagnostic sequence (QA-14).** Requirement on the page, bullet 1: "Spec: titles fixed; four songs remain, no error". Source bullet 2 names the starting titles and the expected output. Worked out: with titles fixed, the list cannot be the side that changes, so an extra `s` in the name is the defect, and the only fix is correcting the name. Editing the list to "Blue Windows" would break "titles fixed", and now the slide says so. The verdict follows. Notes: "The spec says titles are fixed, and the lab's four starting titles include Blue Window, so the list is right" is accurate; the expected-output block is no longer said to hold Blue Window. Boundary: exact equality, extra `s`. No message text. Pass.
   - **Slide 11, merged bullets still teach symptom, check, conclusion.** Bullets: Spec, Source, "Symptom: no output, error type ValueError", "Check: letter by letter finds an extra s". The conclusion is no longer a bullet but is on the slide in the SVG Conclusion box ("extra s in the name, fix the name only", "Ruled out: misspelled list, a different failing line"), in the title ("point at the name"), and in the notes, whose three-cause walk ends "Conclusion: correct the name in remove and leave the list alone." The sequence is intact in order: symptom, check, conclusion. Pass. Observation only: the conclusion lives in the visual and notes, not a bullet, so a student reading bullets alone sees symptom and check.
   - **Slide 12, corrected run.** Requirement on the page: "Spec: titles fixed; four songs remain, no error", source named. Five items after append, four after remove, first song Sunrise Walk, output `Songs: 4` and `First song: Sunrise Walk`. Verdict follows. Notes honestly say the pass does not prove the right song left. Pass.
   - **Slide 17, counter designs.** Requirement on the page: "Specification: the numbers run 1 to 4". Traced: start 0 add after gives 0 to 3, start 1 add before gives 2 to 5, start 1 add after gives 1 to 4. Verdicts follow, boundary 0 against 1 checked. Pass.
   - **Slide 20, finished file against the output.** Requirement on the page: six-line expected block, "Spec: the lab's expected-output block, six lines". Verdict "predicted to match; the lab run confirms" and the slide says the right column is a hand trace. Traced: four items plus one minus one is four, first song Sunrise Walk, numbers 1 to 4. Pass.
   - **Quiz Q1 to Q8.** Unchanged since run 2 and not touched by this resubmission. Q5 states its requirement on the page (starting titles may not be edited, must add "Garden Song" and remove "Blue Window" by name, no error), and the only change that meets every clause is correcting the name in the remove line. Q4, Q6, Q7, Q8 verdicts follow from stated facts. Q7 boundary 0 against 1 decides the answer. Pass.
   - **Lab Step 3 and Step 4.** Planted defect, requirement ("two parts": the four starting titles and the expected-output block), and source of truth are stated before any run (lab lines 64 to 68, 263). Starter comment ordering means nothing prints until Step 3 is live, consistent with Evidence. Step 4 Interpretation (a counter starting at 0 and added before the print also gives 1 to 4) is correct. Pass.
   - **Slides 10 to 12 as a set.** The same requirement and the same two-part source appear on all three, so the failure (slide 10), the diagnosis (slide 11), and the repair (slide 12) judge against one spec. No ValueError message text appears anywhere in the deck, lab, or student quiz (searched for the message wording, no matches). Pass.

4. **Depth marks bind:** Three topics checked. `mention` (removal in a loop): no lab step, no quiz item, listed in lab Step 5 as not covered. `practise` "Debug the ValueError from remove()": Step 3 and Q5 both do it. `practise` "Print every song numbered": Step 4 does it. Pass.

5. **Level fit:** Slide 7 notes explain `None` as "nothing was handed back" with a concrete wrong answer, which fits grades 9 to 10. Slide 15 notes build the counter from the learner's known `count = count + 1` and trace pass one, which fits. Slide 11 notes walk three causes in plain words and rule out two with a fact each, which fits. Slide 2 bullet 4 "CSTA 3A-AP-14 asks for this" means little to a 14 year old; a small mismatch, not a finding.

6. **Vocabulary:** Against the syllabus prerequisites (print, variables, indented blocks, error line numbers, `count = count + 1`): "loop" is defined on slide 2 at first use, "specification" in slide 1 notes, and "string", "function", "method", "comment", "None", "in place", "counter", "error type" each at first use. The edits since run 2 add no new term. No finding.

7. **Notes substance:** Six notes sampled across the deck.
   - Slide 7: "The common wrong answer is x = songs.append("Garden Song"), then expecting x to hold the list. It holds None." Supplies what students get wrong, plus how to judge.
   - Slide 10: "Many learners predict that the prints still show; ask the room to commit to an answer first." Supplies what students get wrong.
   - Slide 11: "The spec says titles are fixed, and the lab's four starting titles include Blue Window, so the list is right, and cause two fails." Supplies why the diagnosis is true and how to judge it. Now accurate.
   - Slide 12: "This pass proves remove matched by value. It does not prove the right song left, only that the count fell by one." Supplies how to judge and the limit of the check.
   - Slide 16: "The line number = 1 sits above the for line, so it runs once; inside the loop it would reset on every pass and print 1 four times." Supplies why it is true and a named wrong output.
   - Slide 20: "A leftover setup ok line, or a first line numbered 0, would fail." Supplies how to judge.

8. **Capstone continuity:** Pass. Seven of eight quiz items name `playlist.py` or the playlist, and Q8 is the declared transfer item. The lab starts from the starter (prints `setup ok`) and each Starting state matches the prior step's end. The syllabus end state, the lab expected output, slide 20, the lab finished file, and slide 19 describe the same six-line artifact.

9. **Student and instructor wall:** Pass. Searched the deck, lab, student quiz, and syllabus for "instructor", "quiz-m01-key", "ta-feedback", and "answer key": no matches (unchanged files, rechecked after the slide 11 edit). The TA feedback pack contains no literal answers, solutions, or answer letters.

10. **Unexecuted labs:** Pass. All six steps carry "Unexecuted teaching sample: no one has run this step." Evidence blocks read as expected results, and none is presented as captured. The SP-U1 message text is quoted nowhere. QA-4 remains the open consequence of this.

## What I did not check

I did not run the starter or any lab step. All output judgements come from reading the code and tracing it by hand. Script-owned checks (manifest, PDFs, em dashes, bullet and notes limits including slide 11's four bullets, citation resolution) were taken from the script output, not repeated; I confirmed by search that no em or en dashes are present in the student-visible files. The narration figure is the script's count (2337 words). The PDFs in `dist/` were not re-inspected; the script owns that check.
