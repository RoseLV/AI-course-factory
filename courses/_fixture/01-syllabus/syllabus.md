---
course: _fixture
stage: 01-syllabus
module: n/a
author: curriculum-architect
date: 2026-11-03
outcomes: LO-1 to LO-3
---

# Intro to SQL: build a gradebook report

FIXTURE: sample content for tooling tests.

## Course metadata

- **Audience level:** high school
- **Modules:** 1
- **Total duration:** 35 minutes
- **Session length:** 35 minutes
- **Delivery format:** instructor-led session with a lab
- **Content last verified:** 2026-11-03

## Prerequisites

The learner can already:

- Read a table of rows and columns.

## Learning outcomes

| ID | Outcome | Applied |
| --- | --- | --- |
| LO-1 | Build a gradebook report query that lists passing students by score | yes |
| LO-2 | Filter rows with a `WHERE` condition and predict which rows it keeps | yes |
| LO-3 | Explain why `>` and `>=` give different results at the boundary | no |

## Capstone

- **Name and pitch:** Gradebook report. One saved query that shows who passed.
- **Artifact:** A saved SQL query over a `grades` table.
- **End state:** Running the query prints the passing students, highest score first.
- **Learner designs:** The passing mark.
- **Proves outcomes:** LO-1, LO-2, LO-3

| Module | Adds to the capstone | State when the module ends | Minutes |
| --- | --- | --- | --- |
| M01 | The whole query | Query prints passing students sorted | 20 |

## Module breakdown

### M01: Build the passing-students report

- **Outcomes:** LO-1, LO-2, LO-3
- **Running case:** A teacher asks for students who scored over 60. The query uses `>`. A student
  with exactly 60 is missing. The requirement says "over 60", so the row is correctly excluded.

| Topic | Depth | Minutes | Lab step or quiz item |
| --- | --- | --- | --- |
| What a query is | mention | 2 | none |
| SELECT and WHERE | practise | 8 | Lab step 1, Q1 |
| Boundary values | practise | 6 | Lab step 2, Q2 |
| ORDER BY | explain | 4 | Q3 |

**Time budget:** narration 5 min, hands-on 20 min, checkpoints 5 min, discussion 5 min.
Total 35 min. Narration word budget: 650.

**Assessment:** quiz-m01. **Lab:** lab-m01.

## Alignment table

| Outcome | Module | Practise topic | Quiz | Lab |
| --- | --- | --- | --- | --- |
| LO-1 | M01 | SELECT and WHERE | Q1, Q3 | steps 1 to 3 |
| LO-2 | M01 | SELECT and WHERE | Q1, Q2 | step 1 |
| LO-3 | M01 | Boundary values | Q2, Q4 | step 2 |

## Out of scope

| Item | Why |
| --- | --- |
| Joins | Needs a second table, which this single module does not have time for |

## Rot watch

| Item | Where it appears | Source |
| --- | --- | --- |
| Online SQL tool | Lab step 0 | SP-1.1 |

## Revision log

| Date | Change | Driven by |
| --- | --- | --- |
| 2026-11-03 | First draft | n/a |
