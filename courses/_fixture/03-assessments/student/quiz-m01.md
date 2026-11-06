---
course: _fixture
stage: 03-assessments/student
module: 01
author: assessment-designer
date: 2026-11-03
outcomes: LO-1, LO-2, LO-3
---

# Quiz: build the passing-students report

FIXTURE: sample content. Answer every question. One correct answer each unless stated.

## Question 1

<!-- item: Q1 | outcome: LO-2 | difficulty: basic -->

In the gradebook report, which clause keeps only the rows whose score is over 60?

A. SELECT
B. WHERE
C. ORDER BY
D. FROM

## Question 2

<!-- item: Q2 | outcome: LO-3 | difficulty: standard -->

**Requirement:** the teacher asked for students with a score over 60.

The gradebook query is `SELECT name FROM grades WHERE score > 60;` and Ben, who scored exactly
60, is not in the output. Is the query correct?

A. No, Ben passed so he must be listed.
B. Yes, exactly 60 is not over 60.
C. No, the query should use ORDER BY.
D. Yes, because WHERE always removes the lowest row.

## Question 3

<!-- item: Q3 | outcome: LO-1 | difficulty: basic -->

In the gradebook report, you want the highest score listed first. What do you add?

A. ORDER BY score DESC
B. ORDER BY score
C. WHERE score DESC
D. SELECT DESC score

## Question 4

<!-- item: Q4 | outcome: LO-3 | difficulty: basic -->

What is a boundary value in the gradebook report?

A. The first row of the grades table
B. A score exactly on the edge of the passing rule
C. The highest score in the class
D. A column name

## Question 5

<!-- item: Q5 | outcome: LO-2 | difficulty: basic -->

In the gradebook report, the grades table has scores 72, 60, and 55. How many rows does
`WHERE score > 60` return?

A. 0
B. 1
C. 2
D. 3

## Question 6

<!-- item: Q6 | outcome: LO-2 | difficulty: standard -->

The gradebook query returns no rows at all. Which check should you run first?

A. Rewrite the whole query.
B. Look at the scores in the table and compare them to the rule.
C. Add ORDER BY.
D. Delete the table.

## Question 7

<!-- item: Q7 | outcome: LO-1 | difficulty: standard -->

Your branch of the gradebook report lists passing students but the order looks random. Which
statement is true?

A. Without ORDER BY the order is not guaranteed.
B. SELECT always sorts by name.
C. WHERE sorts rows by score.
D. The table is broken.

## Question 8

<!-- item: Q8 | outcome: LO-3 | difficulty: stretch -->

**Transfer.** A library lists books "overdue by more than 7 days". A book is exactly 7 days
overdue. Using the same idea as the gradebook report, should that book be listed?

A. Yes, because 7 feels overdue.
B. No, because 7 is not more than 7.
C. Yes, because lists always include boundary values.
D. No, because only the newest books are listed.

## Predict and reflect

**Predict.** Before you run the lab query, write down how many rows you expect.

**Reflect.** After you run it, write what you got and whether your prediction held. Neither
answer is graded for being right.
