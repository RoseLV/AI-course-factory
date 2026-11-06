---
description: Rerun the checker and the QA review for a course
argument-hint: <slug>
---

Run QA for: $ARGUMENTS

1. Render the whole course so no PDF is stale.
2. Run `python scripts/check_package.py <slug> --through production`. If there are blocking
   findings, run the fix loop from CLAUDE.md and do not start the reviewer yet.
3. Run qa-reviewer in REVIEW mode with the checker output. Render `qa`. Run the checker through
   `package`.
4. Report the verdict, the blocking and minor counts, and the numbers table. Do not open Gate 2
   unless the course state is `qa-review` and the verdict is PASS or PASS WITH FIXES.
