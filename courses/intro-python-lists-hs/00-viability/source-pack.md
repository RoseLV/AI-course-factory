---
course: intro-python-lists-hs
stage: 00-viability
module: n/a
author: research-analyst
date: 2026-11-03
outcomes: n/a
---

# Source pack: Intro to Python lists

Pass 1 writes the claims the viability brief cites, as `SP-0.n`. Pass 2, after Gate 0, adds the
module claims `SP-1.n`, `SP-2.n` and the sections below. One entry per claim. Never cite a source
you did not open.

## Open findings

Unsourced claims: 2. Each is listed below under the `SP-U` series (SP-U1, SP-U2).

Not verified in pass 2:

- Stack Overflow could not be opened (the fetch tool refuses the domain) and python-forum.io returned HTTP 403. The misconceptions table therefore cites discuss.python.org, the Treehouse community forum, and one blog article instead.
- Nothing was run. No Python interpreter output is quoted, so exact error message text on 3.15.2 is not verified (SP-U1).

Not verified in pass 1, and not relied on by the brief:

- Whether the AP Create performance task program must itself contain a list. The College Board PDFs that state this could not be read as text.
- The official CSTA wording of 3A-AP-14 from the CSTA document itself. SP-0.12 relies on Code.org's alignment page.
- The national share of US high schools offering computer science in Code.org's 2025 report.
- Whether Khan Academy's Python course has a lists unit, and the current CodeHS Python course structure.

## Canonical sources

| Source | URL | Version covered | Opened |
| --- | --- | --- | --- |
| Python downloads page | https://www.python.org/downloads/ | 3.15.2 | 2026-11-03 |
| Python devguide, status of Python versions | https://devguide.python.org/versions/ | 3.11 to 3.16 | 2026-11-03 |
| Python tutorial, an informal introduction | https://docs.python.org/3/tutorial/introduction.html | 3.15.2 | 2026-11-03 |
| Python tutorial, more control flow tools | https://docs.python.org/3/tutorial/controlflow.html | 3.15.2 | 2026-11-03 |
| Python tutorial, data structures | https://docs.python.org/3/tutorial/datastructures.html | 3.15.2 | 2026-11-03 |
| Python tutorial, data structures (3.11) | https://docs.python.org/3.11/tutorial/datastructures.html | 3.11.18 | 2026-11-03 |
| Using Python on Windows | https://docs.python.org/3/using/windows.html | 3.15.2 | 2026-11-03 |
| TIOBE index | https://www.tiobe.com/tiobe-index/ | October 2026 | 2026-11-03 |
| Stack Overflow Developer Survey 2026, technology | https://survey.stackoverflow.co/2026/technology | 2026 | 2026-11-03 |
| Stack Overflow Developer Survey 2025, technology | https://survey.stackoverflow.co/2025/technology | 2025 | 2026-11-03 |
| GitHub Octoverse 2026 | https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/ | 2026 report | 2026-11-03 |
| AP Computer Science Principles assessment (College Board) | https://apstudents.collegeboard.org/courses/ap-computer-science-principles/assessment | 2026-27 exam | 2026-11-03 |
| Code.org CS Principles Unit 5 standards alignment | https://curriculum.code.org/csp-20/unit5/standards/ | CSTA 2017 standards | 2026-11-03 |
| CSTA interactive standards | https://csteachers.org/k12standards/interactive/ | CSTA 2017 standards | 2026-11-03 |
| Chromebook Help, set up Linux | https://support.google.com/chromebook/answer/9145439 | n/a | 2026-11-03 |
| W3Schools Python Lists | https://www.w3schools.com/python/python_lists.asp | n/a | 2026-11-03 |
| Codecademy Learn Python 3 | https://www.codecademy.com/learn/learn-python-3 | Python 3.13 course | 2026-11-03 |
| Codecademy pricing | https://www.codecademy.com/pricing | n/a | 2026-11-03 |
| Khan Academy blog, Intro to CS with Python | https://blog.khanacademy.org/introducing-khan-academys-new-intro-to-computer-science-course-with-python | post dated 2024-08-15 and 2025-03-20 | 2026-11-03 |
| Khan Academy blog, Python course for high school teachers | https://blog.khanacademy.org/empower-your-students-with-our-python-course-for-high-school-teachers | post dated 2025-09-09 | 2026-11-03 |
| CS50's Introduction to Programming with Python | https://cs50.harvard.edu/python/ | n/a | 2026-11-03 |
| CS50P Week 2 notes | https://cs50.harvard.edu/python/notes/2/ | n/a | 2026-11-03 |
| Python for Everybody, home | https://www.py4e.com/ | n/a | 2026-11-03 |
| Python for Everybody, lessons | https://www.py4e.com/lessons | n/a | 2026-11-03 |
| Python library reference, built-in functions | https://docs.python.org/3/library/functions.html | 3.15.2 | 2026-11-03 |
| Python library reference, built-in exceptions | https://docs.python.org/3/library/exceptions.html | 3.15.2 | 2026-11-03 |
| discuss.python.org, beginner IndexError thread | https://discuss.python.org/t/beginner-level-getting-an-error-indexerror-list-index-out-of-range-in-a-tutorial-program/21026 | forum thread | 2026-11-03 |
| discuss.python.org, append method not working | https://discuss.python.org/t/append-method-not-working/25583 | forum thread | 2026-11-03 |
| Treehouse community, list.remove ValueError | https://teamtreehouse.com/community/statesremoveblue-it-is-saying-valueerror-listremovex-x-not-in-list | forum thread | 2026-11-03 |
| Hacker Noon, deleting while looping skips elements | https://hackernoon.com/why-deleting-items-from-a-list-while-looping-silently-skips-elements | blog article | 2026-11-03 |

