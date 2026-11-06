---
description: Render a course, or one stage of it, to PDF
argument-hint: <slug> [stage]
---

Render: $ARGUMENTS

Run `uv run --with markdown --with pygments python build/render.py <slug>` and add
`--only <stage>` when a stage was given (for example `02-deck` or `03-assessments`). Report the
files written and every `warn` line. Name the owning agent for each warn. Do not edit any course
content yourself.
