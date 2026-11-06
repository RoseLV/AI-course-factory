---
course: intro-python-lists-hs
stage: 02-deck
module: 01
author: deck-writer
date: 2026-11-03
outcomes: LO-1, LO-2, LO-3, LO-4, LO-5
---

# Build playlist.py: keep a class playlist in a Python list

## Slide 1: Today playlist.py grows from a one-line check into a full playlist
- Start: four songs, prints only setup ok
- End: six lines of output, no error
- Five lab steps get you there
Visual: Before and after boxes: the starter prints one line, the finished file prints six.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="40" y="100" width="300" height="160" rx="10" class="box"/>
  <text x="190" y="165" text-anchor="middle" class="label label-strong">Starter</text>
  <text x="190" y="205" text-anchor="middle" class="label label-mono">prints: setup ok</text>
  <path d="M356,180 L446,180" class="connector" marker-end="url(#arrow-muted)"/>
  <rect x="460" y="100" width="300" height="160" rx="10" class="box-accent"/>
  <text x="610" y="165" text-anchor="middle" class="label label-strong">Finished</text>
  <text x="610" y="205" text-anchor="middle" class="label">prints six lines</text>
</svg>
```
Notes: The class asked for one program that keeps its playlist. Right now the starter holds four song titles in a list, which is Python's way of keeping items in order between square brackets. It prints one check line, setup ok. By the end, the same file adds a song, drops a song by name, and prints the count, the first song, and every song numbered. You judge success by comparing your output with the lab's expected-output block, line by line. That block is the specification: the written description of exactly what the program must print. We never judge by whether the code looks right. One line in the starter is wrong on purpose. We will find it by reading an error message.
Covers: LO-1

## Slide 2: One list replaces four separate variables
- Four variables: song1 to song4
- One list: all songs in one place
- One loop (code that repeats) handles every song
- CSTA 3A-AP-14 asks for this (SP-0.12)
Visual: Four separate variable boxes on the left, one list box on the right.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="40" y="50" width="200" height="50" rx="8" class="box"/>
  <text x="140" y="82" text-anchor="middle" class="label label-mono">song1</text>
  <rect x="40" y="120" width="200" height="50" rx="8" class="box"/>
  <text x="140" y="152" text-anchor="middle" class="label label-mono">song2</text>
  <rect x="40" y="190" width="200" height="50" rx="8" class="box"/>
  <text x="140" y="222" text-anchor="middle" class="label label-mono">song3</text>
  <rect x="40" y="260" width="200" height="50" rx="8" class="box"/>
  <text x="140" y="292" text-anchor="middle" class="label label-mono">song4</text>
  <path d="M260,180 L446,180" class="connector" marker-end="url(#arrow-muted)"/>
  <rect x="460" y="90" width="300" height="180" rx="10" class="box-accent"/>
  <text x="610" y="170" text-anchor="middle" class="label label-mono">songs</text>
  <text x="610" y="205" text-anchor="middle" class="label label-sm">one name, four items</text>
  <text x="140" y="360" text-anchor="middle" class="label label-sm">Four names to manage</text>
  <text x="610" y="360" text-anchor="middle" class="label label-sm">One name to manage</text>
</svg>
```
Notes: A list is a value that keeps items in order, written between square brackets with commas. An item is one value inside it. Why bother? With four variables, a fifth song needs a new variable and a change to every line that uses them. With a list, adding a song changes one line, and one loop, which is code that repeats, handles every song the same way. The CSTA standard 3A-AP-14 says to use lists instead of repeated simple variables (SP-0.12). A quick check you can run on any program: how many lines must change to add one more song? If the answer is more than one, the program wants a list.
Covers: LO-1

