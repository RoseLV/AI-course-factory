---
course: intro-python-lists-hs
stage: 04-labs
module: 01
author: lab-engineer
date: 2026-11-03
outcomes: LO-1, LO-2, LO-3, LO-4, LO-5
---

# Build playlist.py: keep a class playlist in a Python list

## What problem this lab solves

**Purpose:** This lab trains you to build a small Python program, `playlist.py`, that keeps your class playlist in one list. You add a song, drop a song by name, and show the playlist numbered.

**Context:** Without lists, a program that holds four songs needs four separate variables, such as `song1`, `song2`, `song3`, and `song4`. Adding a fifth song means writing a fifth variable and changing every line that uses them. A list keeps all the songs in one place, in order, so one `for` loop can handle every song (SP-0.12).

**Core skill being trained:** Changing a list with a method, then checking the result against a written specification instead of trusting that the code looks right.

The class's request, in the class's words: "Keep our class playlist in one program. It starts with four songs, adds one, drops one by name, then shows how many songs there are, which song is first, and every song numbered."

The learner will be able to:

- Build `playlist.py` so that its output matches the expected-output block exactly (LO-1)
- Print the first song by its index and the song count with `len()` (LO-2)
- Change a list with `append()` and `remove()`, and say what each one changes (LO-3)
- Write a `for` loop that prints every song numbered from 1, using a counter you design (LO-4)
- Debug a `ValueError` raised by `remove()` by reading the error line and correcting the song name (LO-5)

**Final deliverable:** A file named `playlist.py`. When you run it, it prints the lab's expected-output block (six lines) and nothing else. A classmate or your teacher can check it by running the file and comparing the two outputs line by line.

## How the steps work together

| Step | Title | Minutes |
| --- | --- | --- |
| 0 | Set up and verify | 5 |
| 1 | Print the count and the first song | 5 |
| 2 | Add a song with append() | 4 |
| 3 | Remove a song by name and fix the ValueError | 6 |
| 4 | Print every song numbered | 6 |
| 5 | Debrief | 3 |

Step times sum to 29 minutes against the module's 29 hands-on minutes in the syllabus.

## Guidance and tools

**Primary tooling:** Python 3.15.2, the current release on 2026-11-03 (SP-0.1). Every list operation in this lab works the same way in Python 3.11 to 3.15 (SP-0.2, SP-0.3). You need a text editor to save `playlist.py`, or a browser editor that your teacher names. On Windows the run command is `python` (SP-0.14).

**Key concepts from the lecture:**

- A **list** keeps items in order inside square brackets. An **item** is one value in the list.
- An **index** is an item's position, counted from 0, so the first song is `songs[0]` (SP-1.1). The last index of a four-item list is 3, and index 4 raises an `IndexError`, the error Python gives when an index does not exist (SP-1.2).
- A **method** is a function you call with a dot after the list, such as `songs.append("x")`. `len(songs)` gives the number of items (SP-1.3).
- `append()` adds one item to the end and returns `None`, so it is called alone on its own line (SP-1.4).
- `remove()` deletes the first item equal to the value you give. It matches by value, not by position. If nothing matches, Python stops with a `ValueError`, the error for a value that is not acceptable here (SP-1.5, SP-0.6).
- A **`for` loop** gives the **loop variable** each item in order, not each index (SP-1.6). A **counter** is a variable you change yourself, for example `number = number + 1`, to count how many times something happened.
- `print()` with commas between its values prints them on one line with a space between them.
- An **error** is Python's report that it could not run a line. It stops the program at that line.

**Not used in this lab:** `if` checks, `enumerate()`, `range()`, `try`, and `except`. Do not add them.

### Planted defect (read this before you run anything)

**Planted defect:** The starter file `playlist.py` holds a `remove()` line, `songs.remove("Blue Windows")`, that names a song which is not in the list. The list holds `"Blue Window"`, with no `s`. The line starts as a comment so it stays quiet until Step 3.

