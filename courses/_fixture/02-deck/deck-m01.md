---
course: _fixture
stage: 02-deck
module: 01
author: deck-writer
date: 2026-11-03
outcomes: LO-1, LO-2, LO-3
---

# Build the passing-students report

## Slide 1: The gradebook report starts empty and ends as one saved query
- Start: a table of grades
- End: a list of passing students
Visual: A grades table on the left and a short list of passing students on the right.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="120" width="300" height="220" rx="10" class="box"/>
  <text x="180" y="165" text-anchor="middle" class="label label-strong">grades table</text>
  <text x="180" y="215" text-anchor="middle" class="label label-sm">name, score</text>
  <text x="180" y="255" text-anchor="middle" class="label label-sm">Ana 72, Ben 60, Cy 55</text>
  <path d="M346,230 L446,230" class="connector" marker-end="url(#arrow-muted)"/>
  <rect x="460" y="120" width="310" height="220" rx="10" class="box-accent"/>
  <text x="615" y="165" text-anchor="middle" class="label label-strong">passing report</text>
  <text x="615" y="230" text-anchor="middle" class="label label-sm">Ana 72</text>
</svg>
```
Notes: Today you build one thing, the gradebook report. Look at the left side. That is a plain table, the same kind of grid you already read in a spreadsheet. The right side is what a teacher wants: only the students who passed. The whole lesson is the move from the left to the right. You will do it with one saved query, and every idea today exists to make that query correct. Judge your own work by one test at the end: run the query and compare the rows with what the teacher asked for. If a row is missing, the problem is in the condition, which we cover in a few slides.
Covers: LO-1

## Slide 2: Mechanism: a WHERE clause keeps a row only when its condition is true
- The database checks each row
- True means keep, false means drop
Visual: Three rows pass through a filter box labelled WHERE score greater than sixty, and one row comes out.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="80" width="200" height="340" rx="10" class="box"/>
  <text x="130" y="115" text-anchor="middle" class="label label-strong">all rows</text>
  <text x="130" y="200" text-anchor="middle" class="label label-sm">Ana 72</text>
  <text x="130" y="250" text-anchor="middle" class="label label-sm">Ben 60</text>
  <text x="130" y="300" text-anchor="middle" class="label label-sm">Cy 55</text>
  <path d="M246,250 L326,250" class="connector" marker-end="url(#arrow-muted)"/>
  <rect x="340" y="170" width="190" height="160" rx="10" class="box-accent"/>
  <text x="435" y="245" text-anchor="middle" class="label label-strong">WHERE</text>
  <text x="435" y="280" text-anchor="middle" class="label label-sm">score &gt; 60</text>
  <path d="M546,250 L626,250" class="connector" marker-end="url(#arrow-muted)"/>
  <rect x="640" y="180" width="140" height="140" rx="10" class="box"/>
  <text x="710" y="255" text-anchor="middle" class="label label-sm">Ana 72</text>
</svg>
```
Notes: A WHERE clause is a test the database runs on every row, one at a time (SP-1.1). If the test comes out true, the row stays. If it comes out false, the row is dropped. That is why the result can never contain a row you did not ask for. To judge a query, run the test yourself on each row in your head. Ana has 72, which is over 60, so she stays. Cy has 55, so Cy is dropped. Ben has exactly 60, and whether Ben stays depends entirely on the symbol you wrote. Most students guess Ben stays, and that guess is the common wrong answer here.
Covers: LO-2

## Slide 3: Worked example: the query leaves out Ben because the request says over sixty
- Requirement: scores over 60 pass
- Query uses greater than
```sql
-- Requirement (the teacher's request): students with a score over 60
SELECT name, score FROM grades WHERE score > 60;
-- Output:
-- Ana | 72
-- Verdict: correct. Ben has exactly 60, which is not over 60.
```
Notes: Read the requirement first, because it is the source of truth here. The source is the teacher's request: over 60. The query uses the greater than symbol, so it keeps scores above 60 and nothing else (SP-1.1). Ben scored exactly 60, so Ben is not over 60, and leaving Ben out is correct. A common mistake is to call this a bug because Ben feels like a passing student. The query is not wrong. The feeling is not a requirement. If the teacher wanted 60 and up, the request would say so, and the symbol would change to greater than or equal to.
Covers: LO-2, LO-3

