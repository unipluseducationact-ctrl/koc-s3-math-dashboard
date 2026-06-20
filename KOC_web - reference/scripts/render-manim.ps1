# Render a Manim scene (low quality preview by default)
param(
    [Parameter(Mandatory = $true)]
    [string]$SceneFile,
    [string]$SceneName,
    [ValidateSet("l", "m", "h", "p", "k")]
    [string]$Quality = "l"
)

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"
$ManimCfg = Join-Path $Root "manim\manim.cfg"

if (-not (Test-Path $VenvPython)) {
    Write-Error "Virtual environment not found. Run: python -m venv .venv; .\.venv\Scripts\pip install -r requirements.txt"
    exit 1
}

$args = @("-m", "manim", "-c", $ManimCfg, "-q$Quality")
if ($SceneName) { $args += $SceneName }
$args += $SceneFile

& $VenvPython @args