## Slide 3: The starter stores four song titles in one list
```python
songs = ["Sunrise Walk", "Blue Window", "Paper Planes", "Night Bus"]
print("setup ok")
```
Notes: Each title is a string, which is text between quotes. The four strings sit between square brackets, separated by commas, and the whole list is stored in the variable songs with an equals sign, as you already do for numbers. Running this file prints only setup ok. The real starter file also holds comment lines that begin with a hash mark. Python ignores comments, so they mark where each lab step goes. One of them hides the wrong remove line, which stays quiet until Step 3. To judge a list line, check three things: brackets in pairs, quotes in pairs, and commas between titles. A missing comma is the usual typo.
Covers: LO-1

## Slide 4: An index counts from zero, so the first song is songs[0]
- Index: a position, counted from 0 (SP-1.1)
- It is the distance from the start
- First song: songs[0]
- Four items means indexes 0 to 3
Visual: Four list cells, each labelled with its index from 0 to 3.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <text x="120" y="160" text-anchor="middle" class="label label-lg">0</text>
  <text x="300" y="160" text-anchor="middle" class="label label-lg">1</text>
  <text x="480" y="160" text-anchor="middle" class="label label-lg">2</text>
  <text x="660" y="160" text-anchor="middle" class="label label-lg">3</text>
  <rect x="40" y="180" width="160" height="90" rx="8" class="box-accent"/>
  <text x="120" y="232" text-anchor="middle" class="label">Sunrise Walk</text>
  <rect x="220" y="180" width="160" height="90" rx="8" class="box"/>
  <text x="300" y="232" text-anchor="middle" class="label">Blue Window</text>
  <rect x="400" y="180" width="160" height="90" rx="8" class="box"/>
  <text x="480" y="232" text-anchor="middle" class="label">Paper Planes</text>
  <rect x="580" y="180" width="160" height="90" rx="8" class="box"/>
  <text x="660" y="232" text-anchor="middle" class="label">Night Bus</text>
  <text x="400" y="360" text-anchor="middle" class="label label-sm">The index is how far an item sits from the start</text>
</svg>
```
Notes: An index is an item's position, counted as the distance from the start. The first item is zero steps from the start, so its index is 0, and songs[0] reads it (SP-1.1). Everyday counting starts at one, which is why the common wrong answer is songs[1] for the first song. That expression gives Blue Window, the second title. Square brackets after a list name, with a number inside, pick one item. This list has four items, so the valid indexes are 0, 1, 2, and 3. To judge any answer, point at the first title and ask how many titles come before it. The answer is the index.
Covers: LO-2

## Slide 5: len() counts the items and songs[0] reads the first one
```python
print("Songs:", len(songs))
print("First song:", songs[0])
```
Notes: len is a function, a named tool you call with parentheses and give a value, like print. Calling len(songs) returns the number of items, which is 4 here (SP-1.3). Notice the pair: the count is 4, but the last index is 3. The count is always one more than the last index. The print lines use commas, so each prints its text, a space, then the value. These two lines print Songs: 4 and then First song: Sunrise Walk. You can check that by hand, with no run: four titles, and the first one is Sunrise Walk. Two wrong answers to watch for are Songs: 3, from mixing up count and index, and Blue Window, from using index 1.
Covers: LO-2

## Slide 6: An index past the end stops the program with an IndexError
```python
print("First song:", songs[4])
```
Notes: An error is Python's report that it could not run a line. The program stops at that line. This line asks for index 4, but a four-item list has indexes 0 to 3, so Python raises an IndexError, the error for an index that does not exist (SP-1.2). You read an error for two facts: the error type and the line number it names. We have not captured the exact message wording, so read the type and the line, not the sentence. This is the off-by-one mistake: counting titles from one, so the last index is taken to be four. Fix it by using index 0 for the first.
Covers: LO-2

## Slide 7: Mechanism: a method changes the list in place and returns None
- Method: a function called with a dot
- songs.append("x") adds to the end
- It changes songs itself (SP-1.4)
- It returns None, meaning nothing back
Visual: A list grows from four to five items while the returned value is None.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="40" y="80" width="300" height="110" rx="10" class="box"/>
  <text x="190" y="130" text-anchor="middle" class="label label-mono">songs</text>
  <text x="190" y="162" text-anchor="middle" class="label label-sm">4 items</text>
  <text x="400" y="118" text-anchor="middle" class="label label-sm">append</text>
  <path d="M356,140 L446,140" class="connector" marker-end="url(#arrow-muted)"/>
  <rect x="460" y="80" width="300" height="110" rx="10" class="box-accent"/>
  <text x="610" y="130" text-anchor="middle" class="label label-mono">songs</text>
  <text x="610" y="162" text-anchor="middle" class="label label-sm">5 items, Garden Song last</text>
  <rect x="250" y="290" width="300" height="100" rx="10" class="box dashed"/>
  <text x="400" y="332" text-anchor="middle" class="label label-sm">value handed back</text>
  <text x="400" y="364" text-anchor="middle" class="label label-mono">None</text>
</svg>
```
Notes: A method is a function that belongs to a value and is called with a dot, as in songs.append. The change it makes happens to the list itself, in place: append adds the item at the end (SP-0.6). A method that only changes a list, such as append, returns None, which is Python's value meaning nothing was handed back (SP-1.4). The common wrong answer is x = songs.append("Garden Song"), then expecting x to hold the list. It holds None, while songs holds the new item. To judge your code, call append alone on its own line. Then check the list with len or a loop.
Covers: LO-3

