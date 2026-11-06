# Dry run 1: intro-python-lists-hs

First end-to-end run of the pipeline, on 2026-11-03. Topic: Intro to Python lists, high school,
one module. Everything is in `courses/intro-python-lists-hs/`.

## Result

The course went from request to published and through a TA question round. All three gates were
approved with plain replies: "yes, good to go" at Gate 0, "YES" at Gate 1, and "yes" at Gate 2. Each
reply is logged verbatim in `APPROVALS.md`.

| Stage | Outcome |
| --- | --- |
| Viability | GO, medium confidence. 23 claims in the source pack |
| Evidence pack | 10 more claims, 2 unsourced and declared, 7 misconception rows |
| Syllabus | 5 applied outcomes, 60 minutes, capstone `playlist.py` |
| Production | 22 slide deck, 8 item quiz with key and TA pack, 6 step lab |
| QA | 3 runs: FAIL (2 blocking), FAIL (1 blocking), PASS WITH FIXES (0 blocking) |
| TA | 4 questions: 1 answered, 3 correctly escalated or refused. Digest written |

The final script check passes with 0 blocking findings and 1 known false positive (a heading that
contains song titles). 13 PDFs for the course plus digest and QA PDFs, all current.

## How it was run

- Models: Sonnet for every agent, as requested for testing. Research pass 1 ran on Opus before that
  instruction arrived.
- The eight agents became available mid-session, so most stages ran the real agent definitions with
  their tool restrictions. The first stages used general-purpose agents told to obey the briefs.
- Cost: the subagents reported about 1.1 million tokens in total, of which the first research pass
  was about 184 thousand. Treat this as a rough figure.

## Findings

| # | Finding | Found by | Fix |
| --- | --- | --- | --- |
| 1 | Checker read every table in a module section as the topic table | Syllabus check | Read only the `Topic / Depth` table; test added |
| 2 | Worked-example check ignored diagram text and the word "spec" | Deck check | Accept both; test added |
| 3 | Checker line numbers were wrong after code fences | Deck check | Count real file lines; test added |
| 4 | A gate was opened while the research agent was still editing its brief | Late agent report | `CLAUDE.md`: wait for the agent's report before acting on its files |
| 5 | Agents' self-reported counts were wrong (920 words reported, 1,402 written) | Checker | Checker is the source of truth; research brief now says count and trim |
| 6 | Parallel deck, quiz, and lab agents need the same capstone data | Planning the stage | Architect fixes the data in the syllabus; otherwise run the lab first |
| 7 | `STYLE.md` said every lab step has the full field set, the brief and checker exempt Step 0 and the debrief | QA run 1 | `STYLE.md` corrected |
| 8 | A fix edit fused five `Covers:` lines into the notes text | Checker | Agent restored them |
| 9 | QA found blocking defects the script cannot see: a requirement that did not force the key's fix, and the same gap on a second slide | QA runs 1 and 2 | Fixed by the owners |
| 10 | Four parallel TA agents overwrote each other's log lines (2 of 4 survived) | Log inspection | `scripts/ta_log.py`, one writer, atomic appends, concurrency test |
| 11 | TA stated the planted defect's cause on its first reply | Reading the answer | TA brief: Socratic first, no defect cause on a first reply |
| 12 | TA log was treated as a document, so its PDF went stale after every question | Published check | Log is a data file: no front matter, no PDF |
| 13 | TA integrity handling and an out-of-course example (slicing) | Reading the answers | TA brief: neutral decline, name only concepts in the pack |

Things that worked as designed: the checker caught findings 2, 3, and 8 that no agent self-report
did; QA caught finding 9; the TA refused the key request containing an override injection, never
opened the key, and the digest named no student.

## Not proven yet

- **Hooks and slash commands in a live session.** They load when a session starts, and this run
  used the main session as producer without them. The stage-order guard and the `/new-course` family
  have only been tested as scripts. Open a fresh session in this folder and run `/status` first.
- **Claude Desktop.** Never run.
- **Real execution.** No lab step or starter was run. QA-4 (no captured output) was waived at
  Gate 2. Running `playlist.py` on the target Python would close it.
- **Opus quality.** Only Sonnet was tested, apart from one research pass.
- **A second course.** One topic is a small sample.

## For the human

- `scripts/ta_log.py` is not in the permission allowlist, because the session was not allowed to
  widen its own permissions. Add `Bash(python scripts/ta_log.py:*)` to `.claude/settings.json`, or
  approve the prompt the first time it runs.
- The three-round cap on QA fixes was exceeded once, for a one-word correction caused by an
  instruction. If you want a hard cap, say so.