**Requirement it violates:** The specification has two parts. The first part is the four starting titles in the starter file, which include "Blue Window". The second part is the expected-output block below, whose six lines show a program that ends with four songs and no error after one song is added and one is removed. `remove()` can only drop a title that matches an item exactly. A name that is one letter off breaks that rule (SP-1.5).

**Source of truth:** A written specification: the expected-output block in this guide and the four starting titles in the starter file. Fix the name in the `remove()` line. Do not change the list to match the typo.

### Starter file

Save this as `playlist.py`. Lines that start with `#` are comments, which Python ignores.

```python
# playlist.py: the class playlist
# Spec: start with four songs, add one, drop one by name,
# then show the count, the first song, and every song numbered.

songs = ["Sunrise Walk", "Blue Window", "Paper Planes", "Night Bus"]

# Step 2: add "Garden Song" to the end of the list here.

# Step 3: remove "Blue Window" here. The line below is the starter's attempt.
# songs.remove("Blue Windows")

# Step 1: print the count and the first song here.

# Step 4: print every song numbered here.

print("setup ok")
```

### Expected output

This is the specification for the finished program. Read it before Step 1. A correct `playlist.py` prints these six lines and nothing else.

```text
Songs: 4
First song: Sunrise Walk
1 Sunrise Walk
2 Paper Planes
3 Night Bus
4 Garden Song
```

You can work this out by hand. The list starts with four songs. Adding "Garden Song" makes five. Removing "Blue Window" leaves four: Sunrise Walk, Paper Planes, Night Bus, Garden Song. The count is 4, the first song is Sunrise Walk, and the numbered lines run 1 to 4 in list order.

### Finished file

This is one correct finished version. Do not open it until you have tried Step 4 yourself, because you design the counter. Other counter designs are fine if the output matches. Use this file to compare in Step 5.

```python
# playlist.py: the class playlist
# Spec: start with four songs, add one, drop one by name,
# then show the count, the first song, and every song numbered.

songs = ["Sunrise Walk", "Blue Window", "Paper Planes", "Night Bus"]

songs.append("Garden Song")

songs.remove("Blue Window")

print("Songs:", len(songs))
print("First song:", songs[0])

number = 1
for song in songs:
    print(number, song)
    number = number + 1
```

### Step 0 - Set up and verify

**Purpose:** Get a place to write and run `playlist.py` and confirm it runs.
**Time:** 5 minutes

Choose one path.

**Path A, Python on your computer:**

1. Open a text editor and paste the starter file from the Starter file section above.
2. Save it as `playlist.py` in a folder you can find again.
3. Open a terminal in that folder and run this command to check Python is installed.

```text
python --version
```

4. Look for a line that starts with `Python 3`. Python 3.11 or later works. This lab was written against 3.15.2.
5. Run the starter.

```text
python playlist.py
```

**Path B, a browser editor:**

1. Open the browser editor your teacher names. Make a new Python file.
2. Paste the starter file into it and name it `playlist.py` if the editor asks for a name.
3. Press the run button. The editor's Python version was not checked for this guide, but the list operations here work in 3.11 to 3.15 (SP-0.3).

**Pass:** The only output is one line, `setup ok`. **Fail:** nothing prints, or an error appears. See the Troubleshooting table at the end.

If you cannot install Python on your device, use Path B.

> Unexecuted teaching sample: no one has run this step.

### Step 1 - Print the count and the first song

**Purpose:** Show how many songs are in the list and which one is first.
**Time:** 5 minutes
**Starting state:** `playlist.py` is the starter file. Running it prints `setup ok`. The list `songs` holds four songs.
**Task:** Under the comment `# Step 1`, add two `print()` lines. The first prints `Songs:` and the count from `len(songs)`. The second prints `First song:` and the first song, found by its index. Delete the `print("setup ok")` line at the bottom, because the final program prints nothing else.
**Prediction:** Before you run, write down the exact two lines you expect to see. Write down which index holds the first song.
**Action:**

