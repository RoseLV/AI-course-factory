#!/usr/bin/env python3
"""Render a course's markdown artifacts to PDF.

Markdown stays the master (STYLE.md "Files and naming"). Markdown in, PDF out,
nothing authored here. Ported from the earlier pipeline's renderer.

Run it through uv so no system Python is needed (or use run.ps1 / run.sh):

    uv run --with markdown --with pygments python build/render.py intro-sql-hs

The main session renders a stage after its agent finishes, with --only:

    uv run --with markdown --with pygments python build/render.py intro-sql-hs --only 02-deck

Outputs land in courses/{slug}/dist/ and are gitignored. They are build
artifacts: regenerate rather than edit.
"""

from __future__ import annotations

import argparse
import base64
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown
from pygments.formatters import HtmlFormatter

REPO = Path(__file__).resolve().parent.parent
THEMES = Path(__file__).resolve().parent / "themes"

MD_EXTENSIONS = [
    "extra",          # tables, fenced code, attr_list, def_list
    "sane_lists",
    "codehilite",
    "admonition",
]
MD_CONFIG = {
    "codehilite": {"guess_lang": False, "noclasses": False},
}

# 16:9 at 96dpi. Chrome honours @page size, so one slide == one page exactly.
SLIDE_W_IN = 13.333
SLIDE_H_IN = 7.5


# --------------------------------------------------------------------------
# chrome
# --------------------------------------------------------------------------

