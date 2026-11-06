#!/usr/bin/env python3
"""Summarise active courses from their STATUS.md files.

    python scripts/course_status.py [--all] [--hook]

Courses whose folder name starts with an underscore (fixtures) are skipped. Published courses are
skipped unless --all is given. With --hook the output is shaped for a SessionStart hook, which adds
stdout to the session context, and nothing is printed when no course is active.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import courselib as cl  # noqa: E402


def summarise(courses_dir: Path, include_done: bool) -> list[str]:
    lines = []
    if not courses_dir.is_dir():
        return lines
    for c in sorted(p for p in courses_dir.iterdir() if p.is_dir() and not p.name.startswith("_")):
        if not (c / "STATUS.md").is_file():
            continue
        state = cl.status_field(c, "State") or "unknown"
        if state in ("published", "maintenance") and not include_done:
            continue
        gate = cl.awaiting_gate(c)
        wait = f"waiting on you at gate {gate} ({cl.GATES[gate]})" if gate is not None else "nothing waiting on you"
        nxt = ""
        text = (c / "STATUS.md").read_text(encoding="utf-8")
        if "## Next step" in text:
            nxt = text.split("## Next step", 1)[1].strip().splitlines()[0] if text.split("## Next step", 1)[1].strip() else ""
        lines.append(f"- {c.name}: state {state}; {wait}. Next: {nxt or 'see STATUS.md'}")
    return lines


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true", help="include published courses")
    ap.add_argument("--hook", action="store_true", help="SessionStart hook output")
    ap.add_argument("--courses-dir", type=Path, default=cl.COURSES)
    args = ap.parse_args(argv)

    lines = summarise(args.courses_dir, args.all)
    if args.hook:
        if lines:
            print("Course factory: courses in progress. Offer to continue the one that is waiting.")
            print("\n".join(lines))
        return 0
    print("\n".join(lines) if lines else "No active courses.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