1. Under `# Step 1`, type this line.

```python
print("Songs:", len(songs))
```

2. On the next line, type this line.

```python
print("First song:", songs[0])
```

3. Delete the line `print("setup ok")`.
4. Save the file and run it.

```text
python playlist.py
```

**Evidence:** Passing output is two lines: `Songs: 4` and `First song: Sunrise Walk`. Failing output, first case: the second line shows `Blue Window`. That means you used index 1, the second song. Failing output, second case: the run stops with an `IndexError`. The last line of the error starts with `IndexError`, and it names the line that holds your index. In a browser editor the error may appear in a panel; find the error type in it. That means you used an index of 4 or more, and a four-item list stops at index 3. Failing output, third case: a third line, `setup ok`, appears. Delete that line.
**Interpretation:** A pass proves you can read the first item by index 0 and count items with `len()`. It does not prove the list is correct after changes, because nothing has changed it yet. Next, change the list.
**Recovery:** If you see an error, read its last line for the error type, then read the line number it names and open that line in your file. Check that you typed `songs`, not `song`, and that every quote and bracket has a partner. To reset, paste the starter file again and redo this step.
**Why this matters:** An index counts from 0, and `len()` counts from 1. Seeing a count of 4 next to a first index of 0 is the quickest way to feel the difference, and the quiz and the loop in Step 4 both depend on it.

> Unexecuted teaching sample: no one has run this step.

### Step 2 - Add a song with append()

**Purpose:** Change the list by adding one song to the end.
**Time:** 4 minutes
**Starting state:** `playlist.py` has the list and your two print lines from Step 1. Running it prints `Songs: 4` and `First song: Sunrise Walk`.
**Task:** Under the comment `# Step 2`, add one line that appends `"Garden Song"` to `songs`. It must sit above your print lines so the count sees the new song.
**Prediction:** Before you run, write down the count you expect and the first song you expect. Write down whether `append()` changes the first song.
**Action:**

1. Under `# Step 2`, type this line.

```python
songs.append("Garden Song")
```

2. Save the file and run it.

```text
python playlist.py
```

**Evidence:** Passing output is `Songs: 5` and `First song: Sunrise Walk`. Failing output, first case: `Songs: 4`. The append line is missing, or it sits below the print lines, so the count ran before the song was added. Failing output, second case: a line that says `None`. You wrote `print(songs.append("Garden Song"))`. `append()` changes the list and returns `None`, so printing its result shows `None` (SP-1.4).
**Interpretation:** A pass proves `append()` changed the list itself and put the new song at the end. The first song stayed the same because `append()` adds to the end. It does not prove the new song is last. Step 4 will show that. Next, remove a song.
**Recovery:** If the count is still 4, check the order of your lines: the append must come before the prints. If you see `None`, call `append()` alone on its own line. To reset, delete your append line and redo it.
**Why this matters:** A method changes the list in place, so the order of your lines decides what later lines see. A line that works alone can still give the wrong answer in the wrong place.

> Unexecuted teaching sample: no one has run this step.

### Step 3 - Remove a song by name and fix the ValueError

**Purpose:** Remove "Blue Window" by name and debug the error the starter's `remove()` line causes.
**Time:** 6 minutes
**Starting state:** `playlist.py` has the list, your append line, and your two print lines. Under `# Step 3` is the commented line `# songs.remove("Blue Windows")`. Running the file prints `Songs: 5` and `First song: Sunrise Walk`.
**Task:** Turn on the starter's `remove()` line and run it. Read the error. Correct the name so `remove()` drops "Blue Window" and the run reaches the end with no error.
**Prediction:** Before you run, write down three things. First, what you expect to see when you turn on the starter's line exactly as written. Second, whether the two print lines below it will print anything. Third, which line of the file you expect Python to name. Use the requirement stated above: the list holds `"Blue Window"`.
**Action:**

