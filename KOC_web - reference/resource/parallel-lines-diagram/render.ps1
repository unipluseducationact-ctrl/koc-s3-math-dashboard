# Render still + slides for parallel-lines diagram.
# Usage (repo root): .\adhoc\parallel-lines-diagram\render.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Pkg = Join-Path $Root "adhoc\parallel-lines-diagram"
$ManimFile = Join-Path $Pkg "manim\diagram.py"
$SlidesDir = Join-Path $Pkg "slides"
$OutputDir = Join-Path $Pkg "output"
$MediaDir = "media/adhoc"

Set-Location $Root
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

Write-Host "=== Still PNG ==="
& .venv\Scripts\manim.exe --media_dir $MediaDir -ql $ManimFile ParallelLinesStill -o parallel-lines-still
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$stillSrc = Join-Path $Root "$MediaDir\images\diagram\parallel-lines-still.png"
$stillDst = Join-Path $OutputDir "parallel-lines-still.png"
Copy-Item $stillSrc $stillDst -Force
Write-Host "Copied still -> $stillDst"

Write-Host "=== HTML slides ==="
& .\scripts\render_slides.ps1 `
    -SceneFile "adhoc/parallel-lines-diagram/manim/diagram.py" `
    -SceneName ParallelLinesDraw `
    -OutputDir "adhoc/parallel-lines-diagram/slides" `
    -Quality ql `
    -MediaDir $MediaDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "Done."
Write-Host "  Still:  $stillDst"
Write-Host "  Slides: $SlidesDir\index.html"
Write-Host "  Preview http://localhost:8000/adhoc/parallel-lines-diagram/slides/index.html"