## Slide 8: The append line goes on its own line, above the lines that count
```python
songs.append("Garden Song")
print("Songs:", len(songs))
```
Notes: Order matters because Python runs lines from top to bottom. The append line sits above the print, so the print sees five songs and shows Songs: 5. If the append sat below the print, the count would run first and show Songs: 4, a result that looks fine but misses the new song. Predict before you run: what is the first song now? Sunrise Walk, because append adds at the end and never touches the front. Judge the step by the count, five, not by whether the code ran without an error.
Covers: LO-3

## Slide 9: remove() deletes by value, never by position
- remove("Blue Window") searches by title
- It deletes the first match only (SP-1.5)
- remove(1) does not mean position 1
- No match raises a ValueError
Visual: The list loses Blue Window after remove, and a missing title stops the program.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="40" y="70" width="300" height="120" rx="10" class="box"/>
  <text x="190" y="120" text-anchor="middle" class="label label-mono">songs</text>
  <text x="190" y="155" text-anchor="middle" class="label label-sm">5 items, Blue Window inside</text>
  <text x="400" y="108" text-anchor="middle" class="label label-sm">remove</text>
  <path d="M356,130 L446,130" class="connector" marker-end="url(#arrow-muted)"/>
  <rect x="460" y="70" width="300" height="120" rx="10" class="box-accent"/>
  <text x="610" y="120" text-anchor="middle" class="label label-mono">songs</text>
  <text x="610" y="155" text-anchor="middle" class="label label-sm">4 items, Blue Window gone</text>
  <rect x="150" y="290" width="500" height="100" rx="10" class="box dashed"/>
  <text x="400" y="332" text-anchor="middle" class="label label-sm">No item equals the name: ValueError</text>
  <text x="400" y="364" text-anchor="middle" class="label label-sm">The program stops at that line</text>