## Claims

### SP-0.1

- **Claim:** On 2026-11-03, python.org lists Python 3.15.2, dated 25 October 2026, as the latest Python 3 release.
- **Mechanism:** The Python release team publishes every release on the downloads page and puts the newest Python 3 release at the top, so that page is the reference for the current stable version.
- **Source:** https://www.python.org/downloads/, the latest release button and the "Active Python releases" table
- **Version:** 3.15.2
- **Opened:** 2026-11-03
- **Serves:** course level: Python version for the syllabus and lab Step 0

### SP-0.2

- **Claim:** Python 3.11, 3.12, 3.13, 3.14, and 3.15 were each first released in October of consecutive years from 2022 to 2026, 3.16 is scheduled for 2027-10-06, and the devguide says support ends five years after a release.
- **Mechanism:** Each version follows a release schedule set out in a PEP (Python Enhancement Proposal, a design document), and the devguide tracks each branch from feature, to bugfix, to security, to end of life. A new version every October means any version number in course text ages by one step a year.
- **Source:** https://devguide.python.org/versions/, "Supported versions" table and the status descriptions
- **Version:** 3.11 to 3.15, and main (3.16)
- **Opened:** 2026-11-03
- **Serves:** course level: durability risk

### SP-0.3

- **Claim:** Section 5.1 of the Python tutorial documents the same 11 list methods, in the same order from `append` to `copy`, in both the 3.11 and the 3.15 documentation.
- **Mechanism:** Each documentation version describes the list type as it exists in that release, so matching method lists in the oldest and newest supported versions mean the course's list operations work in both. The visible difference is notation: 3.15 writes `list.append(value, /)` where 3.11 writes `append(x)`.
- **Source:** https://docs.python.org/3/tutorial/datastructures.html and https://docs.python.org/3.11/tutorial/datastructures.html, section 5.1 "More on Lists" in each
- **Version:** 3.15.2 and 3.11.18
- **Opened:** 2026-11-03
- **Serves:** course level: durability risk, capstone fit

### SP-0.4

