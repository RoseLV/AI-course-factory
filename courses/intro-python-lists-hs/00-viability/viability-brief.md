---
course: intro-python-lists-hs
stage: 00-viability
module: n/a
author: research-analyst
date: 2026-11-03
outcomes: n/a
---

# Viability brief: Intro to Python lists, high school

Two pages maximum. Every factual claim carries an `SP-` ID that resolves in `source-pack.md`.
"My reading" marks interpretation.

## Recommendation

GO. Confidence: medium.

1. Lists are a named high school skill. CSTA (Computer Science Teachers Association) standard 3A-AP-14 asks students to use lists instead of many separate variables (SP-0.12), at the grades 9 to 10 level (SP-0.13). The AP (Advanced Placement) Computer Science Principles exam, a College Board high school exam, tests storing data in lists and looping through them (SP-0.11).
2. The content is stable. The Python tutorial documents the same 11 list methods for Python 3.11 and 3.15 (SP-0.3). A method is a function attached to a value and called with a dot.
3. Python ranks first on TIOBE (SP-0.7), fourth in the Stack Overflow survey (SP-0.8), and second on GitHub (SP-0.10).

Confidence is medium because strong free courses already teach lists. The case is a format gap, not an empty market (my reading).

## Demand signals

- TIOBE index (a monthly language ranking built from search engine counts): Python is first in October 2026 at 19.23 percent, down 5.23 points in a year (SP-0.7).
- Stack Overflow Developer Survey (yearly and self-reported): 58.0 percent of respondents used Python in 2026 (SP-0.8), against 57.9 percent in 2025 (SP-0.9).
- GitHub Octoverse 2026 (GitHub's yearly activity report): Python is second behind TypeScript and gained 3.23 million monthly contributors in a year (SP-0.10).

Direction: falling on TIOBE, flat in the survey, rising on GitHub. My reading is flat at a high level. I found no measure of demand for a lists-only session.

## Audience fit

Yes, this can be taught honestly at this level. A list is an ordered collection of values written in square brackets. The official tutorial introduces lists in its first informal chapter and reuses the indexing rules learners met for text (SP-0.4). An index is an item's position, counting from 0. The tutorial's first `for` loop walks through a list (SP-0.5).

Prerequisites: write and run a short program that uses variables and `print()`, and save a file in an editor. Taught from zero: lists, indexing, `len()`, `append()`, `remove()`, and `for item in list`. Left out: `range()`, `while` loops, and functions.

Risks (my reading): 45 minutes is tight for complete beginners, so enforce the prerequisite and plan for 60 minutes. School-managed Chromebooks may block Linux (SP-0.15), so Step 0 needs a browser option. Khan Academy already runs its Python course in a browser editor (SP-0.19).

## Durability risk

Shelf life: about 36 months for the core content (my reading). Python ships a new version each October and supports each for five years (SP-0.2), and the list methods match across supported versions (SP-0.3).

Most likely to go stale:

1. The version number: 3.15.2 today (SP-0.1), with 3.16 due in October 2027 (SP-0.2).
2. Windows setup: the Python install manager (the new Windows setup tool) replaces the full installer after 3.15 (SP-0.14).
3. Competitor prices and syllabi (SP-0.18).

## Competitor scan

My selection from search results and known reach, not a measured ranking.

| Course | Format | Depth | Price | Gap this course fills |
| --- | --- | --- | --- | --- |
| W3Schools Python Lists (SP-0.16) | Text, try-it editor, exercises | 12 reference pages | No price shown | Reference layout, no stated level |
| Codecademy Learn Python 3 (SP-0.17, SP-0.18) | Interactive lessons, projects, quizzes | 24-hour beginner course, Python 3.13 | Basic $0; Plus $11.99 or Pro $15.99 a month, billed annually | Lists are one module; certificates need a paid plan |
| Khan Academy Intro to CS, Python (SP-0.19, SP-0.20) | Browser projects | Whole course: conditionals, loops, functions | Free | Semester scale; lists unit unconfirmed |
| CS50's Introduction to Programming with Python (SP-0.21, SP-0.22) | Lectures and problem sets, Week 0 to Week 9 | Harvard course; lists inside the loops week | Free; paid certificates | Adult pace and length |
| Python for Everybody (SP-0.23) | Videos, book, autograder | Whole course; Lists is lesson 9 of 17 | Free, open licence | Lists come late; no high school framing |

The gap, in my words: one class period for grades 9 and 10, ending in one program a teacher checks with one command, with a planted bug to find.

## Build cost

One module, one deck, one quiz, and one lab (my reading). Cheapest: the syllabus. Most expensive: the deck (mechanism, worked example with real output, diagnostic sequence, drawn visuals) and the lab (10 fields per step, local and browser Step 0 paths, a planted defect).

## Proposed capstone

A capstone is the one artifact the learner ships. The user named none, so I propose `playlist.py`, a class playlist script that:

1. Creates a list of four song titles.
2. Adds a song with `append()` and removes one with `remove()` (SP-0.6).
3. Prints the song count with `len()` and the first song by its index (SP-0.4).
4. Prints every song, numbered, with a `for` loop (SP-0.5).

End state someone else can check: `python playlist.py` prints exactly the expected-output block in the lab. `python` is the recommended Windows command (SP-0.14). The lab must confirm the macOS, Linux, and browser equivalents.

Planted defect: the starter file removes a song that is not in the list, so `remove()` raises a `ValueError`, its error when no item matches (SP-0.6).

Fits one module: yes, with a 25 to 30 minute lab (my reading). It uses only list methods present in 3.11 through 3.15 (SP-0.2, SP-0.3).

## Limitations

- Two primary PDFs were unreadable. The 3A-AP-14 wording comes from Code.org's page instead (SP-0.12), and I could not confirm that the AP Create task program must contain a list.
- Could not verify the national share of high schools teaching computer science, a lists unit in Khan's course, or CodeHS's current course (its pages need JavaScript, so CodeHS is omitted).
- Did not measure search trends, verify macOS or Linux run commands, or test a browser editor. Prices are as fetched on 2026-11-03 and may vary by region.
