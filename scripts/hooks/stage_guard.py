#!/usr/bin/env python3
"""PreToolUse hook: keep course stages in order and keep approvals out of agents' hands.

Reads the tool call as JSON on stdin. Exit 0 lets the call through. Exit 2 blocks it and shows the
message on stderr to Claude. Any other failure exits 1, which warns but never blocks.

Rules for files under courses/<slug>/:

    APPROVALS.md                  never writable here; the main session uses scripts/approve.py
    01-syllabus/                  needs the viability gate approved
    02-deck, 03-assessments,
    04-labs/                      need the syllabus gate approved
    qa/                           needs the syllabus approved and every production file present
    qa/ta-grounding-manifest.md,
    maintenance/                  need the package gate approved

This is a guardrail, not security: the main session has Bash and could write around it. It stops
an agent drifting ahead of a gate by accident.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import courselib as cl  # noqa: E402
from check_package import Course, Report  # noqa: E402

EDIT_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
NEEDS_VIABILITY = {"01-syllabus"}
NEEDS_SYLLABUS = {"02-deck", "03-assessments", "04-labs"}
NEEDS_PACKAGE = {"maintenance"}


def native(path: str) -> str:
    """On Windows, turn an MSYS style path (/d/Documents/x) into a native one (D:/Documents/x).
    Git Bash hands out the first form and Python only understands the second."""
    m = re.match(r"^/([a-zA-Z])(/.*)?$", path)
    if os.name == "nt" and m:
        return f"{m.group(1).upper()}:{m.group(2) or '/'}"
    return path


def block(message: str) -> int:
    print(f"stage guard: {message}", file=sys.stderr)
    return 2


def missing_production_files(course: Path) -> list[str]:
    c = Course(course, Report(), "production", False)
    c.check_syllabus()
    if not c.module_count:
        return ["01-syllabus/syllabus.md (no module count)"]
    return [f for f in c.required_files() if not (course / f).is_file()]


def decide(project: Path, tool_name: str, file_path: str, cwd: str | None) -> tuple[int, str]:
    """Return (exit code, message)."""
    if tool_name not in EDIT_TOOLS or not file_path:
        return 0, ""
    p = Path(native(file_path))
    if not p.is_absolute():
        p = Path(native(cwd) if cwd else project) / p
    try:
        rel = p.resolve().relative_to((project / "courses").resolve())
    except ValueError:
        return 0, ""
    parts = rel.parts
    if len(parts) < 2:
        return 0, ""
    slug, area = parts[0], parts[1]
    course = project / "courses" / slug

    if area == "APPROVALS.md":
        return 2, ("APPROVALS.md is written only by the main session through scripts/approve.py, quoting "
                   "the human's own words. Agents never write it.")
    if area == "dist":
        return 0, ""

    if area in NEEDS_VIABILITY and not cl.approved(course, "viability"):
        return 2, f"{area}/ cannot be written until Gate 0 (viability) is approved for {slug}."
    if area in NEEDS_SYLLABUS and not cl.approved(course, "syllabus"):
        return 2, f"{area}/ cannot be written until Gate 1 (syllabus) is approved for {slug}."
    if area in NEEDS_PACKAGE and not cl.approved(course, "package"):
        return 2, f"{area}/ cannot be written until Gate 2 (package) is approved for {slug}."
    if area == "qa":
        if not cl.approved(course, "syllabus"):
            return 2, f"qa/ cannot be written until Gate 1 (syllabus) is approved for {slug}."
        if len(parts) > 2 and parts[2] == "ta-grounding-manifest.md":
            if not cl.approved(course, "package"):
                return 2, f"the TA manifest cannot be written until Gate 2 (package) is approved for {slug}."
        else:
            missing = missing_production_files(course)
            if missing:
                return 2, (f"qa/ cannot be written until the package is complete. Missing: "
                           f"{', '.join(missing[:6])}{' ...' if len(missing) > 6 else ''}")
    return 0, ""


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"stage guard: could not read hook input ({e}); allowing the call", file=sys.stderr)
        return 1
    project = Path(native(os.environ.get("CLAUDE_PROJECT_DIR") or str(cl.REPO)))
    tool_input = data.get("tool_input") or {}
    file_path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    code, message = decide(project, data.get("tool_name", ""), file_path, data.get("cwd"))
    if code == 2:
        return block(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
