# House style

Applies to every artifact. Agents read this before writing. `scripts/check_package.py` checks
the mechanical rules, and qa-reviewer checks the rest. A rule marked MUST blocks a package.

## Voice

- Clear, direct, warm, professional. Confident without hype.
- Write for the declared audience level. High school: short sentences, concrete examples before
  abstractions. Undergraduate: two or three concepts per session. Professional: outcome first,
  real constraints, less scaffolding.
- MUST define every technical term at first use, at every level. The syllabus prerequisites are
  the only place a course may declare a term already known.
- Active voice. "The agent reads the file", not "the file is read".

## Mechanics

- MUST NOT use em dashes anywhere. Use a comma, colon, parenthesis, or a new sentence.
- Sentence case for headings and slide titles.
- Oxford comma. One space after periods.
- Numbers one through nine spelled out in prose. Numerals in tables, code, and data.
- Sentences under 25 words where possible. No idioms or wordplay in instructional text.
- Numbered steps for every procedure, one action per step.

## Course shape

- MUST: the majority of course outcomes are applied, meaning the learner does or makes
  something. LO-1 names the capstone artifact the learner ships.
- MUST: one capstone artifact for the whole course, with an end state someone other than the
  learner can check.
- MUST NOT: setup is never a module and never an outcome. It is Step 0 of the first lab, five
  to ten minutes.
- At most one outcome may be about a tool alone.
- Every outcome has an ID, `LO-1`, `LO-2`, and starts with a measurable verb. Never
  "understand" or "know".
- Every topic carries a depth mark and minutes: `mention` (one slide at most, no exercise),
  `explain` (mechanism and worked example), `practise` (the learner does it in the lab).
  Every outcome has at least one `practise` topic.

## Sources and claim IDs

- Claims live in `00-viability/source-pack.md`. Each has an ID `SP-<module>.<n>` (module 0 is for
  course-level viability claims), a one-sentence
  checkable claim, the mechanism (why it is true), a source URL, and the date you opened it.
- MUST: never cite a source you did not open. Never invent a statistic, URL, or quote.
- IDs are allocated once and never renumbered or reused. A withdrawn claim keeps its ID and gains
  `[RETIRED]`. A claim with no source goes in the `SP-U` series and stays visible.
- Quote under 25 words from any one source. Paraphrase the rest.
- Any claim about behaviour, a version, a limit, a price, or a number a student would repeat
  carries its `SP-` ID, on the slide if it is the point, otherwise in the notes.
- Gaps are declared, not filled from memory. A thin honest document beats a full invented one.

## Slides

Schema, one block per slide, in `deck-mNN.md`:

