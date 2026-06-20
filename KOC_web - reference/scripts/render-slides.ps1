# Build and optionally present Manim Slides
param(
    [Parameter(Mandatory = $true)]
    [string]$SlidesFile,
    [switch]$Present
)

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$VenvManimSlides = Join-Path $Root ".venv\Scripts\manim-slides.exe"

if (-not (Test-Path $VenvManimSlides)) {
    Write-Error "manim-slides not installed. Run: .\.venv\Scripts\pip install -r requirements.txt"
    exit 1
}

Push-Location $Root
try {
    & $VenvManimSlides render $SlidesFile
    if ($Present) {
        $base = [System.IO.Path]::GetFileNameWithoutExtension($SlidesFile)
        & $VenvManimSlides present $base
    }
}
finally {
    Pop-Location
}
