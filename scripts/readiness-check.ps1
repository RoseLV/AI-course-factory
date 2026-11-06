# Five PASS or FAIL lines. Fix any FAIL before running the pipeline.
$repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$fail = 0

function Report($ok, $name, $hint) {
    if ($ok) { Write-Host "PASS  $name" }
    else { Write-Host "FAIL  $name  ($hint)"; $script:fail++ }
}

Report ($null -ne (Get-Command git -ErrorAction SilentlyContinue)) "git installed" "install Git"
Report ($null -ne (Get-Command uv -ErrorAction SilentlyContinue)) "uv installed" "install from https://docs.astral.sh/uv/"

$chromeCandidates = @(
    $env:CHROME_PATH,
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
) | Where-Object { $_ -and (Test-Path $_) }
Report ($chromeCandidates.Count -gt 0) "Chrome found" "install Chrome or set CHROME_PATH"

Report ($null -ne (Get-Command claude -ErrorAction SilentlyContinue)) "Claude Code installed" "install Claude Code, then run: claude"

$need = @("CLAUDE.md", "STYLE.md", "build\render.py", ".claude\agents")
$missing = $need | Where-Object { -not (Test-Path (Join-Path $repo $_)) }
Report ($missing.Count -eq 0) "repo files present" ("missing: " + ($missing -join ", "))

exit $fail
