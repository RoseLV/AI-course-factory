#!/usr/bin/env python3
"""Append one line to a course's TA log. Run by the main session after each /ask-ta answer.

    python scripts/ta_log.py <slug> "<date | theme | where in the course | outcome>"

One writer, append-only. The ta-agent used to edit the log itself, and four agents running at once
overwrote each other's lines: each saw no file, created it, and the last write won. Appending a
single line with mode "a" does not lose lines, so the agent now reports the line and this script
writes it.

The entry has four fields: an ISO date, a short theme in the agent's own words, where in the course
the question sits, and an outcome of `answered` or `escalated: <category>`. It never carries a
student name or the student's exact words, and the script refuses an entry that looks like it does.

Exit code 0: appended. 1: refused. 2: usage error.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import courselib as cl  # noqa: E402

HEADER = "# TA log\n\ndate | theme | where in the course | outcome\n"
CATEGORIES = ("grades", "integrity", "wellbeing", "unanswerable")
OUTCOME = re.compile(r"^(answered|escalated: (" + "|".join(CATEGORIES) + r"))$")
MAX_THEME = 100


def refuse(message: str) -> int:
    print(f"refused: {message}", file=sys.stderr)
    return 1


def check_entry(entry: str) -> str | None:
    """Return a reason the entry is not acceptable, or None."""
    if "\n" in entry.strip():
        return "the entry must be one line"
    parts = [p.strip() for p in entry.split("|")]
    if len(parts) != 4:
        return "the entry needs four fields separated by |: date | theme | where | outcome"
    date, theme, where, outcome = parts
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        return "the date must look like 2026-11-03"
    if not theme or not where:
        return "theme and where must not be empty"
    if len(theme) > MAX_THEME:
        return f"the theme is over {MAX_THEME} characters; summarise it, do not quote the student"
    if '"' in theme or '"' in where:
        return "quotation marks suggest the student's own words; paraphrase instead"
    if not OUTCOME.match(outcome):
        return "the outcome must be 'answered' or 'escalated: grades|integrity|wellbeing|unanswerable'"
    return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("entry")
    ap.add_argument("--courses-dir", type=Path, default=cl.COURSES)
    args = ap.parse_args(argv)

    course = args.courses_dir / args.slug
    if not course.is_dir():
        print(f"error: no course at {course}", file=sys.stderr)
        return 2
    if not cl.approved(course, "package"):
        return refuse("the course is not published: Gate 2 is not approved")
    problem = check_entry(args.entry)
    if problem:
        return refuse(problem)

    log = course / "maintenance" / "ta-log.md"
    log.parent.mkdir(parents=True, exist_ok=True)
    line = " | ".join(p.strip() for p in args.entry.split("|")) + "\n"
    # Mode "a" appends in one write, so concurrent callers cannot overwrite each other.
    if not log.exists():
        try:
            with open(log, "x", encoding="utf-8", newline="\n") as f:
                f.write(HEADER)
        except FileExistsError:
            pass
    with open(log, "a", encoding="utf-8", newline="\n") as f:
        f.write(line)
    print(f"logged: {line.strip()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