</svg>
```
Notes: Remove works with a value, not a position. remove compares the value you give with each item from the front, using exact equality, and deletes the first match only (SP-0.6, SP-1.5). Exact means capital letters, spaces, and every letter. When nothing matches, Python does not ignore it. It raises a ValueError, the error for a value that is not acceptable here, and the program stops. Two wrong answers appear often: that remove(1) deletes position 1, and that a missing song is harmless. After the removal, the songs behind it shift left, so Paper Planes moves from index 2 to index 1 (SP-1.8, a secondary source).
Covers: LO-3

## Slide 10: The starter's remove line names a song that is not in the list
- Spec: titles fixed; four songs remain, no error
- Source: lab's starting titles and expected output
```python
songs = ["Sunrise Walk", "Blue Window", "Paper Planes", "Night Bus"]
songs.append("Garden Song")
songs.remove("Blue Windows")
print("Songs:", len(songs))
print("First song:", songs[0])
```
Notes: Run this and the program prints nothing: neither print line appears. It reaches the remove line, finds no title equal to Blue Windows, and raises a ValueError on that line. The error ends the run, so the two print lines below never execute. The spec, the lab's expected-output block, wants four songs and no error, so this starter fails it. Many learners predict that the prints still show; ask the room to commit to an answer first. The list holds Blue Window; the line asks for Blue Windows. We name the error type and the line, and we do not quote the message text, because nobody has captured it on the current Python yet (SP-U1).
Covers: LO-3, LO-5

## Slide 11: Diagnostic sequence: no output and a ValueError point at the name
- Spec: titles fixed; four songs remain, no error
- Source: lab's starting titles and expected output
- Symptom: no output, error type ValueError
- Check: letter by letter finds an extra s
Visual: Symptom leads to the check, which leads to the conclusion.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="130" width="220" height="170" rx="10" class="box"/>
  <text x="140" y="180" text-anchor="middle" class="label label-strong">Symptom</text>
  <text x="140" y="220" text-anchor="middle" class="label label-sm">no program output</text>
  <text x="140" y="250" text-anchor="middle" class="label label-sm">error type: ValueError</text>
  <path d="M256,215 L284,215" class="connector" marker-end="url(#arrow-muted)"/>
  <rect x="290" y="130" width="220" height="170" rx="10" class="box-accent"/>
  <text x="400" y="180" text-anchor="middle" class="label label-strong">Check</text>
  <text x="400" y="220" text-anchor="middle" class="label label-sm">name against list,</text>
  <text x="400" y="250" text-anchor="middle" class="label label-sm">letter by letter</text>
  <path d="M516,215 L544,215" class="connector" marker-end="url(#arrow-muted)"/>
  <rect x="550" y="130" width="220" height="170" rx="10" class="box"/>
  <text x="660" y="180" text-anchor="middle" class="label label-strong">Conclusion</text>
  <text x="660" y="220" text-anchor="middle" class="label label-sm">extra s in the name</text>
  <text x="660" y="250" text-anchor="middle" class="label label-sm">fix the name only</text>
  <text x="400" y="380" text-anchor="middle" class="label label-sm">Ruled out: misspelled list, a different failing line</text>
</svg>
```
Notes: Start from the symptom: the program printed nothing and the error names a ValueError. Three causes fit. First, the name in remove differs from the list item. Second, the list itself is misspelled. Third, a different line failed first. The check that separates them is to compare the quoted name with the list, letter by letter, and with the specification. The names differ by one s, so cause one holds. The spec says titles are fixed, and the lab's four starting titles include Blue Window, so the list is right, and cause two fails. The error names the remove line itself, so cause three fails. Conclusion: correct the name in remove and leave the list alone.
Covers: LO-5

## Slide 12: Correcting the name lets the run reach the end
- Spec: titles fixed; four songs remain, no error
- Source: lab's starting titles and expected output
```python
songs = ["Sunrise Walk", "Blue Window", "Paper Planes", "Night Bus"]
songs.append("Garden Song")
songs.remove("Blue Window")
print("Songs:", len(songs))
print("First song:", songs[0])
```
Notes: Compare this with the failing version: one letter changed. Python now finds an item equal to Blue Window, deletes it, and the run reaches the print lines. The output has two lines, Songs: 4 and First song: Sunrise Walk. The count fell from five to four because remove deleted one item. The first song did not change because the removed title was the second, not the first. This pass proves remove matched by value. It does not prove the right song left, only that the count fell by one. The numbered list in the next steps will let us check the survivors. The spec wants four songs and no error, and this run gives both so far.
Covers: LO-3, LO-5