## Slide 4: Diagnostic sequence: a missing student is a question about the condition
Visual: A three-step path from the symptom to a check to a conclusion.
```svg
<svg viewBox="0 0 1200 420" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="110" width="320" height="170" rx="10" class="box"/>
  <text x="190" y="185" text-anchor="middle" class="label label-strong">Symptom</text>
  <text x="190" y="225" text-anchor="middle" class="label label-sm">Ben is missing</text>
  <path d="M366,195 L436,195" class="connector" marker-end="url(#arrow-muted)"/>
  <rect x="450" y="110" width="320" height="170" rx="10" class="box-accent"/>
  <text x="610" y="185" text-anchor="middle" class="label label-strong">Check</text>
  <text x="610" y="225" text-anchor="middle" class="label label-sm">Is his score exactly 60?</text>
  <path d="M786,195 L856,195" class="connector" marker-end="url(#arrow-muted)"/>
  <rect x="870" y="110" width="300" height="170" rx="10" class="box"/>
  <text x="1020" y="185" text-anchor="middle" class="label label-strong">Conclusion</text>
  <text x="1020" y="225" text-anchor="middle" class="label label-sm">The symbol excluded him</text>
</svg>
```
Notes: When a row is missing, do not rewrite the query yet. Run one check that separates the possible causes. Here the candidates are a typo in the name, a wrong table, or a boundary value. Look at the missing student's score. If it is exactly the passing mark, the cause is the symbol, and the right next move is to reread the requirement. If the score is clearly above the mark, the cause is somewhere else, such as the wrong table. The check sends you to two different places, which is what makes it worth running before you change anything.
Covers: LO-2, LO-3

## Slide 5: ORDER BY puts the highest scores first when you add DESC
- Add ORDER BY score DESC
- Highest score appears first
Visual: Two result lists, unsorted on the left and sorted highest first on the right.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="100" width="300" height="280" rx="10" class="box"/>
  <text x="180" y="140" text-anchor="middle" class="label label-strong">no ORDER BY</text>
  <text x="180" y="210" text-anchor="middle" class="label label-sm">Cy 65</text>
  <text x="180" y="260" text-anchor="middle" class="label label-sm">Ana 72</text>
  <path d="M346,240 L446,240" class="connector" marker-end="url(#arrow-muted)"/>
  <rect x="460" y="100" width="310" height="280" rx="10" class="box-accent"/>
  <text x="615" y="140" text-anchor="middle" class="label label-strong">ORDER BY score DESC</text>
  <text x="615" y="210" text-anchor="middle" class="label label-sm">Ana 72</text>
  <text x="615" y="260" text-anchor="middle" class="label label-sm">Cy 65</text>
</svg>
```
Notes: Sorting happens after filtering, so ORDER BY never changes which rows appear, only their order (SP-1.2). DESC means descending, from the highest value to the lowest. Without ORDER BY, the database may return rows in any order, so never rely on the order you happened to see once. To judge your result, read the score column from top to bottom. Each number should be the same or smaller than the one above it. If a number jumps up, DESC is missing or the wrong column was named.
Covers: LO-1

## Slide 6: Glossary for this module
- Query: a question you ask a database
- WHERE: the test that keeps rows
Visual: A plain list of the terms from this module.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="40" y="60" width="720" height="380" rx="10" class="box"/>
  <text x="400" y="130" text-anchor="middle" class="label label-strong">Glossary</text>
  <text x="400" y="200" text-anchor="middle" class="label label-sm">query, WHERE, boundary value, DESC</text>
</svg>
```
Notes: Use this slide as a quick check, not as new content. A query is a question you ask a database. WHERE is the test that decides which rows stay. A boundary value is a value exactly on the edge of a rule, like Ben's sixty, and it is where most mistakes hide. DESC means sorted from highest to lowest. Ask students to explain each term in their own words to a neighbour. If a student cannot say what a boundary value is, send them back to slide three and ask which row sat on the edge.
Covers: LO-3