- **Claim:** The Python 3.15 tutorial introduces lists in section 3.1.3, inside its first informal chapter, as comma-separated values between square brackets, and shows indexing (index 0 returns the first item), slicing, `append()`, and `len()` on lists there.
- **Mechanism:** A list is a sequence type, like a string, so the indexing and slicing rules learners have just met for text carry over to lists. The tutorial says lists "can be indexed and sliced" like all other built-in sequence types.
- **Source:** https://docs.python.org/3/tutorial/introduction.html, section 3.1.3 "Lists"
- **Version:** 3.15.2
- **Opened:** 2026-11-03
- **Serves:** course level: audience fit, capstone

### SP-0.5

- **Claim:** Python's `for` statement visits the items of a list one at a time in the order they appear, and the tutorial's first `for` example loops over a list of words.
- **Mechanism:** The tutorial says the `for` statement "iterates over the items of any sequence (a list or a string), in the order that they appear in the sequence." A list keeps its items in order, so the loop body runs once per item, first to last.
- **Source:** https://docs.python.org/3/tutorial/controlflow.html, section 4.2 "for Statements"
- **Version:** 3.15.2
- **Opened:** 2026-11-03
- **Serves:** course level: audience fit, capstone

### SP-0.6

- **Claim:** `list.append()` adds an item to the end of a list, and `list.remove()` deletes the first item equal to the given value or raises a `ValueError` if no item matches.
- **Mechanism:** Both methods change the list in place. `remove()` searches from the front and stops at the first match; when nothing matches, Python reports the problem with an error instead of silently doing nothing.
- **Source:** https://docs.python.org/3/tutorial/datastructures.html, section 5.1, the `list.append` and `list.remove` entries
- **Version:** 3.15.2
- **Opened:** 2026-11-03
- **Serves:** course level: capstone and its planted defect

### SP-0.7

- **Claim:** In the October 2026 TIOBE index, Python ranks first with a rating of 19.23 percent, a change of minus 5.23 points from October 2025, when it also ranked first.
- **Mechanism:** TIOBE builds its ratings from search engine counts of skilled engineers, courses, and third-party vendors for each language, so the rating tracks visibility, not quality. The page states the index "is not about the best programming language."
- **Source:** https://www.tiobe.com/tiobe-index/, main ranking table, Python row
- **Version:** October 2026 index
- **Opened:** 2026-11-03
- **Serves:** course level: demand signals

### SP-0.8

- **Claim:** In the 2026 Stack Overflow Developer Survey, 58.0 percent of all respondents reported using Python, ranking it fourth behind JavaScript, SQL, and HTML/CSS.
- **Mechanism:** The survey asks which languages respondents used for any reason, and the percentage is the share of all respondents (n = 16,241 for that question) who chose Python. Respondents are self-selected and self-reporting.
- **Source:** https://survey.stackoverflow.co/2026/technology, "Most popular technologies", languages, All Respondents
- **Version:** 2026 survey
- **Opened:** 2026-11-03
- **Serves:** course level: demand signals

### SP-0.9

- **Claim:** In the 2025 Stack Overflow Developer Survey, 57.9 percent of all respondents used Python, ranking it fourth, after a seven percentage point increase from 2024.
- **Mechanism:** The survey repeats the same language question each year, so the yearly shares compare like for like. The 2025 page itself states the seven-point increase.
- **Source:** https://survey.stackoverflow.co/2025/technology, programming, scripting, and markup languages, All Respondents
- **Version:** 2025 survey
- **Opened:** 2026-11-03
- **Serves:** course level: demand signals

### SP-0.10

- **Claim:** GitHub's Octoverse 2026 report ranks TypeScript first and Python second by monthly contributors, and says Python added 3.23 million monthly contributors between September 2025 and September 2026.
- **Mechanism:** Octoverse counts monthly contributors on GitHub by language, so it measures activity on one platform rather than all developer use. A language can gain millions of contributors and still lose rank if another grows faster.
- **Source:** https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/, language rankings section
- **Version:** Octoverse 2026, published 2026-10-28
- **Opened:** 2026-11-03
- **Serves:** course level: demand signals

