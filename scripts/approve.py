#!/usr/bin/env python3
"""Log a human's gate decision. Run by the main session, never by a subagent.

    python scripts/approve.py <slug> --init
    python scripts/approve.py <slug> approve "<the human's reply, verbatim>"
    python scripts/approve.py <slug> reject  "<the human's reply, verbatim>"

The gate is the one STATUS.md is waiting on (`Awaiting: gate-N`). The script refuses when no gate
is pending, when an earlier gate is not approved, and when an approval reads as hedged or as
feedback. It cannot judge whether a reply is truly positive: that stays with the main session,
which must pass the human's own words from their reply to the pending gate request.

Exit code 0: logged. 1: refused, with the reason on stderr. 2: usage error.
"""

from __future__ import annotations

import argparse
import datetime
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import courselib as cl  # noqa: E402

# Words that turn a "yes" into feedback or a question. A hedged approval is not an approval.
HEDGE = re.compile(
    r"\?|\b(but|however|except|unless|although|not|no|nope|nah|don'?t|dont|wait|hold on|"
    r"change|changes|fix|instead|redo|rework|revise|should|could you|can you|needs?|"
    r"before|first|only if|maybe|perhaps|not sure|unsure)\b",
    re.I,
)
MAX_APPROVAL_CHARS = 300

NEXT_STEP = {
    "viability": "run curriculum-architect (syllabus-draft).",
    "syllabus": "run deck-writer, assessment-designer, and lab-engineer in parallel (in-production).",
    "package": "tag the course, run qa-reviewer in TA-MANIFEST mode, then the course is published.",
}


def refuse(message: str) -> int:
    print(f"refused: {message}", file=sys.stderr)
    return 1


def init(course: Path, template: Path) -> int:
    target = course / "APPROVALS.md"
    if target.exists():
        return refuse("APPROVALS.md already exists")
    text = template.read_text(encoding="utf-8").replace("{slug}", course.name)
    target.write_text(text, encoding="utf-8", newline="\n")
    print(f"created {target}")
    return 0


def log(course: Path, decision: str, reply: str, today: str) -> int:
    gate = cl.awaiting_gate(course)
    if gate is None:
        return refuse("STATUS.md has no gate pending ('Awaiting: gate-0', 'gate-1', or 'gate-2'). "
                      "Open the gate request first.")
    stage = cl.GATES[gate]
    reply = " ".join(reply.split())
    if not reply:
        return refuse("the human's reply is empty")

    if decision == "APPROVED":
        for earlier in range(gate):
            if not cl.approved(course, cl.GATES[earlier]):
                return refuse(f"gate {gate} ({stage}) cannot be approved before gate {earlier} "
                              f"({cl.GATES[earlier]}) is approved")
        if len(reply) > MAX_APPROVAL_CHARS:
            return refuse("the reply is long, so it is probably feedback. Treat it as a rejection with "
                          "notes, or ask the human for a plain yes")
        hedge = HEDGE.search(reply)
        if hedge:
            return refuse(f"the reply contains '{hedge.group(0)}', so it reads as hedged or as feedback. "
                          "Do not log an approval. Ask the human once for a plain yes, or treat it as a "
                          "rejection with notes")

    if '"' in reply:
        reply = reply.replace('"', "'")
    line = f'{today} | {stage} | {decision} | "{reply}"'
    path = course / "APPROVALS.md"
    if not path.is_file():
        return refuse("APPROVALS.md does not exist; run with --init first")
    text = path.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text + line + "\n", encoding="utf-8", newline="\n")
    print(f"logged: {line}")
    if decision == "APPROVED":
        print(f"next: set STATUS Awaiting to nothing, then {NEXT_STEP[stage]}")
    else:
        print("next: send the human's notes verbatim to the owning agent, move the state back to the "
              "draft stage, and revise.")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("action", nargs="?", choices=["approve", "reject"])
    ap.add_argument("reply", nargs="?", default="")
    ap.add_argument("--init", action="store_true", help="create APPROVALS.md from the template")
    ap.add_argument("--courses-dir", type=Path, default=cl.COURSES)
    ap.add_argument("--date", default=None, help="override today's date, for tests")
    args = ap.parse_args(argv)

    course = args.courses_dir / args.slug
    if not course.is_dir():
        print(f"error: no course at {course}", file=sys.stderr)
        return 2
    if args.init:
        return init(course, cl.REPO / "templates" / "approvals.md")
    if not args.action:
        print("error: give approve or reject, or --init", file=sys.stderr)
        return 2
    today = args.date or datetime.date.today().isoformat()
    return log(course, "APPROVED" if args.action == "approve" else "REJECTED", args.reply, today)


if __name__ == "__main__":
    raise SystemExit(main())
