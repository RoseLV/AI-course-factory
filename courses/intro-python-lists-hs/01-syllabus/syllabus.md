---
course: intro-python-lists-hs
stage: 01-syllabus
module: n/a
author: curriculum-architect
date: 2026-11-03
outcomes: LO-1 to LO-5
---

# Intro to Python lists

## Course metadata

- **Audience level:** High school (CSTA level 3A, grades 9 to 10, SP-0.13)
- **Modules:** 1
- **Total duration:** 1 hour
- **Session length:** 60 minutes (a Gate 1 decision, see the report: the high school rubric asks for 30 to 45)
- **Delivery format:** One instructor-led class session. A deck, an eight-item quiz, and a scaffolded lab run on local Python or in a browser editor.
- **Content last verified:** 2026-11-03 (Python 3.15.2 documentation, SP-0.1; list methods match 3.11 to 3.15, SP-0.2, SP-0.3)

## Prerequisites

The learner can already:

- Write and run a short Python program that uses `print()` and stores a value in a variable with `=`.
- Save a file in an editor and run it.
- Read an indented block of code.
- Read a short error message and find the line number in it.
- Change a number variable by assigning to it again, for example `count = count + 1`.

Enforcement: the instructor confirms these five skills before the session, outside the 60 minutes, with a short entry task. A learner who cannot do all five does not join this session. The last skill is an addition to the viability brief's prerequisite list, because the numbering step needs it (see `GAPS`).

Not required: conditionals (`if`), functions, `range()`, `while` loops, or the `in` operator.

## Learning outcomes

| ID | Outcome | Applied |
| --- | --- | --- |
| LO-1 | Build `playlist.py`, a script that creates a list of four songs, changes it, and prints the count, the first song, and every song numbered | yes |
| LO-2 | Print the first item of a list by its index and the number of items with `len()` | yes |
| LO-3 | Change a list with `append()` and `remove()`, and explain what each one changes | yes |
| LO-4 | Write a `for` loop that prints every item in a list, numbered from 1 | yes |
| LO-5 | Debug a `ValueError` raised by `remove()` by reading the error line and correcting the song name | yes |

Applied: 5 of 5. No outcome is about a tool alone. Setup is Step 0 of the lab, not an outcome.

## Capstone

- **Name and pitch:** `playlist.py`: "I made a program that keeps my class playlist, adds a song, drops a song, and shows the list numbered."
- **Artifact:** A single Python file. It creates a list of four song titles, adds one with `append()`, removes one by name with `remove()`, prints the count with `len()`, prints the first song by its index, and prints every song numbered with a `for` loop.
- **End state:** Running `playlist.py` prints exactly the lab's expected-output block, and nothing else. Locally the command is `python playlist.py` (the recommended Windows command, SP-0.14). In a browser editor the run button replaces the command. The block has one count line, one first-song line, and one numbered line per remaining song, numbered 1 to 4 (derived from SP-1.1 to SP-1.7). An instructor or classmate checks it by comparing the two outputs. The lab owns the exact wording of each line.
- **Learner designs:** The numbering logic: the name of the counter variable, where it starts, and where it goes up by one. After the checked run passes, the learner may swap in their own song titles as an extension. That extension is not checked against the expected-output block.
- **Proves outcomes:** LO-1, LO-2, LO-3, LO-4, LO-5

| Module | Adds to the capstone | State when the module ends | Minutes |
| --- | --- | --- | --- |
| M01 | Everything. The starter holds the four-song list and one `remove()` line that names a song not in the list (the planted defect). The learner adds the count and first-song lines, the `append()` call, the corrected `remove()` call, and the numbered loop. | `playlist.py` runs to the end without an error and its output matches the expected-output block. | 29 (the lab) |

## Module breakdown

### M01: Build playlist.py, a numbered playlist you can add to and remove from

- **Outcomes:** LO-1, LO-2, LO-3, LO-4, LO-5
- **Running case:** The task, written as the class's request: "Keep our class playlist in one program. It starts with four songs, adds one, drops one by name, then shows how many songs there are, which song is first, and every song numbered." What happens: the learner builds the script step by step from the starter. The failure: the starter's `remove()` line names a song that is not in the list, so Python stops with a `ValueError` at that line and prints nothing after it (SP-1.5, SP-0.6). The learner reads the error line, compares the name with the list, and corrects the name. A second likely failure is a numbered printout that starts at 0, which the numbering step prevents (SP-1.7). Verified result: the output matches the lab's expected-output block. Source of truth: a written specification, the lab's expected-output block, shown to the learner before they run anything. The ValueError message text itself is not taught or quoted until someone runs it on the current Python (SP-U1).
- **Claims relied on:** SP-0.3, SP-0.4, SP-0.5, SP-0.6, SP-1.1, SP-1.2, SP-1.3, SP-1.4, SP-1.5, SP-1.6, SP-1.8 (mention only), SP-0.12 (the "why lists" framing).
- **Terms to define at first use:** list, item, index, method, `for` loop, loop variable, counter, error, `ValueError`, `IndexError`.

| Topic | Depth | Minutes | Lab step or quiz item |
| --- | --- | --- | --- |
| What a list is: items kept in order in square brackets, one list instead of four variables | explain | 3 | Q8 |
| Index counts from 0, the last index is len minus one, and a missing index raises `IndexError` | explain | 3 | Q1, Q2 |
| Methods, `len()`, and `append()`: a method is a function called with a dot, and `append()` returns `None` | explain | 3 | Q3 |
| `remove()` deletes by value, takes the first match, and raises `ValueError` when nothing matches | explain | 3 | Q4 |
| The `for` loop gives each item in order, not each index | explain | 3 | Q6 |
| A counter variable for numbering from 1 | explain | 2 | Q7 |
| Trap: removing items while looping over the same list | mention | 1 | none |
| Print the first song by index | practise | 3 | Lab Step 1 |
| Print the song count with `len()` | practise | 2 | Lab Step 1 |
| Add a song with `append()` | practise | 4 | Lab Step 2 |
| Remove a song by name | practise | 3 | Lab Step 3 |
| Debug the `ValueError` from `remove()` | practise | 3 | Lab Step 3, Q5 |
| Print every song numbered with a `for` loop and a counter | practise | 6 | Lab Step 4 |
| Assemble and run `playlist.py` against the expected-output block | practise | 3 | Lab Step 5, Q8 |

