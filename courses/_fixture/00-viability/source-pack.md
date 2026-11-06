---
course: _fixture
stage: 00-viability
module: n/a
author: research-analyst
date: 2026-11-03
outcomes: n/a
---

# Source pack: Intro to SQL

FIXTURE: sample content for tooling tests.

## Open findings

Unsourced claims: 0.

## Canonical sources

| Source | URL | Version covered | Opened |
| --- | --- | --- | --- |
| SQLite SELECT documentation | https://www.sqlite.org/lang_select.html | 3.x | 2026-11-03 |

## Claims

### SP-1.1

- **Claim:** A `SELECT` statement with a `WHERE` clause returns only rows for which the condition is true.
- **Mechanism:** The database evaluates the condition on each row and keeps the row only when the result is true.
- **Source:** https://www.sqlite.org/lang_select.html, the WHERE clause section
- **Version:** 3.x
- **Opened:** 2026-11-03
- **Serves:** module 1

### SP-1.2

- **Claim:** `ORDER BY column DESC` sorts rows from the highest value to the lowest.
- **Mechanism:** The database sorts the result set by the named column after filtering, in descending order when `DESC` is given.
- **Source:** https://www.sqlite.org/lang_select.html, the ORDER BY clause section
- **Version:** 3.x
- **Opened:** 2026-11-03
- **Serves:** module 1

## Misconceptions and traps

| Misconception | Why it is plausible | Correction | SP- ID |
| --- | --- | --- | --- |
| `>` includes the boundary value | "Over 60" sounds like "60 and up" in speech | `>` excludes the boundary, `>=` includes it | SP-1.1 |

## Prerequisite map

- Learner must already be able to: read a table of rows and columns.
- The course must teach from zero: what a query is, `SELECT`, `WHERE`, `ORDER BY`.

## Rot watch

| Item | Why it may go stale | Where it will appear |
| --- | --- | --- |
| Online SQL tool | Hosted tools change or close | Lab step 0 |