1. Under `# Step 3`, delete the `#` and the space at the start of the `songs.remove("Blue Windows")` line, so it is live code. Do not change the name yet.
2. Save the file and run it.

```text
python playlist.py
```

3. Read the last line of the error. Write down the error type and the line number it names.
4. Open that line in your file. Compare the name in quotes with the title in the list, letter by letter.
5. Correct the name in the `remove()` line to `"Blue Window"`. Leave the list alone.
6. Save the file and run it again.

```text
python playlist.py
```

**Evidence:** Failing output (step 2): no `Songs:` line and no `First song:` line appear. The last line of the error starts with `ValueError`, and the error names the line that holds `songs.remove`. In a browser editor the error may appear in a panel; find the error type in it. The two print lines never ran, because Python stops at the failing line (SP-1.5). The exact message text after `ValueError` is not checked here. Read the type and the line, not the wording (SP-U1). Passing output (step 6) is two lines: `Songs: 4` and `First song: Sunrise Walk`. The count dropped from 5 to 4 because `remove()` deleted one song.
**Interpretation:** A pass proves `remove()` matched "Blue Window" by value and deleted it. It does not prove the song removed was the right one, only that the count is down by one. If you see `Songs: 5` with no error, check that the line is live and that the name matches. If a different `ValueError` line appears, compare the name with the list again. The error pointed at the line, and the line holds the typo. Next, show every song.
**Recovery:** If the run still stops with `ValueError`, the name still does not match the list. Check capital letters, spaces, and the missing `s`. Do not add an `if` check and do not edit the list. If the count is 5 and no error appears, the `#` is still on the line. If you are lost, paste the starter file again and redo Steps 1 to 3.
**Why this matters:** `remove()` takes a value, not a position, and it does not guess. When it finds no match, the whole program stops and everything after the line is lost, even code that was correct. Reading the error type and line number is how you find a typo in seconds instead of guessing.

> Unexecuted teaching sample: no one has run this step.

**Planted defect:** The starter's `songs.remove("Blue Windows")` line names a song not in the list. **Requirement it violates:** the expected-output block says four songs remain, with "Blue Window" gone and no error. **Source of truth:** a written specification, the expected-output block and the four starting titles.

### Step 4 - Print every song numbered

**Purpose:** Print each song on its own line with a number that starts at 1.
**Time:** 6 minutes
**Starting state:** `playlist.py` runs to the end with no error and prints `Songs: 4` and `First song: Sunrise Walk`. The list holds Sunrise Walk, Paper Planes, Night Bus, and Garden Song, in that order.
**Task:** Under `# Step 4`, write a `for` loop that prints every song with its number. The numbers must run 1, 2, 3, 4. You design the counter: its name, its starting value, and the line where it goes up by one. Use no `enumerate()` and no `range()`.
**Prediction:** Before you write code, answer these on paper. First, what name will your counter have? Second, what value does it start at, and why? Third, does it go up by one before or after the `print()` line? Fourth, what do you expect the last four lines of output to be?
**Action:**

1. Above the loop, create your counter variable and give it a starting value.
2. Write a `for` loop over `songs`. Name the loop variable `song`.
3. Inside the loop, print the counter and then the song, with a comma between them.
4. Inside the loop, add one to the counter on its own line, for example `number = number + 1` if your counter is named `number`.
5. Save the file and run it.

```text
python playlist.py
```