### SP-0.11

- **Claim:** On the AP Computer Science Principles exam, Written Response 2(c), part of Section II (30 percent of the score), assesses developing data abstraction using lists to store multiple elements and writing iteration statements to traverse a list.
- **Mechanism:** The College Board names the learning objectives each written response can assess (here AAP-1.D.a and AAP-2.O.a), and students answer about the program they built for the Create performance task. List skills are therefore tested on the student's own code.
- **Source:** https://apstudents.collegeboard.org/courses/ap-computer-science-principles/assessment, "Written Response 2(c): Data and Procedural Abstraction"
- **Version:** 2026-27 exam (exam date 2027-05-14)
- **Opened:** 2026-11-03
- **Serves:** course level: recommendation, audience fit

### SP-0.12

- **Claim:** CSTA K-12 Computer Science Standard 3A-AP-14 reads "Use lists to simplify solutions, generalizing computational problems instead of repeated use of simple variables."
- **Mechanism:** The standard names the reason lists exist: one list replaces many separate variables, so the same code can process every value. Code.org maps several lessons of its lists unit to this standard.
- **Source:** https://curriculum.code.org/csp-20/unit5/standards/, alignment list for Unit 5 "Lists, Loops, and Traversals" (a secondary source quoting the CSTA standards)
- **Version:** CSTA K-12 standards, revised 2017
- **Opened:** 2026-11-03
- **Serves:** course level: recommendation, audience fit

### SP-0.13

- **Claim:** CSTA describes standards level 3A as grades 9 to 10, "high school core."
- **Mechanism:** CSTA groups its standards into grade bands, and a standard's ID prefix names its band. A standard that starts with 3A, such as 3A-AP-14, belongs to the grades 9 to 10 band.
- **Source:** https://csteachers.org/k12standards/interactive/, level descriptions
- **Version:** CSTA K-12 standards, revised 2017
- **Opened:** 2026-11-03
- **Serves:** course level: recommendation, audience fit

### SP-0.14

- **Claim:** For Python 3.15 on Windows, the documentation recommends the Python install manager and the `python` command, and says the traditional full installer, deprecated as of 3.14, will not be produced for 3.16 or later.
- **Mechanism:** The install manager can hold several Python runtimes; `python` runs the default one and `py` picks a version. The older installer is being retired in its favour, so setup steps written for it will expire with 3.16.
- **Source:** https://docs.python.org/3/using/windows.html, opening sections on the Python install manager
- **Version:** 3.15.2
- **Opened:** 2026-11-03
- **Serves:** course level: durability risk, capstone check command, lab Step 0

### SP-0.15

- **Claim:** Google's Chromebook Help says a Chromebook used at work or school might not be able to use Linux.
- **Mechanism:** On managed devices, the page sends users to their administrator, so the school's settings, not the student, decide whether a local Python install through Linux is possible.
- **Source:** https://support.google.com/chromebook/answer/9145439, "Set up Linux on your Chromebook"
- **Version:** n/a
- **Opened:** 2026-11-03
- **Serves:** course level: audience fit, lab Step 0

### SP-0.16

- **Claim:** W3Schools' Python Lists chapter is a text tutorial with "Try it Yourself" editor links, 12 sub-pages from accessing items to list methods, exercises, and a code challenge, with no price shown for the tutorial and no stated audience level.
- **Mechanism:** The chapter is built as reference pages, one list operation per page, each with runnable examples. The site advertises a paid PLUS upgrade separately from the free pages.
- **Source:** https://www.w3schools.com/python/python_lists.asp, page body and the left menu under Python Lists
- **Version:** n/a
- **Opened:** 2026-11-03
- **Serves:** course level: competitor scan

### SP-0.17