Narration rows (explain and mention) sum to 18 minutes. Practise rows sum to 24 minutes. Lab Step 0 adds 5 minutes of setup, which is not a topic, so the lab totals 29 minutes.

Lab steps this syllabus fixes, for lab-m01:

1. Step 0, set up and run a one-line check: 5 min.
2. Step 1, print the count and the first song: 5 min.
3. Step 2, add a song with `append()`: 4 min.
4. Step 3, remove a song by name and fix the `ValueError`: 6 min. The defect first fires here, not in Step 0.
5. Step 4, print every song numbered: 6 min.
6. Step 5, debrief, including the full run against the expected-output block: 3 min.

Quiz contract for quiz-m01, eight items, 4 basic, 3 standard, 1 stretch:

| Item | Outcome | Difficulty | Topic tested |
| --- | --- | --- | --- |
| Q1 | LO-2 | basic | Which expression gives the first song |
| Q2 | LO-2 | basic | Count of four, last valid index, and what index 4 does |
| Q3 | LO-3 | basic | What `append()` changes and returns |
| Q4 | LO-3 | standard | `remove()` takes a value, not a position |
| Q5 | LO-5 | standard | Judge a real failing run: name the error and the line |
| Q6 | LO-4 | basic | The loop variable holds items, not indexes |
| Q7 | LO-4 | standard | Judge numbered output that starts at the wrong number |
| Q8 | LO-1 | stretch | Transfer: build the same steps for a list of homework tasks |

Q5 must use output someone captured by running the starter. It must not rely on the message wording in SP-U1 unless it is captured.

**Time budget:** narration 18 min, hands-on 29 min, checkpoints 8 min, discussion 5 min.
Total 60 min. Narration word budget: 2340.

The 60 minutes is a fit only if the prerequisite is enforced. The checkpoint minutes cover the eight-item quiz at under one minute an item. If the quiz runs long, move it to the start of the next class. Do not shorten the lab.

**Assessment:** quiz-m01. **Lab:** lab-m01.

## Alignment table

| Outcome | Module | Practise topic | Quiz | Lab |
| --- | --- | --- | --- | --- |
| LO-1 | M01 | Assemble and run `playlist.py` against the expected-output block | Q8 | Step 5 |
| LO-2 | M01 | Print the first song by index; print the song count with `len()` | Q1, Q2 | Step 1 |
| LO-3 | M01 | Add a song with `append()`; remove a song by name | Q3, Q4 | Steps 2, 3 |
| LO-4 | M01 | Print every song numbered with a `for` loop and a counter | Q6, Q7 | Step 4 |
| LO-5 | M01 | Debug the `ValueError` from `remove()` | Q5 | Step 3 |

## Out of scope

| Item | Why |
| --- | --- |
| A guard such as `if song in songs` | Conditionals and `in` are not prerequisites. The defect is fixed by correcting the name. |
| `enumerate(songs, start=1)` (SP-1.7) | It adds tuple unpacking, a second new idea in one loop. The manual counter uses only variables. |
| `range(len(songs))` | The viability brief leaves `range()` out. |
| `try` and `except` | Error handling is a later topic. This lesson teaches reading the error. |
| The other list methods (`insert`, `pop`, `sort`, and the rest of the 11 in SP-0.3) | The capstone needs two. More would break the one-concept rule. |
| Slicing, negative indexes, nested lists | None is needed for the capstone. |
| Removing items inside a loop over the same list (SP-1.8) | Named as a trap only, at mention depth. The skip bug needs its own session. |
| What `print(songs)` shows for a whole list (SP-U2) | Unsourced and unrun. The capstone prints one song per line instead. |
| Reading user input | Songs are written in the file, so no input is needed. |
| AP Computer Science Principles exam preparation (SP-0.11) | The course supports the list skills the exam tests but does not prepare for it. |
| Installing Python on a school-managed device | Step 0 gives a browser option. Administrator settings decide local installs (SP-0.15). |

## Rot watch

| Item | Where it appears | Source |
| --- | --- | --- |
| Python version number, 3.15.2 today, 3.16 due 2027-10-06 | Metadata, lab Step 0, any slide naming a version | SP-0.1, SP-0.2 |
| Windows install steps and the `python` command | Lab Step 0, the capstone end state | SP-0.14 |
| Method notation, `append(value, /)` against `append(x)` | Slides that quote the documentation, glossary | SP-0.3 |
| Exact `ValueError` and `IndexError` message text | Lab evidence, lab troubleshooting table, Q5 | SP-U1 |
| Tutorial section numbers (3.1.3, 4.2, 5.1) | Source citations in slide notes | SP-0.4, SP-0.5, SP-0.6 |
| CSTA and AP claims on the "why lists" slide | Deck slide notes, if used | SP-0.11, SP-0.12, SP-0.13 |
| Chromebook Linux availability | Lab Step 0 browser option | SP-0.15 |
| Forum thread URLs for misconceptions | Instructor notes | SP-1.2, SP-1.4, SP-1.5 |

## Revision log

| Date | Change | Driven by |
| --- | --- | --- |
| 2026-11-03 | First draft | n/a |