## Slide 13: A for loop hands you each item in order, not each index
- Loop: code that repeats
- for song in songs: runs once per song
- Loop variable song holds the current item
- Order matches the list (SP-1.6)
Visual: Four list cells visited in order, one pass per song.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <text x="120" y="135" text-anchor="middle" class="label label-sm">pass 1</text>
  <text x="300" y="135" text-anchor="middle" class="label label-sm">pass 2</text>
  <text x="480" y="135" text-anchor="middle" class="label label-sm">pass 3</text>
  <text x="660" y="135" text-anchor="middle" class="label label-sm">pass 4</text>
  <rect x="40" y="150" width="160" height="90" rx="8" class="box-accent"/>
  <text x="120" y="202" text-anchor="middle" class="label">Sunrise Walk</text>
  <rect x="220" y="150" width="160" height="90" rx="8" class="box"/>
  <text x="300" y="202" text-anchor="middle" class="label">Paper Planes</text>
  <rect x="400" y="150" width="160" height="90" rx="8" class="box"/>
  <text x="480" y="202" text-anchor="middle" class="label">Night Bus</text>
  <rect x="580" y="150" width="160" height="90" rx="8" class="box"/>
  <text x="660" y="202" text-anchor="middle" class="label">Garden Song</text>
  <text x="400" y="320" text-anchor="middle" class="label label-sm">On pass 1, song holds Sunrise Walk</text>
  <text x="400" y="360" text-anchor="middle" class="label label-sm">On pass 4, song holds Garden Song</text>
</svg>
```
Notes: A loop is code that repeats. The for loop repeats its indented lines once for each item in a list. The loop variable, here song, is the name that holds the current item on each pass. The tutorial says the for statement walks the items of a sequence in the order they appear (SP-0.5, SP-1.6). So pass one has song equal to Sunrise Walk, and pass four has Garden Song. The wrong answer is that song counts 0, 1, 2, 3. It holds titles, not positions. The name song is our choice, and any name works. Judge a loop by asking what the variable holds on pass one.
Covers: LO-4

## Slide 14: Printing the loop variable shows every song in list order
```python
for song in songs:
    print(song)
```
Notes: Assume the append and remove lines ran above. The output is four lines, in list order: Sunrise Walk, Paper Planes, Night Bus, Garden Song. Garden Song is last because append adds at the end. Blue Window is gone because remove deleted it before the loop starts. Notice the indent: the print line sits four spaces to the right of the for line, which tells Python it belongs to the loop. An unindented print would be an error. The output has no numbers, because the loop gives us items and never positions. Predict what we need to add.
Covers: LO-4

## Slide 15: A counter you manage yourself gives the numbers
- Counter: a variable you change to count
- Start at 1, print, then add 1
- number = number + 1 adds one
- The order of these lines decides the output
Visual: A counter is set once, then printed and increased on every pass.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="40" width="300" height="80" rx="10" class="box"/>
  <text x="400" y="88" text-anchor="middle" class="label label-mono">number = 1</text>
  <path d="M400,126 L400,174" class="connector" marker-end="url(#arrow-muted)"/>
  <rect x="250" y="180" width="300" height="80" rx="10" class="box-accent"/>
  <text x="400" y="228" text-anchor="middle" class="label label-mono">print(number, song)</text>
  <path d="M400,266 L400,314" class="connector" marker-end="url(#arrow-muted)"/>
  <rect x="250" y="320" width="300" height="80" rx="10" class="box"/>
  <text x="400" y="368" text-anchor="middle" class="label label-mono">number = number + 1</text>
  <path d="M556,360 L620,360 L620,220 L556,220" class="connector" marker-end="url(#arrow-muted)"/>
  <text x="640" y="295" class="label label-sm">repeat</text>
  <text x="640" y="320" class="label label-sm">per song</text>
</svg>
```
Notes: A counter is a variable that you change yourself to keep count. We need one because the loop never hands us a position. The recipe has three parts: set number to 1 before the loop, print it with the song, then add one at the end of each pass. We start at 1 because a numbered playlist starts at 1, while index 0 would print the first song as zero. Trace pass one by hand: print 1 Sunrise Walk, then number becomes 2. Judge the design by the last line: its number should equal the count, 4.
Covers: LO-4