- **Claim:** Codecademy's Learn Python 3 is a beginner course with no prerequisites, an estimated 24 hours, 14 lessons, 14 projects, and 13 quizzes, with separate Lists and Loops modules, and it teaches Python 3.13.
- **Mechanism:** Codecademy publishes the syllabus and an average completion time on the course page. The time estimate comes from combined completion rates, so individual pace varies.
- **Source:** https://www.codecademy.com/learn/learn-python-3, course overview and syllabus
- **Version:** Python 3.13 course
- **Opened:** 2026-11-03
- **Serves:** course level: competitor scan

### SP-0.18

- **Claim:** Codecademy's pricing page shows Basic at $0, Plus at $11.99 a month billed annually ($14.99 billed monthly), and Pro at $15.99 a month billed annually ($19.99 billed monthly), with assessments and certificates not available on Basic.
- **Mechanism:** Codecademy offers a free tier with limited course access and sells projects, assessments, and certificates through paid plans.
- **Source:** https://www.codecademy.com/pricing, plan cards and feature comparison
- **Version:** prices as shown on 2026-11-03
- **Opened:** 2026-11-03
- **Serves:** course level: competitor scan, durability risk

### SP-0.19

- **Claim:** Khan Academy's Intro to Computer Science course in Python is free, project-based, and runs in a browser-based development environment that works on laptops, tablets, and phones.
- **Mechanism:** Because the editor runs in the browser, students need no local install, which avoids restrictions on school devices.
- **Source:** https://blog.khanacademy.org/introducing-khan-academys-new-intro-to-computer-science-course-with-python, feature list and sign-up line
- **Version:** post showing dates 2024-08-15 and 2025-03-20
- **Opened:** 2026-11-03
- **Serves:** course level: competitor scan, audience fit

### SP-0.20

- **Claim:** Khan Academy's post for high school teachers says students in its Python course practise conditionals, loops, and functions, with over 100 example programs.
- **Mechanism:** Khan pitches the course for a full-year computer science class or for coding inside another subject, so it covers the whole beginner sequence rather than one topic.
- **Source:** https://blog.khanacademy.org/empower-your-students-with-our-python-course-for-high-school-teachers
- **Version:** post dated 2025-09-09
- **Opened:** 2026-11-03
- **Serves:** course level: competitor scan

### SP-0.21

- **Claim:** CS50's Introduction to Programming with Python runs from Week 0 to Week 9, each week with a lecture and a problem set, is free through Harvard's OpenCourseWare site, and is designed for students with or without prior programming experience.
- **Mechanism:** Harvard publishes the lectures and problem sets openly and offers paid certificates through edX, so the course content itself costs nothing.
- **Source:** https://cs50.harvard.edu/python/, home page
- **Version:** n/a (no edition stated on the page)
- **Opened:** 2026-11-03
- **Serves:** course level: competitor scan

### SP-0.22

- **Claim:** CS50P introduces lists inside its Week 2 "Loops" notes, in the "For Loops" section.
- **Mechanism:** The course presents the list as the thing a `for` loop walks through, so lists arrive as part of loops rather than as a topic of their own.
- **Source:** https://cs50.harvard.edu/python/notes/2/, "For Loops" section
- **Version:** n/a
- **Opened:** 2026-11-03
- **Serves:** course level: competitor scan

### SP-0.23

- **Claim:** Python for Everybody is a free open course under a Creative Commons Attribution 4.0 licence, with video lectures, an online book, and autograded assignments, and its lessons page lists Lists as lesson 9 of 17, after Files.
- **Mechanism:** The site publishes its materials under an open licence and on GitHub for others to reuse. Its lessons run in a fixed order, so learners reach lists only after strings and files.
- **Source:** https://www.py4e.com/ (licence and formats) and https://www.py4e.com/lessons (lesson order)
- **Version:** n/a
- **Opened:** 2026-11-03
- **Serves:** course level: competitor scan

### SP-1.1

