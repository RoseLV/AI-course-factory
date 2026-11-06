---
course: intro-python-lists-hs
stage: 03-assessments/instructor
module: 01
author: assessment-designer
date: 2026-11-03
outcomes: LO-1, LO-2, LO-3, LO-4, LO-5
---

# Instructor key: quiz-m01

Instructor only. Never copy into the student tree. For human grading. Nothing here is graded by an agent.

## Q1 - Answer: B

- A: a student choosing this counts positions from 1 in daily life and thinks the first item is index 1 (misconceptions table, row 1).
- **B is correct.** The first item has index 0, so `songs[0]` is "Sunrise Walk" (SP-1.1).
- C: a student choosing this thinks the count from `len()` is a position, and that the last place is `len(songs)`. Index 4 does not exist in a four-item list, so this raises `IndexError` (SP-1.2, SP-1.3).
- D: a student choosing this thinks every common action has a named method. A list has no `first()` method (SP-0.3 lists the 11 list methods).

## Q2 - Answer: C

- A: a student choosing this thinks the last index equals the count, so the first index is 1 (SP-1.1, SP-1.3). Index 4 does not exist.
- B: a student choosing this confuses the count with the last index, and thinks `len()` returns the last position (SP-1.3). `len(songs)` is 4.
- **C is correct.** `len(songs)` is 4, indexes run 0 to 3, and index 4 raises `IndexError` (SP-1.2, SP-1.3).
- D: a student choosing this thinks a missing index gives an empty value instead of stopping the program (SP-1.2).

## Q3 - Answer: A

- **A is correct.** `append()` changes the list in place and returns `None`, so `print(result)` shows `None`. The list now has five items, so `len(songs)` is 5 (SP-1.4).
- B: a student choosing this thinks `append()` hands back the updated list (misconceptions table, row 2, the `Newlist = List.append(7)` case).
- C: a student choosing this sees that `None` is returned and concludes nothing was added. The change is a side effect on `songs`, and it happened (SP-1.4).
- D: a student choosing this thinks a method that changes a list cannot be used on the right side of `=`. Python allows it, and `result` holds `None` (SP-1.4).

## Q4 - Answer: D

- A: a student choosing this thinks `remove()` takes a position, because `songs[1]` uses the same brackets-and-number shape (misconceptions table, hypothesis row on `remove(1)`).
- B: a student choosing this thinks `remove()` takes a position and counts positions from 1, so it combines two misconceptions.
- C: a student choosing this thinks `remove()` ignores a value that matches nothing (hypothesis row on absent songs). Python raises `ValueError` and the script stops (SP-1.5, SP-0.6).
- **D is correct.** `remove(value)` compares the value with each top-level item by equality. No item equals 1, so Python raises `ValueError` (SP-1.5). The item does not name the message text (SP-U1).

## Q5 - Answer: ValueError, at line 3. The program stops at line 3 so lines 4 and 5 never run. Change the name in the `remove()` line to "Blue Window" and leave the list alone.

Source of truth: the requirement stated in the item itself, which fixes the four starting titles.
Requirement quoted from the item: "The four starting titles in line 1 are the specification and may not be edited. The program must still add "Garden Song" and remove "Blue Window" by name, and it must run to the end with no error. Python runs lines from top to bottom, and an error stops the program at the line that causes it, so no later line runs."
Why only one fix passes: editing line 1 is barred by the requirement, and deleting line 3 breaks the "remove "Blue Window" by name" clause. Correcting the name in line 3 is the only change that meets every clause.
Boundary check: the error is at line 3, not line 1. Line 1 holds the list with the title spelled "Blue Window", so the list is right and the `remove()` name "Blue Windows" is one letter off (SP-1.5, SP-0.6). Line 2 runs without error, so the append happens before the stop. The fix changes the name in line 3, and the list stays as written, as the item's requirement says.

Marking points, all observable:

1. Names `ValueError` (not `IndexError`, not `NameError`).
2. Names line 3.
3. Says the print lines come after the failing line and Python stops there, so they never run.
4. Says to correct the name in `remove()` to match the list. Do not accept "change the list to match", "add an if check", or "delete the remove line".

This item does not use or require the message text after `ValueError` (SP-U1). Accept any wording of the type and line.

What a learner who pattern-matched the lab would answer instead: not applicable (this is a judgement item). A common slip is to say line 4 or line 5 because the missing output is there. The error line is where the program stops, line 3.

## Q6 - Answer: C

- A: a student choosing this thinks the loop variable holds the index, and that the second item sits at index 1 (SP-1.6).
- B: a student choosing this thinks the loop variable counts passes. It holds items, so numbering needs a counter the learner builds (SP-1.6).
- **C is correct.** A `for` loop gives the loop variable each item in list order, so on the second pass `song` is "Blue Window" (SP-1.6, SP-0.5).
- D: a student choosing this thinks the loop variable keeps its first value until the loop ends. It is reassigned on every pass (SP-1.6).

## Q7 - Answer: B

Source of truth: a written specification, the lab's expected-output block.
Requirement quoted from the item: "The lab's expected-output block numbers the songs counting from 1, so the first song line starts with 1 and the last starts with 4."
Boundary check: the output begins at 0, and 0 is not 1, so the output fails. The numbers do rise by one and no song is missing, but the stated start value decides the verdict. Starting at 0 and adding one after the print gives 0 to 3. Either starting at 1, or adding one before the print, would pass, as the lab notes.

- A: a student choosing this checks only that the numbers rise steadily and ignores the stated start (hypothesis row on numbering from 1, SP-1.7).
- **B is correct.** The first number is 0, and the requirement starts at 1.
- C: a student choosing this confuses an index, which counts from 0 (SP-1.1), with a display number, which the requirement counts from 1. The loop does not use the index at all.
- D: a student choosing this miscounts the output. All four songs appear, so none is missing.

## Q8 - Answer: any program that prints the five output lines exactly, using append(), remove() by name, len(), index 0, and a for loop with a counter

Source of truth: a written specification, the output block shown in the item.
Requirement quoted from the item: "prints exactly the output below and nothing else", with a `for` loop and a counter variable, and no `if`, `enumerate()`, or `range()`.
Boundary check: the list has 3 items, gains one, and loses one, so the count is 3. The order after the changes is Read chapter 3, Essay draft, Science quiz, so the first task is "Read chapter 3". The counter's first printed value is 1, not 0.

One full-credit model answer:

```python
tasks.append("Science quiz")
tasks.remove("Math worksheet")
print("Tasks:", len(tasks))
print("First task:", tasks[0])
number = 1
for task in tasks:
    print(number, task)
    number = number + 1
```

Marking points, all observable:

1. Calls `append("Science quiz")` alone on its own line, not stored or printed (SP-1.4).
2. Calls `remove("Math worksheet")` with the exact name, not a position (SP-1.5).
3. Both calls come before the count and first-task lines.
4. Prints the count with `len(tasks)` and the first task with `tasks[0]` (SP-1.1, SP-1.3).
5. Uses a `for` loop over `tasks` with a counter whose printed values are 1, 2, 3. Accept a counter that starts at 0 and goes up before the print.
6. The program prints the five lines and nothing else, with no `if`, `enumerate()`, or `range()`.

Accept any variable names and any print form that gives the same lines.

What a learner who pattern-matched the capstone would answer instead: copy `songs`, "Garden Song", or "Blue Window" from `playlist.py` into the answer, or start the counter at 0 so the numbers run 0 to 2.
