---
course: _fixture
stage: 04-labs
module: 01
author: lab-engineer
date: 2026-11-03
outcomes: LO-1, LO-2, LO-3
---

# Filtering and ordering rows to build a report

FIXTURE: sample content.

## What problem this lab solves

**Purpose:** Trains a high school learner to turn a plain request into a correct query.

**Context:** Learners often write a query and trust it because it ran without an error. This lab
makes them check the rows against the written rule.

**Core skill being trained:** Checking a result against a stated requirement.

The learner will be able to:

- Build a gradebook report query (LO-1)
- Predict which rows a WHERE condition keeps (LO-2)

**Final deliverable:** One saved query that prints the passing students, highest score first.

## How the steps work together

| Step | Title | Minutes |
| --- | --- | --- |
| 0 | Set up and verify | 5 |
| 1 | Filter the passing students | 8 |
| 2 | Find the boundary row | 4 |
| 3 | Debrief | 3 |

Step times sum to 20 minutes against the module's 20 hands-on minutes in the syllabus.

## Guidance and tools

**Primary tooling:** Any SQL tool the instructor provides, with a `grades` table loaded.

**Key concepts from the lecture:** WHERE, boundary value, ORDER BY.

### Step 0 - Set up and verify

**Purpose:** Confirm the tool runs.
**Time:** 5 minutes

1. Open the SQL tool.
2. Run `SELECT name, score FROM grades;` and confirm three rows appear.

### Step 1 - Filter the passing students

**Purpose:** Write the first version of the report.
**Time:** 8 minutes
**Starting state:** The `grades` table has Ana 72, Ben 60, Cy 55.
**Task:** List students whose score is over 60.
**Prediction:** Write how many rows you expect before you run it.
**Action:** `SELECT name, score FROM grades WHERE score > 60 ORDER BY score DESC;`
**Evidence:** Passing output: one row, Ana 72. Failing output: three rows, which means the WHERE
clause is missing.
**Interpretation:** A pass proves the filter works on this data. It does not prove the rule is right.
**Recovery:** If you see an error, check the semicolon and the column names.
**Why this matters:** A query that runs is not the same as a query that is correct.

> Unexecuted teaching sample: no one has run this step.

### Step 2 - Find the boundary row

**Purpose:** Meet the planted defect.
**Time:** 4 minutes
**Starting state:** The report from step 1.
**Task:** Ben says he passed. Decide whether the report is wrong.
**Prediction:** Write whether you think Ben should be listed.
**Action:** Reread the request, then run `SELECT name, score FROM grades WHERE score = 60;`
**Evidence:** Passing output: one row, Ben 60. Failing output: no rows.
**Interpretation:** Ben is exactly on the boundary. The request says "over 60", so he is correctly excluded.
**Recovery:** If your table has no Ben row, reload the starting data.
**Why this matters:** The written request is the source of truth, not the feeling that someone passed.

**Planted defect:** Ben's score is exactly 60. **Requirement it violates:** none, the report is
correct as written, which is the lesson. **Source of truth:** the user's request.

> Unexecuted teaching sample: no one has run this step.

### Step 3 - Debrief

**Purpose:** Pull the lab together.
**Time:** 3 minutes

- What exists now: a saved report that prints passing students highest first.
- The prediction learners most often get wrong: that Ben is included.
- The planted defect and its source of truth: Ben at exactly 60, from the teacher's request.
- What the next module picks up: nothing, this is a one-module fixture.
- What this lab did not cover: joins.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Error near WHERE | Missing FROM clause | Add `FROM grades` |
| All rows appear | WHERE clause missing | Add `WHERE score > 60` |
