# Render a course to PDF. Usage: ./run.ps1 <slug> [render.py flags...]
# Wraps: uv run --quiet --with markdown --with pygments python build/render.py <slug> ...
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$Slug,
    [Parameter(ValueFromRemainingArguments = $true)][string[]]$Rest
)
$repo = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $repo
try {
    uv run --quiet --with markdown --with pygments python build/render.py $Slug @Rest
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
