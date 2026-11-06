---
course: intro-python-lists-hs
stage: 03-assessments/student
module: 01
author: assessment-designer
date: 2026-11-03
outcomes: LO-1, LO-2, LO-3, LO-4, LO-5
---

# Quiz: Build playlist.py, a numbered playlist you can add to and remove from

Answer every question. Multiple choice questions have one correct answer unless stated.

## Question 1

<!-- item: Q1 | outcome: LO-2 | difficulty: basic -->

In `playlist.py`, the class playlist starts as this list:

```python
songs = ["Sunrise Walk", "Blue Window", "Paper Planes", "Night Bus"]
```

An index is the position number you write in square brackets after the list name. Which expression gives the first song, "Sunrise Walk"?

A. `songs[1]`
B. `songs[0]`
C. `songs[len(songs)]`
D. `songs.first()`

## Question 2

<!-- item: Q2 | outcome: LO-2 | difficulty: basic -->

`playlist.py` starts with the same four-song list as Question 1, before any song is added or removed. An `IndexError` is the error Python gives when an index does not exist in the list. Which statement is true?

A. `len(songs)` is 4, the last index is 4, and `songs[4]` gives "Night Bus".
B. `len(songs)` is 3, the last index is 3, and `songs[3]` gives "Night Bus".
C. `len(songs)` is 4, the last index is 3, and `songs[4]` raises an `IndexError`.
D. `len(songs)` is 4, the last index is 3, and `songs[4]` gives `None`.

## Question 3

<!-- item: Q3 | outcome: LO-3 | difficulty: basic -->

A method is a function you call with a dot after the list name. A student tests `append()` in a copy of `playlist.py`:

```python
songs = ["Sunrise Walk", "Blue Window", "Paper Planes", "Night Bus"]
result = songs.append("Garden Song")
print(result)
print(len(songs))
```

What does the program print?

A. `None`, then `5`
B. The whole new list, then `5`
C. `None`, then `4`
D. An error, because the result of `append()` cannot be stored in a variable

## Question 4

<!-- item: Q4 | outcome: LO-3 | difficulty: standard -->

In `playlist.py`, "Garden Song" has been added, so `songs` holds Sunrise Walk, Blue Window, Paper Planes, Night Bus, and Garden Song, in that order. A student wants to drop "Blue Window", which sits at index 1, and writes this line:

```python
songs.remove(1)
```

A `ValueError` is the error Python raises when a method gets a value it cannot use. What happens when Python runs the line?

A. It removes "Blue Window", because 1 is the index of that song.
B. It removes "Sunrise Walk", because `remove()` counts positions from 1.
C. It does nothing and the list stays the same, because no song is named 1.
D. It raises a `ValueError`, because `remove()` looks for an item equal to 1 and no item is equal to 1.

## Question 5

<!-- item: Q5 | outcome: LO-5 | difficulty: standard -->

**Requirement:** The four starting titles in line 1 are the specification and may not be edited. The program must still add "Garden Song" and remove "Blue Window" by name, and it must run to the end with no error. Python runs lines from top to bottom, and an error stops the program at the line that causes it, so no later line runs.

A student saves this version of `playlist.py`. The numbers at the left are the file's line numbers and are not part of the code. The file has no blank lines and no comments.

```text
1  songs = ["Sunrise Walk", "Blue Window", "Paper Planes", "Night Bus"]
2  songs.append("Garden Song")
3  songs.remove("Blue Windows")
4  print("Songs:", len(songs))
5  print("First song:", songs[0])
```

The student runs the file. The screen shows no `Songs:` line and no `First song:` line, and Python reports an error.

1. Name the type of error Python reports.
2. Name the line number where the error happens.
3. Say why neither `print()` line shows anything, and say what the student should change to meet the requirement.

## Question 6

<!-- item: Q6 | outcome: LO-4 | difficulty: basic -->

`playlist.py` has a loop over the Question 1 list that starts like this:

```python
for song in songs:
    print(song)
```

The loop body runs once for each song. What does the loop variable `song` hold the second time the body runs?

A. `1`, the index of the second song
B. `2`, the number of the pass
C. "Blue Window", the second item in the list
D. "Sunrise Walk", because the variable keeps the first song until the loop ends

## Question 7

<!-- item: Q7 | outcome: LO-4 | difficulty: standard -->

**Requirement:** The lab's expected-output block numbers the songs counting from 1, so the first song line starts with 1 and the last starts with 4.

A student writes this numbering loop for `playlist.py`. At this point `songs` holds Sunrise Walk, Paper Planes, Night Bus, and Garden Song, in that order.

```python
number = 0
for song in songs:
    print(number, song)
    number = number + 1
```

Working through the code by hand gives this output:

```text
0 Sunrise Walk
1 Paper Planes
2 Night Bus
3 Garden Song
```

Does the output meet the requirement, and why?

A. It meets the requirement, because every number goes up by exactly one with no repeats.
B. It does not meet the requirement, because the numbers start at 0 and the requirement starts at 1.
C. It meets the requirement, because index 0 is the first song, so 0 is the right label for it.
D. It does not meet the requirement, because Garden Song is missing from the output.

## Question 8

<!-- item: Q8 | outcome: LO-1 | difficulty: stretch -->

**Transfer.** A student keeps homework in a list instead of songs. The program starts with this line:

```python
tasks = ["Read chapter 3", "Math worksheet", "Essay draft"]
```

Write the lines that come after it so the program prints exactly the output below and nothing else. The program must add "Science quiz" to the end of the list, remove "Math worksheet" by name, then print the count, the first task, and every task numbered from 1. Use a `for` loop and a counter variable. Do not use `if`, `enumerate()`, or `range()`.

```text
Tasks: 3
First task: Read chapter 3
1 Read chapter 3
2 Essay draft
3 Science quiz
```

## Predict and reflect

**Predict.** Before you run the lab step that turns on the starter's `remove()` line, write what you expect to see on the screen, and whether the two `print()` lines below it will show anything.

**Reflect.** After the step, write what actually happened and whether your prediction held.
Neither answer is graded for being right.
