---
description: Do the next step for a course, or re-show the gate it is waiting on
argument-hint: [slug]
---

Continue the course: $ARGUMENTS

If no slug was given, run `python scripts/course_status.py` and pick the only active course, or ask
which one if there are several. Read that course's `STATUS.md`.

- If it is waiting on a gate, do not advance. Have course-producer run GATE-REQUEST and show the
  text again, then wait for the human's reply.
- Otherwise run the next step from the pipeline table in CLAUDE.md for its current state, following
  the stage routine: status, agent, render, check, fix loop, status, commit.
- If the state and the files on disk disagree, trust the files, tell the human, and have
  course-producer correct STATUS.
