---
course: intro-python-lists-hs
stage: 03-assessments/instructor
module: 01
author: assessment-designer
date: 2026-11-03
outcomes: LO-1, LO-2, LO-3, LO-4, LO-5
---

# TA feedback pack: module 01

Safe for the ta-agent. Contains criteria and misconception explanations only. No literal answers,
no solutions, no answer letters. Write it assuming a student will read it.

People grade the quiz and the lab. This pack helps a TA give feedback to a student who is stuck. It does not grade anything.

## What each quiz item measures

| Item | Outcome | What it checks | Common confusion, explained without the answer |
| --- | --- | --- | --- |
| Q1 | LO-2 | Reading one song out of the playlist list by its position number | Everyday counting starts at one, and Python's position numbers follow a different habit. Ask how they decided which number to write, and whether that habit would work the same way in every counting situation. |
| Q2 | LO-2 | Relating the count from `len()` to the position numbers that exist | The count and the highest position number look alike, so learners treat them as one number. Ask them to list every position of the four-song list on paper. |
| Q3 | LO-3 | What `append()` does to the list, and what a method call gives back | Learners expect every function call to hand back a finished result. Ask which of the two things happened to `songs`: a change, or a returned value, or both. |
| Q4 | LO-3 | What kind of input `remove()` takes | The same brackets-and-number look appears in two places in a program, so learners assume the number means the same thing in both. Ask what they think `remove()` needs to be told in order to find the right item. |
| Q5 | LO-5 | Reading a failed run: error type, line number, and why later lines stay silent | Learners look at where the missing output should be, not where the program stopped. Ask them to read the file top to bottom, one line at a time, and say what the screen would show after each line. |
| Q6 | LO-4 | What the loop variable holds on each pass of a `for` loop | Learners picture the loop as counting. Ask them to write out a table with one row per pass and one column for the loop variable. |
| Q7 | LO-4 | Judging printed numbers against a written requirement | A pattern that looks tidy can still break a rule that is stated in words. Ask them to read the requirement again and check the output against it, one line at a time. |
| Q8 | LO-1 | Applying the same sequence of steps to a new list | Learners copy the shape of `playlist.py` without checking each line against the new data. Ask them to work out by hand what the list holds after each step. |

## Lab rubric criteria

Observable behaviours a person can check by running the file and reading the code.

- The file is named `playlist.py` and runs to the end with no error report.
- Running it prints six lines that match the Expected output block in the lab, with nothing before or after.
- The list is created with the four starting titles, spelled as in the starter file.
- One `append()` call sits on its own line and is not printed or stored in a variable.
- One `remove()` call sits on its own line and names a title that exists in the list, spelled exactly as in the list.
- The list line was not edited to match the starter's `remove()` line.
- The count line uses `len()`. The first-song line uses an index.
- Both the count line and the first-song line sit below the lines that change the list.
- The numbered output comes from a `for` loop over the list, with a counter variable the student named and set up.
- The counter changes inside the loop, on its own line.
- The file contains no `if`, `enumerate()`, `range()`, `try`, or `except`.
- In the Step 3 prediction, the student wrote down what they expected before running. The prediction is not marked for being right.
- In the Step 3 reflection, the student states the error type and the line number the error report names.

## Hints that do not give the answer

- Step 1: "Which number do you put in the brackets for the first song? Write the positions of all four songs on paper and check."
- Step 1: "If the program stops with an index error, which line does it name, and what does that index point at?"
- Step 2: "Does the line that changes the list come before or after the lines that read it? Walk through the file top to bottom."
- Step 2: "Is there anything on the screen you did not expect? Which line of your file produced it?"
- Step 3: "Read the last line of the error report. What type is it, and which line does it name?"
- Step 3: "Put the name in your `remove()` line next to the title in the list. Compare them letter by letter. What differs?"
- Step 3: "What does the lab text say you may and may not change in the file?"
- Step 3: "After the line that failed, which lines did Python run?"
- Step 4: "Write the loop on paper with three columns: the pass, the counter, and the song. Fill in each row before you run."
- Step 4: "What is the first number the expected output shows? Where in your loop is the counter set, and where does it change?"
- Step 4: "If every line shows the same number, which line is meant to change the counter, and is it inside the loop?"
- Step 5: "Compare your output with the Expected output block line by line. Which line first differs, and what part of your code writes that line?"
- Quiz Q8: "Write the list on paper. Cross out and add items by hand in the order the steps say. What does it hold at the end?"