## Slide 16: The numbered loop prints 1 Sunrise Walk through 4 Garden Song
```python
number = 1
for song in songs:
    print(number, song)
    number = number + 1
```
Notes: Trace it by hand. Before the loop, number is 1. Pass one prints 1 Sunrise Walk, then number becomes 2. Pass two prints 2 Paper Planes. Pass three prints 3 Night Bus. Pass four prints 4 Garden Song, and number ends at 5, which is never printed. Those four lines are lines three to six of the expected output. Two details matter. The line number = 1 sits above the for line, so it runs once; inside the loop it would reset on every pass and print 1 four times. And both indented lines start four spaces in, so both repeat.
Covers: LO-4

## Slide 17: Where the counter starts and changes decides the numbers
- Start 0, add after print: 0 to 3
- Start 1, add before print: 2 to 5
- Start 1, add after print: 1 to 4
- Only the last matches the specification
Visual: Three counter designs with the numbers each prints, the correct one highlighted.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="40" y="50" width="720" height="80" rx="10" class="box"/>
  <text x="70" y="98" class="label">start 0, add after the print</text>
  <text x="730" y="98" text-anchor="end" class="label label-mono">0 to 3</text>
  <rect x="40" y="160" width="720" height="80" rx="10" class="box"/>
  <text x="70" y="208" class="label">start 1, add before the print</text>
  <text x="730" y="208" text-anchor="end" class="label label-mono">2 to 5</text>
  <rect x="40" y="270" width="720" height="80" rx="10" class="box-accent"/>
  <text x="70" y="318" class="label">start 1, add after the print</text>
  <text x="730" y="318" text-anchor="end" class="label label-mono">1 to 4</text>
  <text x="400" y="420" text-anchor="middle" class="label label-sm">Specification: the numbers run 1 to 4</text>
</svg>
```
Notes: The counter is the part you design, and the design can be wrong while the program still runs. Trace each version by hand. Start at 0 and add after the print: the numbers are 0, 1, 2, 3. Start at 1 and add before the print: the first print already sees 2, so 2 to 5. Start at 1 and add after the print: 1 to 4, which matches the specification. Both wrong versions look tidy, and neither raises an error. Only the written specification catches them, because the spec says 1 to 4.
Covers: LO-4

## Slide 18: Trap: removing songs inside a loop over the same list skips items
- Removal shifts later items one place left
- The loop still moves forward one place
- The shifted item can be skipped (SP-1.8)
- Remove outside the loop, as we did
Visual: Removing B while the loop stands on B leaves C unvisited.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="60" y="50" width="140" height="70" rx="8" class="box"/>
  <text x="130" y="94" text-anchor="middle" class="label">A</text>
  <rect x="230" y="50" width="140" height="70" rx="8" class="box-accent"/>
  <text x="300" y="94" text-anchor="middle" class="label">B</text>
  <rect x="400" y="50" width="140" height="70" rx="8" class="box"/>
  <text x="470" y="94" text-anchor="middle" class="label">C</text>
  <rect x="570" y="50" width="140" height="70" rx="8" class="box"/>
  <text x="640" y="94" text-anchor="middle" class="label">D</text>
  <text x="400" y="200" text-anchor="middle" class="label label-sm">The loop stands on B (position 1) and removes it</text>
  <text x="400" y="245" text-anchor="middle" class="label label-sm">The list becomes A, C, D</text>
  <text x="400" y="290" text-anchor="middle" class="label label-sm">The loop moves to position 2, which holds D</text>
  <text x="400" y="335" text-anchor="middle" class="label label-sm">C is never visited</text>
</svg>
```
Notes: This is a trap to name, not a skill to practise. If a loop removes items from the list it is walking over, later items shift one place left, while the loop still moves one place forward. The item that slid into the gap is never visited, so the loop can skip it (SP-1.8). The Python tutorial warns that changing a collection while looping over it can be tricky to get right. Our program is safe because it removes once, before the loop starts. The wrong belief is that removing in a loop works like removing items one by one.
Covers: LO-3