**Evidence:** Passing output is six lines, the whole expected-output block. The last four lines are `1 Sunrise Walk`, `2 Paper Planes`, `3 Night Bus`, and `4 Garden Song`. Failing output, first case: the numbers run 0 to 3. The counter starts at 0 and goes up after the print. Failing output, second case: the numbers run 2 to 5. The counter starts at 1 but goes up before the print. Failing output, third case: every line shows the same number. The counter never goes up, or the line that adds one sits outside the loop. Failing output, fourth case: the lines show a number and no song. You printed the counter twice or printed a number where the song should be.
**Interpretation:** A pass proves your counter logic and shows that `for song in songs` gives each item, in list order. The new song sits last, as `append()` promised. It does not prove your design is the only right one: a counter that starts at 0 and goes up before the print also passes. Next, compare the full run in the debrief. When the checked run passes, you may swap in your own song titles as an extension. That extension is not checked against the expected-output block.
**Recovery:** Check the indent. The lines inside the loop must start four spaces to the right of the `for` line. If the lines are not indented, Python reports an error about the indent and names the line. If your numbers are wrong, change the start value or move the add-one line, then run again. To reset, delete the loop and counter lines and begin Step 4 again.
**Why this matters:** The `for` loop gives you each song but never its position, so numbering needs a variable you manage yourself. Deciding where it starts and where it goes up is the part of the program you designed, and a wrong start gives a printout that looks fine but is off by one.

> Unexecuted teaching sample: no one has run this step.

### Step 5 - Debrief

**Purpose:** Run the finished program against the expected-output block and name what you learned.
**Time:** 3 minutes

1. Run the program one last time.

```text
python playlist.py
```

2. Compare your output with the Expected output block, line by line. A pass is six lines that match exactly, with nothing before or after.
3. Compare your code with the Finished file. Differences in the counter's name or design are fine if the output matches.

> Unexecuted teaching sample: no one has run this step.

- What exists now: `playlist.py` creates a list of four songs, appends one with `append()`, removes one by name with `remove()`, prints the count with `len()`, prints the first song by index, and prints every song numbered 1 to 4 with a `for` loop and your counter. It runs to the end with no error. It is the whole capstone.
- The prediction to watch: in Step 3, many learners predict that the two print lines still run before the error. They do not. The print lines sit below the `remove()` line, and Python stops at the failing line, so nothing prints. The reason is that Python runs lines top to bottom and an error ends the run.
- The planted defect and its source of truth: the starter's `songs.remove("Blue Windows")` names a song that is not in the list, so `remove()` raises a `ValueError`. The source of truth is a written specification: the expected-output block and the four starting titles. The fix was to correct the name, not to change the list.
- What the next module picks up: this is the only module of the course, so `playlist.py` is the capstone end state. A natural next step is a later session on `if` checks, which would let a program test a song name before removing it.
- What this lab did not cover: other list methods such as `insert` and `sort`, negative indexes, removing items while looping over the same list (a known trap, SP-1.8), and reading song titles from the user.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `python` is not recognised or not found | Python is not installed, or the command differs on your computer | On Windows the recommended command is `python` (SP-0.14). Ask your teacher which command your computer uses, or switch to Path B |
| Step 0 prints nothing | You saved the file without running it, or you ran a different file | Check the file name is `playlist.py` and that you are in the same folder, then run it again |
| The error mentions the indent | A line inside the loop is not indented, or the indent is uneven | Start every line inside the loop four spaces to the right of the `for` line |
| `IndexError` on the first-song line | You used an index of 4 or more on a four-item list | Use index 0 for the first song (SP-1.1, SP-1.2) |
| `ValueError` at the `remove()` line | The name in `remove()` does not match an item exactly | Compare it letter by letter with the list, then fix the name in the `remove()` line (SP-1.5) |
| `Songs: 5` after Step 3 and no error | The `remove()` line is still a comment | Delete the `#` at the start of the line |
| A line that says `None` | You printed the result of `append()` | Call `append()` alone on its own line (SP-1.4) |
| Numbers start at 0 or 2 | The counter starts at the wrong value, or goes up in the wrong place | Match the start value to where you add one: start at 1 and add one after the print |
| An extra line `setup ok` | The Step 0 line is still at the bottom of the file | Delete the `print("setup ok")` line |
| Output is right but has a different count after you changed song titles | You are on the unchecked extension | Compare against the expected-output block only with the original titles |