- **Claim:** In a Python list the first item has index 0, so `squares[0]` returns the first item of the list `squares`.
- **Mechanism:** An index counts how far an item sits from the start, so the first item is zero steps away. The tutorial says lists are indexed "like strings", and its string section gives the first character index 0.
- **Source:** https://docs.python.org/3/tutorial/introduction.html, sections 3.1.2 "Text" and 3.1.3 "Lists"
- **Version:** 3.15.2
- **Opened:** 2026-11-03
- **Serves:** module 1: indexing, the first song printed by index

### SP-1.2

- **Claim:** Using an index that does not exist in a list raises `IndexError`, so a list of four items accepts indexes 0 to 3 (and -1 to -4), and index 4 fails.
- **Mechanism:** Python checks every subscript against the list's current length. The exceptions page says `IndexError` is "raised when a sequence subscript is out of range." The 0 to 3 range follows from SP-1.1 and SP-1.3, and the negative range from the tutorial's `squares[-1]` example (my derivation, not a quoted sentence).
- **Source:** https://docs.python.org/3/library/exceptions.html, the `IndexError` entry; the beginner thread at https://discuss.python.org/t/beginner-level-getting-an-error-indexerror-list-index-out-of-range-in-a-tutorial-program/21026 shows `while i <= len(List1)` failing for this reason
- **Version:** 3.15.2
- **Opened:** 2026-11-03
- **Serves:** module 1: off-by-one errors, index errors

### SP-1.3

- **Claim:** `len()` returns the number of items in a list, so a list of four songs gives `len(songs)` equal to 4, which is one more than the last index.
- **Mechanism:** `len()` counts items, and indexes start at 0, so the last valid index is always `len(songs) - 1`. The tutorial shows `len(letters)` returning 4 for a four-item list.
- **Source:** https://docs.python.org/3/library/functions.html, `len()` entry; https://docs.python.org/3/tutorial/introduction.html, section 3.1.3
- **Version:** 3.15.2
- **Opened:** 2026-11-03
- **Serves:** module 1: printing the count with `len()`

### SP-1.4

- **Claim:** `list.append(value)` changes the list in place and returns `None`, so `x = songs.append("Song")` makes `x` equal to `None`, and `songs` still holds the new item.
- **Mechanism:** The tutorial says methods that only modify a list, such as `insert`, `remove`, or `sort`, return the default `None`, a design rule for mutable data structures. The change is the side effect, not the return value.
- **Source:** https://docs.python.org/3/tutorial/datastructures.html, section 5.1, `list.append` entry and the note on methods with no return value
- **Version:** 3.15.2
- **Opened:** 2026-11-03
- **Serves:** module 1: `append()`, traps when printing its result

### SP-1.5

- **Claim:** `list.remove(value)` removes the first item equal to the given value, not the item at a position, and raises `ValueError` when no top-level item equals it.
- **Mechanism:** `remove()` compares the value with each item from the front using equality. A value that appears only inside a nested list is not a top-level item, so it is not found. A Treehouse thread shows `remove('blue')` failing when `'blue'` sat inside a nested list.
- **Source:** https://docs.python.org/3/tutorial/datastructures.html, section 5.1, `list.remove` entry; https://teamtreehouse.com/community/statesremoveblue-it-is-saying-valueerror-listremovex-x-not-in-list
- **Version:** 3.15.2 (documentation); the forum thread shows no version
- **Opened:** 2026-11-03
- **Serves:** module 1: `remove()` and the planted defect (removing a song not in the list)

### SP-1.6

- **Claim:** A `for` loop over a list gives the loop variable each item in list order, not each index, so `for song in songs:` sets `song` to the first song, then the second, to the last.
- **Mechanism:** The `for` statement asks the list for its items in sequence. The tutorial contrasts it with C or Pascal, where the loop counts numbers. If the loop needs a number, the learner adds a counter or uses an index.
- **Source:** https://docs.python.org/3/tutorial/controlflow.html, section 4.2 "for Statements" (the `words` example prints `cat 3`, `window 6`, `defenestrate 12`)
- **Version:** 3.15.2
- **Opened:** 2026-11-03
- **Serves:** module 1: `for` loop over a list

