---
description: Start a new course, run the viability research, and open Gate 0
argument-hint: <topic>, level: <level>[, modules: N][, capstone: ...]
---

Start a new course from this request: $ARGUMENTS

Follow the "New course" procedure in CLAUDE.md. Parse the topic, level, module count (default 2),
and the capstone idea if one was given. If the topic or the level is missing, ask one short
question and stop. Otherwise create the course, run viability-review (research-analyst pass 1),
render, check through `viability`, and open Gate 0 with course-producer's gate request. Then stop
and wait for the human's reply.
