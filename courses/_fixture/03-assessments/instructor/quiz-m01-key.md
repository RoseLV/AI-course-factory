---
course: _fixture
stage: 03-assessments/instructor
module: 01
author: assessment-designer
date: 2026-11-03
outcomes: LO-1, LO-2, LO-3
---

# Instructor key: quiz-m01

FIXTURE: sample content. Instructor only.

## Q1 - Answer: B

- A: a student choosing this thinks SELECT picks rows, when it only picks columns.
- **B is correct.** WHERE keeps rows whose condition is true (SP-1.1).
- C: a student choosing this confuses sorting with filtering.
- D: a student choosing this thinks FROM names a condition, when it names the table.

## Q2 - Answer: B

Source of truth: the user's request. Requirement quoted from the item: "over 60".
Boundary check: exactly 60 is not over 60, so excluding Ben is correct.

- A: a student choosing this lets the feeling that Ben passed override the written rule.
- **B is correct.**
- C: a student choosing this thinks sorting could bring a row back.
- D: a student choosing this thinks WHERE removes a fixed row instead of testing each one.

## Q3 - Answer: A

- **A is correct.** DESC sorts highest first (SP-1.2).
- B: a student choosing this does not know the default direction is ascending.
- C: a student choosing this puts a sort word inside a filter.
- D: a student choosing this invents syntax.

## Q4 - Answer: B

- A: a student choosing this treats "boundary" as "beginning".
- **B is correct.**
- C: a student choosing this confuses an extreme value with an edge value.
- D: a student choosing this confuses a value with a name.

## Q5 - Answer: B

Only 72 is over 60. Misconception for C: counting 60 as passing.

- A: a student choosing this thinks no row can pass.
- **B is correct.**
- C: a student choosing this counts the boundary row.
- D: a student choosing this thinks WHERE removes nothing.

## Q6 - Answer: B

- A: a student choosing this changes things before finding the cause.
- **B is correct.** The check separates a wrong rule from a wrong table.
- C: a student choosing this thinks sorting can create rows.
- D: a student choosing this acts destructively.

## Q7 - Answer: A

- **A is correct.**
- B: a student choosing this assumes a default sort by name.
- C: a student choosing this confuses filtering with sorting.
- D: a student choosing this blames the data.

## Q8 - Answer: B

Source of truth: the written rule "more than 7 days". Exactly 7 is not more than 7.
What a learner who pattern-matched the gradebook might answer instead: "list it", because Ben's row
felt like it should pass.

- A: a student choosing this lets feeling override the rule.
- **B is correct.**
- C: a student choosing this invents a rule about boundaries.
- D: a student choosing this ignores the stated condition.