### SP-1.7

- **Claim:** `enumerate(songs)` pairs each item with a count that starts at 0 by default, and `enumerate(songs, start=1)` starts the count at 1, which gives a numbered list for display.
- **Mechanism:** `enumerate` takes an optional `start` argument, whose default is 0, and adds it to a running count. The tutorial says that `range(len(a))` with `a[i]` also works but that `enumerate()` is usually more convenient. Whether the capstone may use `enumerate` is a course decision, not a fact.
- **Source:** https://docs.python.org/3/library/functions.html, `enumerate()` entry; https://docs.python.org/3/tutorial/controlflow.html, section 4.3 "The range() Function"
- **Version:** 3.15.2
- **Opened:** 2026-11-03
- **Serves:** module 1: printing every song numbered 1 to 4 rather than 0 to 3

### SP-1.8

- **Claim:** The Python tutorial warns that code which changes a collection while looping over that same collection "can be tricky to get right", and a loop that removes list items can skip the item after each removal.
- **Mechanism:** Removing an item shifts every later item one place left, while the loop's position still moves forward, so the item that slid into the vacated place is never visited. The skip appears only in some data, such as matching items side by side, so tests can pass by luck. The mechanism text comes from the Hacker Noon article, a secondary source.
- **Source:** https://docs.python.org/3/tutorial/controlflow.html, section 4.2; https://hackernoon.com/why-deleting-items-from-a-list-while-looping-silently-skips-elements
- **Version:** 3.15.2
- **Opened:** 2026-11-03
- **Serves:** module 1: a trap to name when learners combine `remove()` with a loop (mention depth)

### SP-U1

- **Claim:** The exact text of the `ValueError` message from `remove()` on Python 3.15.2.
- **Mechanism:** Not established. The Treehouse thread shows `list.remove(x): x not in list`, but its Python version is unknown, and the official documentation names the exception without giving the message.
- **Source:** none for 3.15.2. I could not run Python in this task.
- **Version:** unknown
- **Opened:** 2026-11-03
- **Serves:** module 1: lab Step evidence for the failing run. The lab author must run the starter and paste the real message, or mark it a reconstruction.

### SP-U2

- **Claim:** What `print(songs)` shows for a list of strings, including whether it prints brackets, quotes, and commas.
- **Mechanism:** Not established. The tutorial shows bracketed lists only in the interactive interpreter display and gives no `print()` rule for lists. I did not find an official page that states it.
- **Source:** none opened
- **Version:** unknown
- **Opened:** 2026-11-03
- **Serves:** module 1: the capstone does not need this if each song is printed on its own line. Do not teach the output shape of `print(songs)` until it is sourced or run.

### Capstone output, interpretation (mine, derived from SP-1.1 to SP-1.7)

For `songs` with four items, after one `append()` and one `remove()`, a correct `playlist.py` should show: the count from `len(songs)`, the item at `songs[0]`, and one numbered line per remaining item, with the number running 1 to `len(songs)`. After `remove()` of an absent song the starter stops with `ValueError` and prints nothing after that line, which is the planted defect (SP-1.5). A checker can compare the count and the numbered lines. The exact wording of the lines belongs to the lab, not to this pack.

## Misconceptions and traps

