#!/usr/bin/env python3
"""Mechanical QA checks for a course package. Standard library only.

    python scripts/check_package.py <slug> [--through STAGE] [--no-pdf] [--json]

STAGE is how far the course has got, so the checker can run at every gate:

    viability   brief and source pack
    syllabus    ... plus the syllabus
    production  ... plus decks, quizzes, keys, TA packs, labs (run this before QA)
    package     ... plus qa-report and alignment matrix (default, run at Gate 2)
    published   ... plus the TA grounding manifest

Exit code 0: no blocking findings. 1: at least one blocking finding. 2: usage error.
Every finding carries a stable code, so tests and agents can refer to it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STAGES = ["viability", "syllabus", "production", "package", "published"]
WORDS_PER_MINUTE = 130

FRONT_KEYS = ["course", "stage", "module", "author", "date", "outcomes"]
# Scripts append to these. They are data, not documents: no front matter, no PDF.
DATA_FILES = {"maintenance/ta-log.md"}
DEPTHS = {"mention", "explain", "practise"}
SP_RE = re.compile(r"\bSP-(?:U\d+|\d+\.\d+)\b")
LO_RE = re.compile(r"\bLO-\d+\b")
FENCE_RE = re.compile(r"```(\w*)\n(.*?)```", re.S)
ITEM_RE = re.compile(
    r"<!--\s*item:\s*(\S+)\s*\|\s*outcome:\s*(LO-\d+)\s*\|\s*difficulty:\s*(\w+)\s*-->"
)


# Who fixes a finding, by the folder it is in. PDF findings are fixed by rendering, which only the
# main session does.
OWNER_BY_FOLDER = {
    "00-viability": "research-analyst",
    "01-syllabus": "curriculum-architect",
    "02-deck": "deck-writer",
    "03-assessments": "assessment-designer",
    "04-labs": "lab-engineer",
    "qa": "qa-reviewer",
    "maintenance": "ta-agent",
    "STATUS.md": "course-producer",
    "APPROVALS.md": "main session",
}


def owner_for(code: str, path: str) -> str:
    if code.startswith("PDF-"):
        return "main session (render)"
    first = path.replace("\\", "/").split(":")[0].split(" ")[0].split("/")[0]
    return OWNER_BY_FOLDER.get(first, "main session")


@dataclass
class Finding:
    code: str
    severity: str  # blocking or minor
    path: str
    message: str
    owner: str = ""


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)

    def add(self, code: str, severity: str, path: str, message: str) -> None:
        self.findings.append(Finding(code, severity, path, message, owner_for(code, path)))

    @property
    def blocking(self) -> int:
        return sum(1 for f in self.findings if f.severity == "blocking")

    @property
    def minor(self) -> int:
        return sum(1 for f in self.findings if f.severity == "minor")


# --------------------------------------------------------------------------
# parsing helpers
# --------------------------------------------------------------------------

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    meta = {}
    for line in text[3:end].strip("\n").splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, text[end + 4:]


def strip_code(text: str) -> str:
    return FENCE_RE.sub("", text)


def prose_lines(text: str):
    """Yield (line number, line) for every line outside a fenced code block, with real line numbers.
    Counting after the fences are removed would shift every number below the first block."""
    in_fence = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield i, line


def table_rows(text: str, first_cell: re.Pattern) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and first_cell.match(cells[0]):
            rows.append(cells)
    return rows


def section(text: str, heading: str) -> str:
    """Body of the '## heading' section, up to the next '## '."""
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.M | re.I)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^##\s+", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


@dataclass
class Slide:
    number: int
    title: str
    bullets: list[str] = field(default_factory=list)
    code: list[str] = field(default_factory=list)
    svg: str = ""
    visual: str = ""
    visual_src: str = ""
    notes: str = ""
    covers: str = ""


KEY_RE = re.compile(r"^(Visual-src|Visual|Notes|Covers)\s*:\s*(.*)$", re.I)


def parse_deck(text: str) -> list[Slide]:
    _, body = front_matter(text)
    marks = list(re.finditer(r"^##\s+Slide\s+(\d+)\s*:\s*(.+?)\s*$", body, re.M))
    slides = []
    for i, mark in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        block = body[mark.end():end]
        s = Slide(int(mark.group(1)), mark.group(2))

        def take(m: re.Match) -> str:
            lang = (m.group(1) or "text").lower()
            if lang == "svg":
                s.svg = m.group(2).strip()
            else:
                s.code.append(m.group(2))
            return ""

        block = FENCE_RE.sub(take, block)
        current = None
        for line in block.splitlines():
            key = KEY_RE.match(line.strip())
            if key:
                current = key.group(1).lower().replace("-", "_")
                setattr(s, current, key.group(2).strip())
                continue
            t = line.strip()
            if not t:
                continue
            if t.startswith(("- ", "* ")) and current is None:
                s.bullets.append(t[2:].strip())
            elif current:
                setattr(s, current, (getattr(s, current) + " " + t).strip())
        slides.append(s)
    return slides


# --------------------------------------------------------------------------
# the course
# --------------------------------------------------------------------------

@dataclass
class Module:
    number: int
    title: str
    narration_min: int | None = None
    hands_on_min: int | None = None
    checkpoints_min: int | None = None
    discussion_min: int | None = None
    total_min: int | None = None
    word_budget: int | None = None
    depths: list[str] = field(default_factory=list)


class Course:
    def __init__(self, root: Path, report: Report, through: str, check_pdf: bool):
        self.root = root
        self.slug = root.name
        self.r = report
        self.through = STAGES.index(through)
        self.check_pdf = check_pdf
        self.outcomes: list[str] = []
        self.modules: list[Module] = []
        self.module_count = 0
        self.sp_ids: set[str] = set()

    def rel(self, p: Path) -> str:
        return p.relative_to(self.root).as_posix()

    def at_least(self, stage: str) -> bool:
        return self.through >= STAGES.index(stage)

    # ---- manifest -------------------------------------------------------

    def required_files(self) -> list[str]:
        files = ["STATUS.md", "APPROVALS.md"]
        n = self.module_count
        files += ["00-viability/viability-brief.md", "00-viability/source-pack.md"]
        if self.at_least("syllabus"):
            files.append("01-syllabus/syllabus.md")
        if self.at_least("production"):
            for i in range(1, n + 1):
                m = f"m{i:02d}"
                files += [
                    f"02-deck/deck-{m}.md",
                    f"03-assessments/student/quiz-{m}.md",
                    f"03-assessments/instructor/quiz-{m}-key.md",
                    f"03-assessments/instructor/ta-feedback-pack-{m}.md",
                    f"04-labs/lab-{m}.md",
                ]
        if self.at_least("package"):
            files += ["qa/qa-report.md", "qa/alignment-matrix.md"]
        if self.at_least("published"):
            files.append("qa/ta-grounding-manifest.md")
        return files

    def check_manifest(self) -> None:
        for f in self.required_files():
            if not (self.root / f).is_file():
                self.r.add("MANIFEST-MISSING", "blocking", f, "required file is missing")

    # ---- generic file checks --------------------------------------------

    def md_files(self) -> list[Path]:
        return sorted(p for p in self.root.rglob("*.md") if "dist" not in p.relative_to(self.root).parts)

    def check_generic(self) -> None:
        for p in self.md_files():
            rel = self.rel(p)
            text = read(p)
            lines = text.splitlines()

            if rel != "APPROVALS.md":
                for i, line in enumerate(lines, 1):
                    if "—" in line or "&mdash;" in line:
                        self.r.add("EM-DASH", "blocking", f"{rel}:{i}", "em dash found; use a comma, colon, or new sentence")

            if rel not in ("STATUS.md", "APPROVALS.md") and rel not in DATA_FILES:
                meta, _ = front_matter(text)
                missing = [k for k in FRONT_KEYS if k not in meta]
                if missing:
                    self.r.add("FRONT-MATTER", "blocking", rel, f"front matter missing: {', '.join(missing)}")
                else:
                    if meta["course"] != self.slug:
                        self.r.add("FRONT-MATTER", "blocking", rel, f"course is '{meta['course']}', expected '{self.slug}'")
                    expected = p.parent.relative_to(self.root).as_posix()
                    if meta["stage"] != expected:
                        self.r.add("FRONT-MATTER", "minor", rel, f"stage is '{meta['stage']}', expected '{expected}'")

            if rel == "STATUS.md" and len(lines) > 60:
                self.r.add("STATUS-LENGTH", "minor", rel, f"{len(lines)} lines; the limit is 60")

            if rel != "APPROVALS.md":
                for i, raw in prose_lines(text):
                    line = re.sub(r"`[^`\n]*`", "", raw)
                    if re.search(r"\{[A-Za-z][^{}\n]{0,60}\}", line):
                        self.r.add("TEMPLATE-BRACE", "blocking", f"{rel}:{i}", "unfilled template placeholder in braces")
                    if re.search(r"\b(TBD|TODO|FIXME|lorem ipsum)\b", line, re.I):
                        self.r.add("PLACEHOLDER-TEXT", "blocking", f"{rel}:{i}", "placeholder text left in the file")

            for i, line in prose_lines(text):
                m = re.match(r"^#{1,6}\s+(.*)$", line)
                if not m:
                    continue
                title = re.sub(r"^(Slide\s+\d+\s*:|Question\s+\d+|Step\s+\d+\s*-)\s*", "", m.group(1))
                words = title.split()[1:]
                caps = [w for w in words if w[0].isupper() and not w.isupper() and w.isalpha()]
                if len(caps) >= 3:
                    self.r.add("HEADING-CASE", "minor", f"{rel}:{i}", "heading looks like Title Case; use sentence case")

    def check_pdfs(self) -> None:
        dist = self.root / "dist"
        for p in self.md_files():
            rel = p.relative_to(self.root)
            if rel.parts[0] == "dist" or rel.as_posix() in DATA_FILES:
                continue
            if rel.parts[0] == "02-deck":
                if not re.match(r"deck-m\d+\.md$", p.name):
                    continue
                outs = [dist / "02-deck" / f"{p.stem}.pdf", dist / "02-deck" / f"{p.stem}-instructor.pdf"]
            else:
                outs = [dist / rel.with_suffix(".pdf")]
            for out in outs:
                if not out.is_file():
                    self.r.add("PDF-MISSING", "blocking", rel.as_posix(), f"no PDF at dist/{out.relative_to(dist).as_posix()}")
                elif out.stat().st_mtime + 2 < p.stat().st_mtime:
                    self.r.add("PDF-STALE", "blocking", rel.as_posix(), f"dist/{out.relative_to(dist).as_posix()} is older than its markdown")

    # ---- viability ------------------------------------------------------

    def check_source_pack(self) -> None:
        p = self.root / "00-viability/source-pack.md"
        if not p.is_file():
            return
        rel = self.rel(p)
        text = read(p)
        seen: set[str] = set()
        blocks = list(re.finditer(r"^###\s+(SP-\S+)\s*$", text, re.M))
        for i, m in enumerate(blocks):
            sid = m.group(1)
            if sid in seen:
                self.r.add("SP-DUPLICATE", "blocking", rel, f"{sid} is allocated twice")
            seen.add(sid)
            end = blocks[i + 1].start() if i + 1 < len(blocks) else len(text)
            body = text[m.end():end]
            fields = ["Claim", "Mechanism", "Opened"] + ([] if sid.startswith("SP-U") else ["Source"])
            for f in fields:
                if not re.search(rf"\*\*{f}:\*\*\s*\S", body):
                    self.r.add("SP-FIELD", "blocking", rel, f"{sid} has no {f}")
            if "Source" in fields:
                src = re.search(r"\*\*Source:\*\*\s*(.*)", body)
                if src and "http" not in src.group(1):
                    self.r.add("SP-SOURCE", "blocking", rel, f"{sid} source has no URL")
        self.sp_ids = seen
        self.r.metrics["claims"] = len(seen)

    def check_brief(self) -> None:
        p = self.root / "00-viability/viability-brief.md"
        if not p.is_file():
            return
        text = read(p)
        rel = self.rel(p)
        if not re.search(r"\b(NO-GO|GO|DEFER)\b", section(text, "Recommendation")):
            self.r.add("BRIEF-VERDICT", "blocking", rel, "Recommendation section has no GO, NO-GO, or DEFER")
        words = len(text.split())
        if words > 1100:
            self.r.add("BRIEF-LENGTH", "minor", rel, f"{words} words; the brief is limited to two pages")

    # ---- syllabus -------------------------------------------------------

    def check_syllabus(self) -> None:
        p = self.root / "01-syllabus/syllabus.md"
        if not p.is_file():
            return
        rel = self.rel(p)
        text = read(p)

        m = re.search(r"\*\*Modules:\*\*\s*(\d+)", text)
        self.module_count = int(m.group(1)) if m else 0
        if not self.module_count:
            self.r.add("SYLLABUS-MODULES", "blocking", rel, "metadata has no '**Modules:** N' line")
        elif not 1 <= self.module_count <= 4:
            self.r.add("SYLLABUS-MODULES", "blocking", rel, f"{self.module_count} modules; the limit is 1 to 4")

        rows = table_rows(section(text, "Learning outcomes"), re.compile(r"LO-\d+"))
        self.outcomes = [r[0] for r in rows]
        if not 3 <= len(rows) <= 9:
            self.r.add("OUTCOMES-COUNT", "blocking", rel, f"{len(rows)} outcomes; expected 3 to 9")
        applied = [r for r in rows if len(r) >= 3 and r[2].lower().startswith("y")]
        if rows and len(applied) * 2 <= len(rows):
            self.r.add("OUTCOMES-APPLIED", "blocking", rel, f"{len(applied)} of {len(rows)} outcomes are applied; the majority must be")
        if rows and (len(rows[0]) < 3 or not rows[0][2].lower().startswith("y")):
            self.r.add("OUTCOMES-APPLIED", "blocking", rel, "LO-1 must be applied and name the capstone artifact")
        for r in rows:
            if re.match(r"(understand|know)\b", r[1], re.I):
                self.r.add("OUTCOME-VERB", "blocking", rel, f"{r[0]} starts with a vague verb: use a measurable one")

        cap = section(text, "Capstone")
        if not re.search(r"\*\*End state:\*\*\s*\S", cap):
            self.r.add("CAPSTONE", "blocking", rel, "capstone has no end state")

        heads = list(re.finditer(r"^###\s+M(\d+):\s*(.+?)\s*$", text, re.M))
        if self.module_count and len(heads) != self.module_count:
            self.r.add("SYLLABUS-MODULES", "blocking", rel, f"{len(heads)} module sections but metadata says {self.module_count}")
        for i, h in enumerate(heads):
            stops = [len(text)]
            if i + 1 < len(heads):
                stops.append(heads[i + 1].start())
            nxt = text.find("\n## ", h.end())
            if nxt != -1:
                stops.append(nxt)
            block = text[h.end():min(stops)]
            mod = Module(int(h.group(1)), h.group(2))
            if re.search(r"\b(install|set ?up)\b", mod.title, re.I):
                self.r.add("SETUP-MODULE", "minor", rel, f"module {mod.number} title suggests setup; setup is Step 0 of the first lab")
            t = re.search(
                r"narration\s+(\d+)\s*min.*?hands-on\s+(\d+)\s*min.*?checkpoints\s+(\d+)\s*min.*?discussion\s+(\d+)\s*min.*?Total\s+(\d+)\s*min",
                block, re.S | re.I)
            if t:
                mod.narration_min, mod.hands_on_min, mod.checkpoints_min, mod.discussion_min, mod.total_min = map(int, t.groups())
                if sum([mod.narration_min, mod.hands_on_min, mod.checkpoints_min, mod.discussion_min]) != mod.total_min:
                    self.r.add("TIME-BUDGET", "blocking", rel, f"module {mod.number} buckets do not sum to its total")
            else:
                self.r.add("TIME-BUDGET", "blocking", rel, f"module {mod.number} has no time budget in the required form")
            w = re.search(r"Narration word budget:\s*(\d+)", block)
            if w:
                mod.word_budget = int(w.group(1))
                if mod.narration_min is not None and mod.word_budget != mod.narration_min * WORDS_PER_MINUTE:
                    self.r.add("TIME-BUDGET", "minor", rel, f"module {mod.number} word budget is not narration minutes x {WORDS_PER_MINUTE}")
            else:
                self.r.add("TIME-BUDGET", "blocking", rel, f"module {mod.number} states no narration word budget")
            # Only the table headed "Topic | Depth" carries depth marks. Other tables in the module
            # section, such as a quiz contract, are not topics.
            in_topics = False
            for line in block.splitlines():
                line = line.strip()
                if not line.startswith("|"):
                    in_topics = False
                    continue
                cells = [c.strip() for c in line.strip("|").split("|")]
                if len(cells) >= 2 and cells[0].lower() == "topic" and cells[1].lower() == "depth":
                    in_topics = True
                    continue
                if not in_topics or set("".join(cells)) <= set("-: "):
                    continue
                depth = cells[1].lower() if len(cells) > 1 else ""
                if depth in DEPTHS:
                    mod.depths.append(depth)
                else:
                    self.r.add("DEPTH-MARK", "blocking", rel, f"module {mod.number} topic '{cells[0]}' has invalid depth '{cells[1] if len(cells) > 1 else ''}'")
            if "practise" not in mod.depths:
                self.r.add("DEPTH-MARK", "blocking", rel, f"module {mod.number} has no topic marked practise")
            self.modules.append(mod)

        align = table_rows(section(text, "Alignment table"), re.compile(r"LO-\d+"))
        aligned = {r[0] for r in align}
        for lo in self.outcomes:
            if lo not in aligned:
                self.r.add("SYLLABUS-ALIGNMENT", "blocking", rel, f"{lo} has no row in the alignment table")
        for r in align:
            if any(not c for c in r):
                self.r.add("SYLLABUS-ALIGNMENT", "blocking", rel, f"{r[0]} has an empty alignment cell")

    # ---- decks ----------------------------------------------------------

    def check_decks(self) -> None:
        for p in sorted((self.root / "02-deck").glob("deck-m*.md")):
            rel = self.rel(p)
            mnum = int(re.search(r"m(\d+)", p.stem).group(1))
            text = read(p)
            slides = parse_deck(text)
            if not slides:
                self.r.add("DECK-SLIDES", "blocking", rel, "no '## Slide N:' headings found")
                continue
            note_words = 0
            run = longest = 0
            cites = 0
            for s in slides:
                loc = f"{rel} slide {s.number}"
                if len(s.bullets) > 4:
                    self.r.add("SLIDE-BULLETS", "blocking", loc, f"{len(s.bullets)} bullets; the limit is 4")
                for b in s.bullets:
                    if len(b.split()) > 8:
                        self.r.add("SLIDE-BULLET-WORDS", "blocking", loc, f"bullet over 8 words: '{b[:40]}'")
                if not s.covers or not LO_RE.search(s.covers):
                    self.r.add("SLIDE-COVERS", "blocking", loc, "no Covers line naming an outcome")
                for lo in LO_RE.findall(s.covers):
                    if self.outcomes and lo not in self.outcomes:
                        self.r.add("OUTCOME-UNKNOWN", "blocking", loc, f"{lo} is not in the syllabus")
                words = len(s.notes.split())
                note_words += words
                if words < 80 or words > 150:
                    self.r.add("NOTES-LENGTH", "blocking", loc, f"notes are {words} words; the range is 80 to 150")
                for c in s.code:
                    if len([ln for ln in c.strip("\n").splitlines()]) > 12:
                        self.r.add("CODE-LENGTH", "blocking", loc, "code block over 12 lines")
                if s.visual and not (s.svg or s.visual_src):
                    self.r.add("VISUAL-PLACEHOLDER", "blocking", loc, "Visual line has no drawn svg or Visual-src")
                if s.visual_src and not (p.parent / s.visual_src).is_file():
                    self.r.add("VISUAL-MISSING", "blocking", loc, f"Visual-src not found: {s.visual_src}")
                if s.svg:
                    self.check_svg(s, loc)

                sps = SP_RE.findall(s.notes + " " + s.title + " " + " ".join(s.bullets))
                cites += len(sps)
                evidence = bool(s.code or sps or s.visual_src or re.match(r"(mechanism|worked example|diagnostic sequence|real output|failure)", s.title, re.I))
                run = 0 if evidence else run + 1
                longest = max(longest, run)

            titles = [s.title.lower() for s in slides]
            for label in ("mechanism", "worked example", "diagnostic sequence"):
                if not any(t.startswith(label) for t in titles):
                    self.r.add("DECK-REQUIRED", "blocking", rel, f"no slide titled '{label}...'")
            if "glossary" not in titles[-1]:
                self.r.add("DECK-REQUIRED", "blocking", rel, "the last slide must be the glossary")
            for s in slides:
                if s.title.lower().startswith("worked example"):
                    # The title does not count: the requirement belongs in the slide body.
                    # Text drawn inside the diagram counts: a slide may show the spec as the diagram.
                    svg_text = " ".join(re.findall(r"<text[^>]*>(.*?)</text>", s.svg, re.S))
                    blob = " ".join(s.bullets + s.code + [s.visual, svg_text]).lower()
                    if not re.search(r"requirement|specification|\bspec\b|request|test suite|expected[- ]output", blob):
                        self.r.add("WORKED-EXAMPLE-SOURCE", "blocking", f"{rel} slide {s.number}", "worked example does not state its requirement on the slide")
            if longest >= 3:
                self.r.add("DECK-DENSITY", "blocking", rel, f"{longest} abstract slides in a row; the limit is 2")
            if cites == 0:
                self.r.add("DECK-NO-CITATIONS", "minor", rel, "the deck cites no SP- claim IDs")

            mod = next((m for m in self.modules if m.number == mnum), None)
            gap = None
            if mod and mod.word_budget:
                gap = (note_words - mod.word_budget) / mod.word_budget
                if abs(gap) > 0.20:
                    self.r.add("NARRATION-GAP", "blocking", rel, f"{note_words} note words against a budget of {mod.word_budget} ({gap:+.0%}); the limit is 20 percent")
            self.r.metrics.setdefault("decks", {})[f"m{mnum:02d}"] = {
                "slides": len(slides),
                "note_words": note_words,
                "word_budget": mod.word_budget if mod else None,
                "narration_gap_minutes": round((note_words - mod.word_budget) / WORDS_PER_MINUTE, 1) if mod and mod.word_budget else None,
                "longest_abstract_run": longest,
            }

    def check_svg(self, s: Slide, loc: str) -> None:
        svg = s.svg
        if "viewBox" not in svg:
            self.r.add("SVG-VIEWBOX", "blocking", loc, "svg has no viewBox")
        else:
            wide = 'viewBox="0 0 1200 420"' in svg
            if s.bullets and wide:
                self.r.add("SVG-VIEWBOX-SIZE", "minor", loc, "slide with bullets uses the full-width viewBox; use 0 0 800 500")
            if not s.bullets and 'viewBox="0 0 800 500"' in svg:
                self.r.add("SVG-VIEWBOX-SIZE", "minor", loc, "slide without bullets should use viewBox 0 0 1200 420")
        root = re.match(r"\s*<svg\b[^>]*>", svg)
        if root and re.search(r"\s(width|height)=", root.group(0)):
            self.r.add("SVG-SIZE-ATTR", "minor", loc, "svg root sets width or height; use viewBox only")
        if re.search(r"<script|<foreignObject", svg, re.I):
            self.r.add("SVG-FORBIDDEN", "blocking", loc, "svg contains script or foreignObject")
        if re.search(r"""(href|src)=["']https?:""", svg, re.I):
            self.r.add("SVG-FORBIDDEN", "blocking", loc, "svg loads an external resource")
        if re.search(r"""(fill|stroke)=["'](#|rgb)""", svg, re.I) or "style=" in svg:
            self.r.add("SVG-COLOUR", "minor", loc, "svg writes a literal colour; use the class vocabulary")

    # ---- assessments ----------------------------------------------------

    def check_quizzes(self) -> None:
        for p in sorted((self.root / "03-assessments/student").glob("quiz-m*.md")):
            rel = self.rel(p)
            mnum = re.search(r"m(\d+)", p.stem).group(1)
            text = read(p)
            heads = re.findall(r"^##\s+Question\s+\d+", text, re.M)
            items = ITEM_RE.findall(text)
            if len(heads) != len(items):
                self.r.add("QUIZ-TAGS", "blocking", rel, f"{len(heads)} questions but {len(items)} item tags")
            if not 8 <= len(items) <= 12:
                self.r.add("QUIZ-COUNT", "blocking", rel, f"{len(items)} items; expected 8 to 12")
            ids = [i[0] for i in items]
            if len(set(ids)) != len(ids):
                self.r.add("QUIZ-TAGS", "blocking", rel, "duplicate item IDs")
            diffs = [i[2] for i in items]
            for i in items:
                if i[2] not in ("basic", "standard", "stretch"):
                    self.r.add("QUIZ-TAGS", "blocking", rel, f"{i[0]} has invalid difficulty '{i[2]}'")
                if self.outcomes and i[1] not in self.outcomes:
                    self.r.add("OUTCOME-UNKNOWN", "blocking", rel, f"{i[0]} tests {i[1]}, which is not in the syllabus")
            if items:
                basic = diffs.count("basic") / len(diffs)
                if not 0.25 <= basic <= 0.65:
                    self.r.add("QUIZ-DIFFICULTY-MIX", "minor", rel, f"{basic:.0%} of items are basic; aim for about half")
            if "stretch" not in diffs:
                self.r.add("QUIZ-TRANSFER", "blocking", rel, "no stretch item, so no transfer item")
            if not re.search(r"\*\*Transfer", text):
                self.r.add("QUIZ-TRANSFER", "blocking", rel, "no item labelled Transfer")
            if not re.search(r"\*\*Requirement:\*\*", text):
                self.r.add("QUIZ-EVIDENCE", "blocking", rel, "no real-output item with a stated requirement")
            if not (re.search(r"\*\*Predict", text) and re.search(r"\*\*Reflect", text)):
                self.r.add("QUIZ-PREDICT", "blocking", rel, "no predict and reflect prompts")

            self.check_key(rel, mnum, text, items)

    def check_key(self, qrel: str, mnum: str, qtext: str, items: list) -> None:
        kp = self.root / f"03-assessments/instructor/quiz-m{mnum}-key.md"
        if not kp.is_file():
            return
        krel = self.rel(kp)
        ktext = read(kp)
        entries = {m.group(1): m for m in re.finditer(r"^##\s+(\S+)\s+-\s+Answer:\s*(.*)$", ktext, re.M)}
        item_ids = [i[0] for i in items]
        for iid in item_ids:
            if iid not in entries:
                self.r.add("KEY-MISSING", "blocking", krel, f"no key entry for {iid}")
        for kid in entries:
            if kid not in item_ids:
                self.r.add("KEY-ORPHAN", "blocking", krel, f"key entry {kid} matches no quiz item")
        keys = list(entries.values())
        # Split the quiz into per-item chunks to find multiple choice options.
        chunks = re.split(r"^##\s+Question\s+\d+", qtext, flags=re.M)[1:]
        for idx, chunk in enumerate(chunks):
            if idx >= len(item_ids) or item_ids[idx] not in entries:
                continue
            letters = re.findall(r"^([A-D])\.\s", chunk, re.M)
            if not letters:
                continue
            m = entries[item_ids[idx]]
            ans = re.match(r"([A-D])\b", m.group(2).strip())
            if not ans or ans.group(1) not in letters:
                self.r.add("KEY-ANSWER", "blocking", krel, f"{item_ids[idx]} answer is not one of {', '.join(letters)}")
                continue
            end = ktext.find("\n## ", m.end())
            body = ktext[m.end(): end if end != -1 else len(ktext)]
            for L in letters:
                if L != ans.group(1) and not re.search(rf"^- {L}:\s*\S", body, re.M):
                    self.r.add("KEY-DISTRACTOR", "minor", krel, f"{item_ids[idx]} has no misconception line for distractor {L}")

    def check_ta_packs(self) -> None:
        for p in sorted((self.root / "03-assessments/instructor").glob("ta-feedback-pack-m*.md")):
            text = read(p)
            for i, line in prose_lines(text):
                if re.search(r"\bAnswer\s*:|correct answer|\bis correct\b|^##\s+Q\d+\s+-\s+Answer", line, re.I):
                    self.r.add("TA-ANSWER-LEAK", "blocking", f"{self.rel(p)}:{i}", "TA pack contains a literal answer")

    def check_wall(self) -> None:
        pattern = re.compile(r"instructor/|quiz-m\d+-key|ta-feedback|instructor key", re.I)
        student: list[Path] = []
        student += list((self.root / "03-assessments/student").glob("*.md"))
        student += list((self.root / "02-deck").glob("*.md"))
        student += list((self.root / "04-labs").glob("*.md"))
        student += [self.root / "01-syllabus/syllabus.md"]
        for p in student:
            if not p.is_file():
                continue
            for i, line in enumerate(read(p).splitlines(), 1):
                if pattern.search(line):
                    self.r.add("WALL-LEAK", "blocking", f"{self.rel(p)}:{i}", "student-visible file references the instructor tree")

    # ---- labs -----------------------------------------------------------

    def check_labs(self) -> None:
        for p in sorted((self.root / "04-labs").glob("lab-m*.md")):
            rel = self.rel(p)
            mnum = int(re.search(r"m(\d+)", p.stem).group(1))
            text = read(p)
            steps = list(re.finditer(r"^###\s+Step\s+(\d+)\s+-\s+(.+?)\s*$", text, re.M))
            if not steps:
                self.r.add("LAB-STEPS", "blocking", rel, "no '### Step N - title' headings")
                continue
            if steps[0].group(1) != "0":
                self.r.add("LAB-STEPS", "blocking", rel, "the first step must be Step 0")
            if "debrief" not in steps[-1].group(2).lower():
                self.r.add("LAB-STEPS", "blocking", rel, "the last step must be the debrief")
            total = 0
            for i, st in enumerate(steps):
                end = steps[i + 1].start() if i + 1 < len(steps) else len(text)
                body = text[st.end():end]
                body = body.split("\n## ")[0]
                t = re.search(r"\*\*Time:\*\*\s*(\d+)", body)
                if not t:
                    self.r.add("LAB-TIME", "blocking", rel, f"step {st.group(1)} has no Time")
                else:
                    total += int(t.group(1))
                    if st.group(1) == "0" and int(t.group(1)) > 10:
                        self.r.add("LAB-STEP0", "minor", rel, "step 0 is over ten minutes; setup is five")
                if st.group(1) != "0" and "debrief" not in st.group(2).lower():
                    for f in ("Starting state", "Task", "Prediction", "Action", "Evidence", "Interpretation", "Recovery", "Why this matters"):
                        if not re.search(rf"\*\*{f}:\*\*", body):
                            self.r.add("LAB-STEP-FIELDS", "blocking", rel, f"step {st.group(1)} has no '{f}'")
            mod = next((m for m in self.modules if m.number == mnum), None)
            if mod and mod.hands_on_min is not None:
                if total > mod.hands_on_min or total < mod.hands_on_min * 0.8:
                    self.r.add("LAB-TIME-SUM", "blocking", rel, f"step times sum to {total} but hands-on is {mod.hands_on_min}; allowed range is {round(mod.hands_on_min * 0.8)} to {mod.hands_on_min}")
                elif total != mod.hands_on_min:
                    self.r.add("LAB-TIME-SUM", "minor", rel, f"step times sum to {total} against {mod.hands_on_min} hands-on minutes")
            if not re.search(r"\*\*Planted defect:\*\*", text) or not re.search(r"Source of truth", text, re.I):
                self.r.add("LAB-DEFECT", "blocking", rel, "no planted defect with a stated source of truth")
            if not re.search(r"^##\s+Troubleshooting", text, re.M | re.I):
                self.r.add("LAB-TROUBLESHOOTING", "blocking", rel, "no troubleshooting table")
            if "Unexecuted teaching sample" not in text:
                self.r.add("LAB-DISCLOSURE", "minor", rel, "no unexecuted-step disclosure; labs are written, not run")
            self.r.metrics.setdefault("labs", {})[f"m{mnum:02d}"] = {"step_minutes": total, "hands_on": mod.hands_on_min if mod else None}

    # ---- citations, alignment, manifest ---------------------------------

    def check_citations(self) -> None:
        skip = {"00-viability/source-pack.md"}
        count = 0
        for p in self.md_files():
            rel = self.rel(p)
            if rel in skip or rel == "APPROVALS.md":
                continue
            for i, line in enumerate(read(p).splitlines(), 1):
                for sid in SP_RE.findall(line):
                    count += 1
                    if self.sp_ids and sid not in self.sp_ids:
                        self.r.add("SP-UNRESOLVED", "blocking", f"{rel}:{i}", f"{sid} does not exist in the source pack")
        self.r.metrics["citations"] = count

    def check_alignment(self) -> None:
        p = self.root / "qa/alignment-matrix.md"
        if not p.is_file():
            return
        rel = self.rel(p)
        rows = table_rows(read(p), re.compile(r"LO-\d+"))
        have = {r[0] for r in rows}
        for lo in self.outcomes:
            if lo not in have:
                self.r.add("ALIGN-MISSING", "blocking", rel, f"{lo} has no row")
        empty = 0
        for r in rows:
            for c in r:
                if not c or c.lower() in ("tbd", "none", "-"):
                    empty += 1
        if empty:
            self.r.add("ALIGN-EMPTY", "blocking", rel, f"{empty} empty cell(s); every cell must name slides, items, or steps")
        self.r.metrics["alignment_empty_cells"] = empty

    def check_ta_manifest(self) -> None:
        p = self.root / "qa/ta-grounding-manifest.md"
        if not p.is_file():
            return
        rel = self.rel(p)
        for m in re.finditer(r"`(courses/[^`]+)`", read(p)):
            path = m.group(1)
            if "03-assessments/instructor/" in path and "ta-feedback-pack" not in path:
                self.r.add("TA-MANIFEST", "blocking", rel, f"manifest lists instructor material: {path}")
            if not (REPO / path).is_file() and not (self.root.parent.parent / path).is_file():
                self.r.add("TA-MANIFEST", "minor", rel, f"manifest lists a file that does not exist: {path}")

    # ---- driver ---------------------------------------------------------

    def run(self) -> None:
        # The syllabus sets the module count, so read it before the manifest.
        self.check_syllabus()
        self.check_manifest()
        self.check_generic()
        self.check_brief()
        self.check_source_pack()
        if self.at_least("production"):
            self.check_decks()
            self.check_quizzes()
            self.check_ta_packs()
            self.check_labs()
            self.check_wall()
        if self.at_least("package"):
            self.check_alignment()
        if self.at_least("published"):
            self.check_ta_manifest()
        self.check_citations()
        if self.check_pdf:
            self.check_pdfs()


