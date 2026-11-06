---
description: Show where courses stand
argument-hint: [slug]
allowed-tools: Bash(python scripts/course_status.py:*)
---

Show course status for: $ARGUMENTS

Run `python scripts/course_status.py --all`. If a slug was given, also read that course's
`STATUS.md` and summarise its gates, stages, blockers, and next step in a few lines. Do not start
any work.
