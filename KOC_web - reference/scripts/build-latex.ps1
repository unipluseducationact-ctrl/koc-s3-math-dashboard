# Compile a LaTeX document with pdflatex
param(
    [Parameter(Mandatory = $true)]
    [string]$TexFile
)

$texPath = Resolve-Path $TexFile
$dir = Split-Path $texPath
$name = [System.IO.Path]::GetFileNameWithoutExtension($texPath)

Push-Location $dir
try {
    pdflatex -interaction=nonstopmode $name.tex
    pdflatex -interaction=nonstopmode $name.tex
    Write-Host "Output: $dir\$name.pdf"
}
finally {
    Pop-Location
}
