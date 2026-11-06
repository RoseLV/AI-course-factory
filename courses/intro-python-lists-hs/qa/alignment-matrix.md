---
course: intro-python-lists-hs
stage: qa
module: n/a
author: qa-reviewer
date: 2026-11-03
outcomes: all
---

# Alignment matrix

Every cell names a specific slide range, item IDs, or lab steps. An empty cell is blocking.
Run 3, rebuilt from the current files.

| Outcome | Deck | Quiz | Lab |
| --- | --- | --- | --- |
| LO-1 | m01 slides 1 to 3 (goal, why a list, the starter), slide 19 (finished file), slide 20 (worked example against the expected output), slides 21 and 22 (capstone state, glossary) | m01 Q8 (transfer: same build for a homework list) | m01 Step 5 (full run against the expected-output block); Steps 1 to 4 build the file |
| LO-2 | m01 slides 4 to 6 (zero-based index, `len()` with `songs[0]`, `IndexError`) | m01 Q1, Q2 | m01 Step 1 (count and first song; the `IndexError` case is in its Evidence) |
| LO-3 | m01 slides 7 to 10 (`append()` mechanism, order of lines, `remove()` by value, the failing starter line), slide 12 (corrected run), slide 18 (loop-removal trap, mention depth only) | m01 Q3, Q4 | m01 Step 2 (`append()`), Step 3 (`remove()`) |
| LO-4 | m01 slides 13 to 17 (loop variable, printing items, counter idea, numbered loop, counter-design comparison) | m01 Q6, Q7 | m01 Step 4 (numbered loop and counter) |
| LO-5 | m01 slides 10 to 12 (failing run, diagnostic sequence with spec and source on the page, corrected run), slide 21 (capstone state, name fixed not list) | m01 Q5 | m01 Step 3 (turn on the starter line, read the error, fix the name) |

## Orphans

Slides that cover no outcome: none. Every slide carries a `Covers:` line naming real IDs.

Quiz items that cover no outcome: none. All eight carry an outcome tag that matches the syllabus quiz contract (Q1 LO-2, Q2 LO-2, Q3 LO-3, Q4 LO-3, Q5 LO-5, Q6 LO-4, Q7 LO-4, Q8 LO-1).

Lab steps that cover no outcome: Step 0 (set up and verify). By design: setup is Step 0 of the first lab and is never an outcome (STYLE). Not a finding.

Slide 18 (removal inside a loop) covers LO-3 at mention depth and has no lab step and no quiz item, as the depth mark requires.

Empty cells: 0.