def find_chrome() -> str:
    candidates = [
        os.environ.get("CHROME_PATH", ""),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        "/usr/bin/google-chrome",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for c in candidates:
        if c and Path(c).exists():
            return c
    sys.exit("error: Chrome not found. Set CHROME_PATH to the chrome binary.")


def html_to_pdf(chrome: str, html_text: str, out_pdf: Path) -> None:
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    tmpdir = Path(tempfile.mkdtemp(prefix="render-"))
    try:
        src = tmpdir / "page.html"
        src.write_text(html_text, encoding="utf-8")
        cmd = [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=10000",
            f"--print-to-pdf={out_pdf}",
            src.as_uri(),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if not out_pdf.exists():
            sys.exit(
                f"error: chrome produced no PDF for {out_pdf.name}\n"
                f"{proc.stdout}\n{proc.stderr}"
            )
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# --------------------------------------------------------------------------
# markdown helpers
# --------------------------------------------------------------------------

def split_front_matter(text: str) -> tuple[dict, str]:
    """Pull the leading --- ... --- block. Deliberately not a YAML parser:
    the briefs specify flat key/value front matter."""
    if not text.lstrip().startswith("---"):
        return {}, text
    body = text.lstrip()
    end = body.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = body[3:end].strip("\n")
    rest = body[end + 4:].lstrip("\n")
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, rest


def md_to_html(text: str) -> str:
    md = markdown.Markdown(extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG)
    return md.convert(text)


FONTS = Path(__file__).resolve().parent / "fonts"

# Weight-name pairs are enough: every file here is <family>-<weight>.woff2.
def font_faces() -> str:
    """@font-face rules with the font bytes inlined.

    Chrome renders from a temp directory, so a relative font path resolves to
    nothing and the page silently falls back to a different typeface. Inlining
    is what makes a theme's font choice actually hold."""
    if not FONTS.is_dir():
        return ""
    out = []
    for f in sorted(FONTS.glob("*.woff2")):
        family, _, weight = f.stem.rpartition("-")
        if not (family and weight.isdigit()):
            continue
        b64 = base64.b64encode(f.read_bytes()).decode("ascii")
        out.append(
            f"@font-face{{font-family:'{family.title()}';font-style:normal;"
            f"font-weight:{weight};font-display:block;"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
        )
    return "\n".join(out)


def read_theme(theme: str) -> str:
    """Layout lives in _base.css; a theme file supplies only the palette and
    type choices, so a reskin is one small file."""
    path = THEMES / f"{theme}.css"
    if not path.exists():
        available = ", ".join(
            sorted(p.stem for p in THEMES.glob("*.css") if not p.stem.startswith("_"))
        )
        sys.exit(f"error: unknown theme {theme!r}. Available: {available}")
    base = (THEMES / "_base.css").read_text(encoding="utf-8")
    return path.read_text(encoding="utf-8") + "\n" + base


def pygments_css() -> str:
    return HtmlFormatter(style="friendly").get_style_defs(".codehilite")


# --------------------------------------------------------------------------
# document rendering
# --------------------------------------------------------------------------

DOC_SHELL = """<!doctype html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
@page {{ size: A4; margin: 20mm 18mm; }}
{fonts}
{theme}
{pygments}
</style></head>
<body class="doc {body_class}">
{frame_open}
<header class="doc-head">
  <div class="doc-kicker">{kicker}</div>
  <h1 class="doc-title">{title}</h1>
  <div class="doc-meta">{meta}</div>
</header>
<main>
{content}
</main>
<footer class="doc-foot">{footer}</footer>
{frame_close}
</body></html>
"""

# The "Instructor only" warning must print on every page without covering a line
# of the document. Chrome repeats a thead on each page a table breaks across, and
# a thead is in flow, so it reserves the space it occupies rather than painting
# over the text underneath -- which is what the position: fixed ribbon this
# replaces did to every page after the first. See .page-frame in themes/_base.css
# for the mechanisms that were measured and rejected.
INSTRUCTOR_FRAME_OPEN = (
    '<table class="page-frame"><thead><tr><td>'
    '<div class="instructor-ribbon">Instructor only. '
    'Not for student distribution.</div>'
    '</td></tr></thead><tbody><tr><td>'
)
INSTRUCTOR_FRAME_CLOSE = "</td></tr></tbody></table>"


def render_document(
    chrome: str, src: Path, out_pdf: Path, theme_css: str, *,
    slug: str, instructor: bool = False,
) -> None:
    raw = src.read_text(encoding="utf-8")
    meta, body = split_front_matter(raw)

    # Prefer a leading H1 as the title, and drop it so it is not printed twice.
    title = meta.get("title", "")
    m = re.match(r"\s*#\s+(.+?)\s*\n", body)
    if m:
        if not title:
            title = m.group(1)
        body = body[m.end():]
    if not title:
        title = src.stem.replace("-", " ")

    content = inline_images(md_to_html(body), src.parent, src.name)

    meta_bits = [f"{k}: {v}" for k, v in meta.items() if k not in ("title",)]
    footer_bits = [b for b in ("Course Factory Lite", slug) if b]

    page = DOC_SHELL.format(
        title=html.escape(title),
        fonts=font_faces(),
        theme=theme_css,
        pygments=pygments_css(),
        body_class="instructor" if instructor else "",
        frame_open=INSTRUCTOR_FRAME_OPEN if instructor else "",
        frame_close=INSTRUCTOR_FRAME_CLOSE if instructor else "",
        kicker=html.escape(slug),
        meta=html.escape(" &middot; ".join(meta_bits)) if meta_bits else "",
        content=content,
        footer=html.escape(" &middot; ".join(footer_bits)),
    )
    # meta/footer joined with an HTML entity: unescape the separator only.
    page = page.replace("&amp;middot;", "&middot;")
    html_to_pdf(chrome, page, out_pdf)


IMG_SRC_RE = re.compile(r'(<img[^>]*?src=")([^"]+)(")', re.I)


def inline_images(html_text: str, base: Path, label: str) -> str:
    """Rewrite every local <img src> to a data URI, relative to the markdown
    file. Chrome renders from a temp directory, so a relative path would
    resolve to nothing and print a broken image into the PDF."""
    def swap(m: re.Match) -> str:
        raw = m.group(2)
        if raw.startswith(("data:", "http://", "https://")):
            return m.group(0)
        target = (base / raw).resolve()
        if not target.is_file():
            print(f"  warn  {label}: image not found: {raw}")
            return m.group(0)
        if target.suffix.lower() not in IMAGE_MIME:
            print(f"  warn  {label}: not an image: {raw}")
            return m.group(0)
        return m.group(1) + data_uri(target) + m.group(3)
    return IMG_SRC_RE.sub(swap, html_text)


# --------------------------------------------------------------------------
# deck rendering
# --------------------------------------------------------------------------

SLIDE_RE = re.compile(r"^##\s+Slide\s+(\d+)\s*:\s*(.+?)\s*$", re.M)
# Visual-src before Visual: the alternation is ordered, and the longer key
# would otherwise be swallowed by the shorter one.
KEY_RE = re.compile(r"^(Visual-src|Visual|Notes|Covers)\s*:\s*(.*)$", re.I)
KEY_ATTR = {
    "visual-src": "visual_src",
    "visual": "visual",
    "notes": "notes",
    "covers": "covers",
}
SCRIPT_RE = re.compile(r"<script\b.*?</script\s*>", re.S | re.I)
IMAGE_MIME = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml",
}


class Slide:
    def __init__(self, number: str, title: str) -> None:
        self.number = number
        self.title = title
        self.bullets: list[str] = []
        self.code: list[tuple[str, str]] = []   # (lang, source)
        self.visual = ""        # designer intent; also the alt text
        self.svg = ""           # inline ```svg block, the authored diagram
        self.visual_src = ""    # path to an image asset, relative to the deck
        self.notes = ""
        self.covers = ""


def parse_deck(text: str) -> tuple[dict, list[Slide]]:
    meta, body = split_front_matter(text)
    slides: list[Slide] = []

    marks = list(SLIDE_RE.finditer(body))
    for i, mark in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        block = body[mark.end():end]
        slide = Slide(mark.group(1), mark.group(2))

        # Lift fenced blocks out first so their contents are never parsed as
        # keys. An ```svg fence is the slide's diagram, not code to display.
        def take_code(m: re.Match) -> str:
            lang = (m.group(1) or "text").lower()
            if lang == "svg":
                slide.svg = m.group(2).strip()
            else:
                slide.code.append((lang, m.group(2)))
            return ""

        block = re.sub(r"```(\w*)\n(.*?)```", take_code, block, flags=re.S)

        current: str | None = None
        for line in block.splitlines():
            key = KEY_RE.match(line.strip())
            if key:
                current = KEY_ATTR[key.group(1).lower()]
                setattr(slide, current, key.group(2).strip())
                continue
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith(("-", "*")) and current is None:
                slide.bullets.append(stripped.lstrip("-* ").strip())
            elif current:
                setattr(slide, current, (getattr(slide, current) + " " + stripped).strip())
        slides.append(slide)

    return meta, slides


# Arrowheads live once per document so an authored diagram can just say
# marker-end="url(#arrow)". Defining markers is the most error-prone part of
# hand-written SVG, and every deck needs the same two.
SVG_SPRITE = """<svg class="svg-sprite" aria-hidden="true"><defs>
<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
        markerWidth="6" markerHeight="6" orient="auto-start-reverse">
  <path d="M0,0 L10,5 L0,10 z" class="fill-ink"/>
</marker>
<marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5"
        markerWidth="6" markerHeight="6" orient="auto-start-reverse">
  <path d="M0,0 L10,5 L0,10 z" class="fill-accent"/>
</marker>
<marker id="arrow-muted" viewBox="0 0 10 10" refX="9" refY="5"
        markerWidth="6" markerHeight="6" orient="auto-start-reverse">
  <path d="M0,0 L10,5 L0,10 z" class="fill-muted"/>
</marker>
</defs></svg>"""

DECK_SHELL = """<!doctype html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
@page {{ size: {w}in {h}in; margin: 0; }}
{fonts}
{theme}
{pygments}
</style></head>
<body class="deck {mode}">
{sprite}
{slides}
</body></html>
"""


def data_uri(path: Path) -> str:
    mime = IMAGE_MIME.get(path.suffix.lower(), "application/octet-stream")
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def visual_html(slide: Slide, asset_dir: Path, warn) -> str:
    """The slide's visual, in priority order: authored SVG, then image asset,
    then the dashed placeholder holding the designer instruction.

    The placeholder is deliberate. An unillustrated slide should look
    obviously unfinished rather than quietly shipping as if it were done."""
    alt = html.escape(slide.visual or "Slide visual")

    if slide.svg:
        svg = SCRIPT_RE.sub("", slide.svg).strip()
        if not svg.lstrip().startswith("<svg"):
            warn(f"slide {slide.number}: ```svg block does not start with <svg>; ignored")
        else:
            if "viewBox" not in svg:
                warn(
                    f"slide {slide.number}: inline svg has no viewBox, so it "
                    f"cannot scale to the slide. Add one."
                )
            return f'<figure class="visual visual-live" role="img" aria-label="{alt}">{svg}</figure>'

    if slide.visual_src:
        src = (asset_dir / slide.visual_src).resolve()
        if not src.is_file():
            warn(f"slide {slide.number}: Visual-src not found: {slide.visual_src}")
            return (
                '<figure class="visual visual-missing"><figcaption>Missing asset</figcaption>'
                f"<p>{html.escape(slide.visual_src)}</p></figure>"
            )
        if src.suffix.lower() not in IMAGE_MIME:
            warn(f"slide {slide.number}: Visual-src is not an image: {slide.visual_src}")
        else:
            return (
                '<figure class="visual visual-live">'
                f'<img src="{data_uri(src)}" alt="{alt}"></figure>'
            )

    if slide.visual:
        return (
            '<figure class="visual"><figcaption>Visual</figcaption>'
            f"<p>{html.escape(slide.visual)}</p></figure>"
        )
    return ""


def slide_html(
    slide: Slide, *, slug: str, total: int, with_notes: bool,
    asset_dir: Path, warn,
) -> str:
    visual = visual_html(slide, asset_dir, warn)
    live = "visual-live" in visual

    text: list[str] = []
    if slide.bullets:
        text.append('<ul class="slide-bullets">')
        for b in slide.bullets:
            text.append(f"<li>{md_inline(b)}</li>")
        text.append("</ul>")
    for lang, source in slide.code:
        text.append(md_to_html(f"```{lang}\n{source}```"))

    # A real visual beside text earns a two-column slide. A real visual with
    # nothing beside it gets the full width. A placeholder never splits: half
    # a slide of dashed box reads as a layout bug rather than as missing art.
    split = live and bool(text)

    parts = ['<section class="slide">']
    parts.append('<div class="slide-body">')
    parts.append(f'<h2 class="slide-title">{html.escape(slide.title)}</h2>')
    parts.append(f'<div class="slide-content{" split" if split else ""}">')
    if text:
        parts.append('<div class="col-text">')
        parts.extend(text)
        parts.append("</div>")
    if visual:
        parts.append(f'<div class="col-visual">{visual}</div>')
    parts.append("</div>")  # slide-content
    parts.append("</div>")  # slide-body
    parts.append(
        '<div class="slide-foot">'
        f'<span class="foot-left">Course Factory Lite &middot; {html.escape(slug)}</span>'
        f'<span class="foot-mid">{html.escape(slide.covers)}</span>'
        f'<span class="foot-right">{html.escape(slide.number)} / {total}</span>'
        "</div>"
    )
    parts.append("</section>")

    if with_notes:
        parts.append(
            '<section class="notes-page">'
            f'<div class="notes-head">Slide {html.escape(slide.number)}: '
            f"{html.escape(slide.title)}</div>"
            f'<div class="notes-body">{md_inline(slide.notes) or "<em>No speaker notes supplied.</em>"}</div>'
            f'<div class="notes-covers">{html.escape(slide.covers)}</div>'
            "</section>"
        )
    return "\n".join(parts)


def md_inline(text: str) -> str:
    """Inline markdown only: bold, italic, code. Keeps bullets on one line."""
    out = html.escape(text)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", out)
    return out


def render_deck(
    chrome: str, src: Path, out_dir: Path, theme_css: str, *, slug: str,
) -> list[Path]:
    meta, slides = parse_deck(src.read_text(encoding="utf-8"))
    if not slides:
        print(f"  skip {src.name}: no '## Slide N:' headings found")
        return []

    seen: set[str] = set()

    def warn(msg: str) -> None:
        # Both passes render the same slides; report each problem once.
        if msg not in seen:
            seen.add(msg)
            print(f"  warn  {src.name}: {msg}")

    placeholders = [s.number for s in slides if s.visual and not (s.svg or s.visual_src)]

    written = []
    title = meta.get("module", src.stem)
    for with_notes, suffix in ((False, ""), (True, "-instructor")):
        body = "\n".join(
            slide_html(
                s, slug=slug, total=len(slides), with_notes=with_notes,
                asset_dir=src.parent, warn=warn,
            )
            for s in slides
        )
        page = DECK_SHELL.format(
            title=html.escape(f"{slug} {title}"),
            fonts=font_faces(),
            theme=theme_css,
            pygments=pygments_css(),
            w=SLIDE_W_IN,
            h=SLIDE_H_IN,
            mode="with-notes" if with_notes else "projection",
            sprite=SVG_SPRITE,
            slides=body,
        )
        out = out_dir / f"{src.stem}{suffix}.pdf"
        html_to_pdf(chrome, page, out)
        written.append(out)

    if placeholders:
        print(
            f"  warn  {src.name}: {len(placeholders)} slide(s) still show a "
            f"dashed placeholder instead of a visual: "
            f"{', '.join(placeholders)}. The deck is not finished."
        )
    return written


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

# (source subpath, output subpath, instructor-only, theme override or None)
# Lab guides always use the lab theme, which matches the house lab format.
DOC_MAP = [
    ("STATUS.md", "", False, None),
    ("APPROVALS.md", "", False, None),
    ("00-viability", "00-viability", False, None),
    ("01-syllabus", "01-syllabus", False, None),
    ("03-assessments/student", "03-assessments/student", False, None),
    ("03-assessments/instructor", "03-assessments/instructor", True, None),
    ("04-labs", "04-labs", False, "lab"),
    ("qa", "qa", False, None),
    ("maintenance", "maintenance", False, None),
]


# Files that scripts append to. They are data, not documents: no front matter and no PDF, because a
# PDF of a file that changes after every TA question would be stale the moment it was made.
DATA_FILES = {"maintenance/ta-log.md"}

# Machine droppings, never a document. Anything else below a stage is named in
# the warning rather than filtered here: deciding for the author which of their
# files "obviously" was not meant to render is how the silence started.
NON_DOC_DIRS = re.compile(r"^(\..+|__pycache__|node_modules)$")


def skipped_markdown(stage: Path) -> list[str]:
    """Markdown under a stage that the top-level scan does not render.

    A stage's documents live at its top level and nested folders are material:
    lab starter repos, video scenes, caches. That is the contract, but it used to
    be enforced in silence -- a document written one folder too deep produced no
    PDF and no warning, and stayed unrenderable for as long as nobody noticed.
    Naming the skipped files does not render them; it makes the gap visible."""
    out = []
    for root, dirs, files in os.walk(stage):
        # Prune, do not filter afterwards: walking a node_modules in full just to
        # throw the result away is the slow way to ignore it.
        dirs[:] = [d for d in dirs if not NON_DOC_DIRS.match(d)]
        rel_root = Path(root).relative_to(stage)
        if rel_root == Path("."):
            continue                      # rendered by the top-level scan
        out += [(rel_root / f).as_posix() for f in files if f.lower().endswith(".md")]
    return sorted(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("slug", help="course slug under courses/")
    ap.add_argument(
        "--theme", default="neutral",
        help="theme name from build/themes/ (default: neutral). Lab guides "
             "always render with the 'lab' theme.",
    )
    ap.add_argument("--clean", action="store_true", help="wipe dist/ first")
    ap.add_argument(
        "--only", action="append", metavar="PATH", default=None,
        help="render just this course-relative source path, e.g. '02-deck' or "
             "'STATUS.md'. Repeatable. Render one stage at a time so an "
             "in-flight draft is never shipped as finished. Omit to render the "
             "whole course.",
    )
    args = ap.parse_args()

    course = REPO / "courses" / args.slug
    if not course.is_dir():
        sys.exit(f"error: no course at {course}")

    only = [o.replace("\\", "/").strip("/") for o in (args.only or [])]
    if only:
        known = [rel for rel, _, _, _ in DOC_MAP] + ["02-deck"]
        for o in only:
            # A stage, or a parent of stages (03-assessments covers both halves).
            if any(o == k or k.startswith(o + "/") for k in known):
                continue
            # A path *inside* a stage used to pass this check and then widen
            # silently: --only 05-demo/video rendered the whole of 05-demo and
            # reported success. --only selects whole stages, so say so.
            inside = next((k for k in known if o.startswith(k + "/")), None)
            if inside:
                sys.exit(
                    f"error: --only {o} names a path inside {inside}, and --only "
                    f"selects whole stages, not paths within one.\n"
                    f"       use --only {inside} to render it."
                )
            sys.exit(
                f"error: --only {o} matches no renderable path.\n"
                f"       renderable paths: {', '.join(known)}"
            )

    def wanted(rel: str) -> bool:
        """No --only renders everything; otherwise match a stage or its parent.

        Deliberately no third clause matching an --only that sits *below* rel:
        that is what made --only 05-demo/video render the whole of 05-demo. The
        argument check above rejects those before we get here."""
        if not only:
            return True
        rel = rel.replace("\\", "/")
        return any(rel == o or rel.startswith(o + "/") for o in only)

    dist = course / "dist"
    if args.clean and dist.exists():
        if only:
            sys.exit("error: --clean wipes the whole dist/; do not combine it with --only")
        shutil.rmtree(dist)

    chrome = find_chrome()
    theme_css = read_theme(args.theme)
    count = 0

    scope = f" ({', '.join(only)})" if only else ""
    print(f"rendering {args.slug} with theme {args.theme}{scope}")

    for rel, out_rel, instructor, theme_override in DOC_MAP:
        if not wanted(rel):
            continue
        doc_css = read_theme(theme_override) if theme_override else theme_css
        src = course / rel
        if src.is_file():
            out = dist / (Path(out_rel) / f"{src.stem}.pdf" if out_rel else f"{src.stem}.pdf")
            render_document(chrome, src, out, doc_css, slug=args.slug, instructor=instructor)
            print(f"  doc   {rel} -> {out.relative_to(dist)}")
            count += 1
        elif src.is_dir():
            for md in sorted(src.glob("*.md")):
                if f"{rel}/{md.name}" in DATA_FILES:
                    continue
                out = dist / out_rel / f"{md.stem}.pdf"
                render_document(chrome, md, out, doc_css, slug=args.slug, instructor=instructor)
                print(f"  doc   {rel}/{md.name} -> {out.relative_to(dist)}")
                count += 1
            deeper = skipped_markdown(src)
            if deeper:
                print(
                    f"  warn  {rel}: {len(deeper)} markdown file(s) below the "
                    f"top level of the stage, which this scan does not render: "
                    f"{', '.join(deeper)}. Move a document up to {rel}/ to "
                    f"render it; anything meant as material can stay."
                )

    deck_dir = course / "02-deck"
    if deck_dir.is_dir() and wanted("02-deck"):
        for md in sorted(deck_dir.glob("deck-m*.md")):
            for out in render_deck(chrome, md, dist / "02-deck", theme_css, slug=args.slug):
                print(f"  deck  {md.name} -> {out.relative_to(dist)}")
                count += 1

    if count == 0:
        print(f"nothing to render yet: no markdown artifacts found{scope}")
    else:
        print(f"done: {count} PDFs in {dist}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