| Misconception | Why it is plausible | Correction | SP- ID |
| --- | --- | --- | --- |
| The first item is index 1 and the last is index `len(songs)`. Evidence: a beginner loop `while i <= len(List1)` raised `IndexError` and was fixed with `<`. https://discuss.python.org/t/beginner-level-getting-an-error-indexerror-list-index-out-of-range-in-a-tutorial-program/21026 | People count items from 1 in daily life, and `len()` returns a count that looks like a position. | The first index is 0 and the last is `len(songs) - 1`. An index equal to `len(songs)` raises `IndexError`. | SP-1.1, SP-1.2, SP-1.3 |
| `x = songs.append("Song")` gives back the new list. Evidence: a poster got `None` after `Newlist = List.append(7)`. https://discuss.python.org/t/append-method-not-working/25583 | Many functions return a result, and assignment looks like the natural way to keep it. | `append()` changes `songs` itself and returns `None`. Call it alone on a line, then print `songs`. | SP-1.4 |
| `remove("blue")` finds the value anywhere inside the list, including nested lists. Evidence: a learner got `ValueError` for a value inside a nested list. https://teamtreehouse.com/community/statesremoveblue-it-is-saying-valueerror-listremovex-x-not-in-list | The value is visibly "in" the printed list, so it looks removable. | `remove()` matches only top-level items by equality. A missing match raises `ValueError`. | SP-1.5 |
| Removing items inside a `for` loop over the same list works like removing them one by one. Evidence: https://hackernoon.com/why-deleting-items-from-a-list-while-looping-silently-skips-elements (an article, not a Q&A thread). | The loop and the deletion each look correct alone. | Later items shift left, so the loop skips one. Loop over a copy or build a new list. | SP-1.8 |
| Hypothesis (mine, not sourced from a thread): `remove(1)` removes the item at position 1. | `songs[1]` uses a position in the same brackets-and-number shape, and `remove` sounds like "delete this". | `remove(value)` matches by value, not by position. | SP-1.5 |
| Hypothesis (mine): `remove()` of an absent song does nothing, so a missing song is harmless. | Some tools ignore a delete that matches nothing. | Python raises `ValueError`, and the script stops at that line. | SP-1.5 |
| Hypothesis (mine): a numbered list from `enumerate(songs)` or an index should start at 1. | People read numbered lists from 1. | `enumerate` starts at 0 unless `start=1` is given, and index 0 is the first item. | SP-1.7, SP-1.1 |

Source note: the Q&A sites with the best-known threads, Stack Overflow and python-forum.io, could not be opened, so none is cited.

## Prerequisite map

- Learner must already be able to: run a Python file or use the course's runner (Step 0 of the lab covers setup); write and run a one-line `print("text")`; store a value in a variable with `=`; read an indented block; read a short error message to find the line number.
- The course must teach from zero: what a list is and how square brackets write one; index numbers and counting from 0; `len()`; `append()` and `remove()` and what each changes; the `for` loop over a list; the `ValueError` and `IndexError` messages and how to find the cause; the numbered printout with the number starting at 1.
- Not required: conditionals, functions, or `in`. A guard such as `if song in songs` needs a conditional, so it is out of scope unless the course adds it (course decision, mine).

## Rot watch

| Item | Why it may go stale | Where it will appear |
| --- | --- | --- |
| Python version number (3.15.2 on 2026-11-03) | A new minor release arrives each October, and 3.16 is due 2027-10-06 (SP-0.2). | Lab Step 0, the syllabus, and any slide naming a version |
| Windows install steps | The traditional installer will not be produced for 3.16 or later (SP-0.14). | Lab Step 0 |
| Method signature notation, `append(value, /)` against `append(x)` | The docs changed notation between 3.11 and 3.15 (SP-0.3). | Slides quoting the docs, glossary |
| Exact `ValueError` and `IndexError` message text | It is not in the documentation and may change between versions (SP-U1). | Lab Evidence and troubleshooting table, quiz items that show output |
| Section numbers in the tutorial (3.1.3, 4.2, 5.1) | The docs can be reorganised. | Source citations in slides and notes |
| Forum thread URLs in this table | Threads can be moved, closed, or deleted. | Instructor notes on misconceptions |
| Competitor and standards claims from pass 1 | They change without notice (SP-0.18 prices, SP-0.12 alignment). | Not taught, only in the brief |