## Slide 19: The finished playlist.py is nine lines of code
```python
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
Notes: Read the file as five blocks, top to bottom. The list, the append, the remove, the two print lines, and the numbered loop. Each block is one lab step, and the order matters: the append and remove run before the prints, so the prints see the final four songs. This is one correct version. A different counter name or start value is fine if the output matches the specification. Your lab job is to write the pieces yourself, then compare with this file in Step 5. Do not copy it first, because the counter is the part you design.
Covers: LO-1

## Slide 20: Worked example: the finished file checked against the expected output
- Spec: the lab's expected-output block, six lines
- Input: the finished playlist.py
- Command: python playlist.py
- Verdict: predicted to match; the lab run confirms
Visual: The expected-output block beside the output traced by hand from the code, with the verdict below.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="20" width="350" height="300" rx="10" class="box"/>
  <text x="205" y="55" text-anchor="middle" class="label label-strong">Expected output (spec)</text>
  <text x="60" y="100" class="label label-mono">Songs: 4</text>
  <text x="60" y="136" class="label label-mono">First song: Sunrise Walk</text>
  <text x="60" y="172" class="label label-mono">1 Sunrise Walk</text>
  <text x="60" y="208" class="label label-mono">2 Paper Planes</text>
  <text x="60" y="244" class="label label-mono">3 Night Bus</text>
  <text x="60" y="280" class="label label-mono">4 Garden Song</text>
  <rect x="420" y="20" width="350" height="300" rx="10" class="box"/>
  <text x="595" y="55" text-anchor="middle" class="label label-strong">Traced from the code</text>
  <text x="450" y="100" class="label label-mono">Songs: 4</text>
  <text x="450" y="136" class="label label-mono">First song: Sunrise Walk</text>
  <text x="450" y="172" class="label label-mono">1 Sunrise Walk</text>
  <text x="450" y="208" class="label label-mono">2 Paper Planes</text>
  <text x="450" y="244" class="label label-mono">3 Night Bus</text>
  <text x="450" y="280" class="label label-mono">4 Garden Song</text>
  <rect x="30" y="360" width="740" height="110" rx="10" class="box-accent"/>
  <text x="400" y="408" text-anchor="middle" class="label label-strong">Verdict: six of six lines predicted to match</text>
  <text x="400" y="445" text-anchor="middle" class="label label-sm">Right column traced by hand, not a captured run</text>
</svg>
```
Notes: The source of truth is the lab's expected-output block, shown on the slide. Trace the input by hand. Four songs, plus Garden Song, makes five. Removing Blue Window leaves four: Sunrise Walk, Paper Planes, Night Bus, Garden Song. So len gives 4, songs[0] gives Sunrise Walk, and the loop numbers 1 to 4. The right column is traced from the code, not a captured run, because nobody has run it for this deck. So the verdict is a prediction until you run it in the lab and compare line by line. It follows from the spec as written: six lines, nothing before or after. A leftover setup ok line, or a first line numbered 0, would fail.
Covers: LO-1

## Slide 21: The capstone now meets its specification, and the lab builds it
- playlist.py now meets the whole specification
- Each lab step adds one piece
- Step 5 compares your run with the spec
- Extension: your own titles, unchecked
Visual: Four build steps feed the final comparison against the six expected lines.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="40" y="50" width="340" height="70" rx="10" class="box"/>
  <text x="210" y="93" text-anchor="middle" class="label">Step 1: count and first song</text>
  <rect x="40" y="140" width="340" height="70" rx="10" class="box"/>
  <text x="210" y="183" text-anchor="middle" class="label">Step 2: append Garden Song</text>
  <rect x="40" y="230" width="340" height="70" rx="10" class="box"/>
  <text x="210" y="273" text-anchor="middle" class="label">Step 3: remove, fix the name</text>
  <rect x="40" y="320" width="340" height="70" rx="10" class="box"/>
  <text x="210" y="363" text-anchor="middle" class="label">Step 4: numbered loop</text>
  <path d="M396,220 L446,220" class="connector" marker-end="url(#arrow-muted)"/>
  <rect x="460" y="130" width="300" height="180" rx="10" class="box-accent"/>
  <text x="610" y="205" text-anchor="middle" class="label label-strong">Step 5</text>
  <text x="610" y="240" text-anchor="middle" class="label label-sm">compare with the six lines</text>