```
## Slide 3: The title is a full sentence stating the idea
- Bullet, maximum four per slide, maximum eight words each
Visual: one sentence saying what the visual shows
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">...</svg>
```
Notes: 80 to 150 words, written to be spoken aloud.
Covers: LO-1
```

- 16:9. One idea per slide. Code on a slide: at most 12 lines.
- Every slide has `Covers:` naming real outcome IDs.
- Every `Visual:` has a drawn SVG or a `Visual-src:` file that exists. A visual with neither is
  an unfinished placeholder and blocks.
- A slide whose content is a code block carries the code and omits the `Visual:` line. The
  renderer shows fenced code on the slide, and a `Visual:` line with no drawing would flag it as
  a placeholder.
- SVG: always a `viewBox` and no width or height. Bullets present: `0 0 800 500`. No bullets:
  `0 0 1200 420`. No scripts, external images, web fonts, or `foreignObject`. Use only the class
  vocabulary: fills `fill-ink fill-muted fill-faint fill-accent fill-panel fill-code fill-slide
  fill-none`, strokes `stroke-ink stroke-muted stroke-rule stroke-accent stroke-none dashed`,
  shapes `box box-accent box-solid connector connector-accent`, text `label label-lg label-sm
  label-mono label-strong`, arrows `url(#arrow)`, `url(#arrow-accent)`, `url(#arrow-muted)`.
  Never write a literal colour.
- A diagram earns its space by showing a mechanism. Six or seven boxes is busy. One accent per
  diagram.
- Every module deck MUST carry one mechanism explanation (why, not only what), one complete worked
  example (input, command, real output, verdict, nothing elided), and one diagnostic sequence
  (symptom, the check that separates the causes, the conclusion). Label all three on their slides.
- MUST NOT: three consecutive slides carrying only definitions, lists, or abstract diagrams.
- Notes MUST explain why the claim holds and how a student judges it. Notes that restate the
  bullets are a defect.
- Every deck ends with a glossary slide: term, one plain sentence, first slide it appears on.
- Real interface or product output: use a capture the course supplies, or label the drawing
  "reconstruction, not a capture" inside the visual itself.

## Assessments

- A quiz has 8 to 12 items. Roughly half basic, a third standard, the rest stretch.
- Every item is tagged in a comment: `<!-- item: Q1 | outcome: LO-1 | difficulty: basic -->`.
- Test only topics marked explain or practise.
- No trick questions. Every item is answerable from course material alone.
- Distractors are plausible wrong answers a real learner would give. The key gives one line per
  distractor on the misconception behind it.
- At least half the items name the capstone artifact or the module's running case.
- Each quiz has one item that shows real output and asks the learner to judge it, one transfer
  item in a new context (marked stretch), and a predict prompt and a reflect prompt for any
  hands-on step. Prediction accuracy is never graded.
- Instruments are for human grading. Never imply an agent grades.

## Labs

- Title names the skill, not "Lab 1".
- Step 0 is environment setup, five minutes. The last step is `### Step N - Debrief`.
- Every step except Step 0 and the debrief has: Purpose, Time in minutes, Starting state, Task,
  Prediction, Action, Evidence (expected passing and failing output), Interpretation, Recovery,
  Why this matters. Step 0 and the debrief carry Purpose and Time and follow their own formats.
- Step times sum to the module's hands-on minutes in the syllabus.
- Plant at least one defect, and state the requirement it violates before the learner runs
  anything.
- The deliverable names something that runs or can be inspected, never "the tool configured".
- Labs are written, not executed. Every step that no one ran carries this visible note:
  `Unexecuted teaching sample: no one has run this step.` Never present a guess as output.
- A troubleshooting table closes the lab: symptom, cause, fix.
- No secrets, tokens, or real credentials anywhere.

## Worked examples

A worked example is any passage that judges something right or wrong: a diff and a verdict, a
failing test, a before and after, a quiz item with a right answer.

- MUST state the source of truth before the evidence, on the page and not only in the notes. It
  is one of four: the user's request, a written specification, a disclosed test suite, or a later
  correction from the user.
- MUST NOT let the verdict contradict the stated requirement. If the rule says "over 100", then
  exactly 100 does not qualify, and code that excludes 100 is correct.
- Check boundaries (`>` against `>=`, inclusive against exclusive) with extra care.

## Student and instructor wall

- `03-assessments/student/` and `dist/03-assessments/student/` are what students see.
- `03-assessments/instructor/` holds keys, rubrics, and TA feedback packs. MUST NOT be linked,
  quoted, or copied into anything student-visible, and instructor PDFs carry an "Instructor only"
  ribbon.
- TA feedback packs contain rubric criteria and misconception explanations only. Zero literal
  answers. Write them assuming a student will eventually read them.

## Front matter

Every markdown artifact starts with:

```
---
course: {slug}
stage: {00-viability | 01-syllabus | 02-deck | 03-assessments | 04-labs | qa | maintenance}
module: {NN or n/a}
author: {agent name}
date: {YYYY-MM-DD}
outcomes: {LO ids covered, or n/a}
---
```

Deck front matter is authoring metadata only and does not reach the PDF. Put anything an
instructor must see on a slide.

## Agent final report

Every agent ends its run with this block, so the producer can act on it:

```
DONE: what was produced, one line
PATHS: files written
COUNTS: the numbers the brief asks for
GAPS: anything declared missing or unverified
NEEDS A HUMAN: decisions only a person can make, or "nothing"
```

## Files and naming

- Slug: topic plus level, kebab-case, for example `intro-sql-hs`.
- Modules are zero padded: `deck-m01.md`, `quiz-m01.md`, `quiz-m01-key.md`, `lab-m01.md`.
- Markdown is the master. A PDF is a build artifact in `courses/{slug}/dist/`. Never edit a PDF.
- An agent writes only inside its own folder.
