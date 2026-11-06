"""Small shared helpers for course state. Standard library only."""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COURSES = REPO / "courses"

# Gate number to stage name. The stage name is what APPROVALS.md records.
GATES = {0: "viability", 1: "syllabus", 2: "package"}
GATE_BY_STAGE = {v: k for k, v in GATES.items()}

APPROVAL_LINE = re.compile(
    r"^(\d{4}-\d{2}-\d{2}) \| (viability|syllabus|package) \| (APPROVED|REJECTED) \| (.*)$"
)


def status_field(course: Path, key: str) -> str:
    """Value of a '- **Key:** value' line in STATUS.md, or an empty string."""
    p = course / "STATUS.md"
    if not p.is_file():
        return ""
    m = re.search(rf"^- \*\*{re.escape(key)}:\*\*\s*(.*?)\s*$", p.read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else ""


def read_approvals(course: Path) -> dict[str, str]:
    """Last decision per stage: {'viability': 'APPROVED', ...}. A later line replaces an earlier one."""
    p = course / "APPROVALS.md"
    out: dict[str, str] = {}
    if not p.is_file():
        return out
    for line in p.read_text(encoding="utf-8").splitlines():
        m = APPROVAL_LINE.match(line.strip())
        if m:
            out[m.group(2)] = m.group(3)
    return out


def approved(course: Path, stage: str) -> bool:
    return read_approvals(course).get(stage) == "APPROVED"


def awaiting_gate(course: Path) -> int | None:
    """The gate number STATUS.md is waiting on, from 'Awaiting: gate-N', or None."""
    m = re.fullmatch(r"gate-([012])", status_field(course, "Awaiting").strip().lower())
    return int(m.group(1)) if m else None
