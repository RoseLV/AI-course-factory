#!/usr/bin/env bash
# Five PASS or FAIL lines. Fix any FAIL before running the pipeline.
repo="$(cd "$(dirname "$0")/.." && pwd)"
fail=0

report() {  # report <ok 0|1> <name> <hint>
    if [ "$1" -eq 0 ]; then echo "PASS  $2"; else echo "FAIL  $2  ($3)"; fail=$((fail + 1)); fi
}

command -v git >/dev/null 2>&1; report $? "git installed" "install Git"
command -v uv >/dev/null 2>&1; report $? "uv installed" "install from https://docs.astral.sh/uv/"

chrome_ok=1
for c in "$CHROME_PATH" /usr/bin/google-chrome "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
         "/c/Program Files/Google/Chrome/Application/chrome.exe"; do
    if [ -n "$c" ] && [ -e "$c" ]; then chrome_ok=0; break; fi
done
report $chrome_ok "Chrome found" "install Chrome or set CHROME_PATH"

command -v claude >/dev/null 2>&1; report $? "Claude Code installed" "install Claude Code, then run: claude"

missing=""
for f in CLAUDE.md STYLE.md build/render.py .claude/agents; do
    [ -e "$repo/$f" ] || missing="$missing $f"
done
[ -z "$missing" ]; report $? "repo files present" "missing:$missing"

exit $fail