def check_course(root: Path, through: str = "package", check_pdf: bool = True) -> Report:
    report = Report()
    Course(root, report, through, check_pdf).run()
    return report


def print_report(slug: str, through: str, report: Report) -> None:
    print(f"check_package: {slug} through {through}")
    order = {"blocking": 0, "minor": 1}
    for f in sorted(report.findings, key=lambda f: (order[f.severity], f.code, f.path)):
        print(f"  {f.severity.upper():8} {f.code:22} {f.path}: {f.message}  -> {f.owner}")
    m = report.metrics
    print("metrics:")
    print(f"  claims in source pack: {m.get('claims', 0)}, citations: {m.get('citations', 0)}")
    for k, d in m.get("decks", {}).items():
        print(f"  deck {k}: {d['slides']} slides, longest abstract run {d['longest_abstract_run']}, "
              f"notes {d['note_words']} words vs budget {d['word_budget']}, narration gap {d['narration_gap_minutes']} min")
    for k, d in m.get("labs", {}).items():
        print(f"  lab {k}: step minutes {d['step_minutes']} vs hands-on {d['hands_on']}")
    if "alignment_empty_cells" in m:
        print(f"  alignment empty cells: {m['alignment_empty_cells']}")
    print(f"result: {report.blocking} blocking, {report.minor} minor")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("--through", choices=STAGES, default="package")
    ap.add_argument("--no-pdf", action="store_true", help="skip the PDF existence and freshness check")
    ap.add_argument("--courses-dir", type=Path, default=REPO / "courses")
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    args = ap.parse_args(argv)

    root = args.courses_dir / args.slug
    if not root.is_dir():
        print(f"error: no course at {root}", file=sys.stderr)
        return 2
    report = check_course(root, args.through, not args.no_pdf)
    if args.json:
        print(json.dumps({"findings": [asdict(f) for f in report.findings], "metrics": report.metrics,
                          "blocking": report.blocking, "minor": report.minor}, indent=2))
    else:
        print_report(args.slug, args.through, report)
    return 1 if report.blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