</svg>
```
Notes: Here is where the capstone stands. playlist.py holds four songs in a list, adds Garden Song, removes Blue Window by name, prints the count and the first song, and prints every song numbered from 1. It meets the whole specification, so a classmate can check it by running the file and comparing six lines. The starter stopped at the remove line with a ValueError, and we fixed the name rather than the list, because the written spec decided which side was wrong. In the lab you will build each piece, predict before you run, and compare at Step 5.
Covers: LO-1, LO-5

## Slide 22: Glossary for this module
- Index: a position, counted from 0 (slide 4)
- Counter: variable you change to count (slide 15)
- IndexError: no item at that position (slide 6)
- ValueError: no item equals the value (slide 9)
Visual: A table of the ten terms with one plain sentence and the first slide each appears on.
```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="20" width="740" height="460" rx="10" class="box"/>
  <text x="50" y="60" class="label label-sm label-strong">list</text>
  <text x="200" y="60" class="label label-sm">Items kept in order between square brackets</text>
  <text x="740" y="60" text-anchor="end" class="label label-sm">slide 1</text>
  <text x="50" y="102" class="label label-sm label-strong">item</text>
  <text x="200" y="102" class="label label-sm">One value inside a list</text>
  <text x="740" y="102" text-anchor="end" class="label label-sm">slide 2</text>
  <text x="50" y="144" class="label label-sm label-strong">index</text>
  <text x="200" y="144" class="label label-sm">An item's position, counted from 0</text>
  <text x="740" y="144" text-anchor="end" class="label label-sm">slide 4</text>
  <text x="50" y="186" class="label label-sm label-strong">method</text>
  <text x="200" y="186" class="label label-sm">A function called with a dot after a value</text>
  <text x="740" y="186" text-anchor="end" class="label label-sm">slide 7</text>
  <text x="50" y="228" class="label label-sm label-strong">error</text>
  <text x="200" y="228" class="label label-sm">Python's report that it could not run a line</text>
  <text x="740" y="228" text-anchor="end" class="label label-sm">slide 6</text>
  <text x="50" y="270" class="label label-sm label-strong">IndexError</text>
  <text x="200" y="270" class="label label-sm">The error for an index that does not exist</text>
  <text x="740" y="270" text-anchor="end" class="label label-sm">slide 6</text>
  <text x="50" y="312" class="label label-sm label-strong">ValueError</text>
  <text x="200" y="312" class="label label-sm">The error when remove finds no matching value</text>
  <text x="740" y="312" text-anchor="end" class="label label-sm">slide 9</text>
  <text x="50" y="354" class="label label-sm label-strong">for loop</text>
  <text x="200" y="354" class="label label-sm">Code that repeats once for each item</text>
  <text x="740" y="354" text-anchor="end" class="label label-sm">slide 13</text>
  <text x="50" y="396" class="label label-sm label-strong">loop variable</text>
  <text x="200" y="396" class="label label-sm">The name holding the current item each pass</text>
  <text x="740" y="396" text-anchor="end" class="label label-sm">slide 13</text>
  <text x="50" y="438" class="label label-sm label-strong">counter</text>
  <text x="200" y="438" class="label label-sm">A variable you change yourself to count</text>
  <text x="740" y="438" text-anchor="end" class="label label-sm">slide 15</text>
</svg>
```
Notes: Ten terms, all defined earlier. Two pairs get confused most. First, index and count. The index is a position that starts at 0, and the count from len is how many items there are, so the last index is always one less than the count. Second, item and loop variable: an item lives in the list, while the loop variable is a name that refers to one item during one pass. Also keep the two errors apart. IndexError means a position does not exist, and ValueError, from remove, means the value was not found.
Covers: LO-2, LO-3, LO-4, LO-5
