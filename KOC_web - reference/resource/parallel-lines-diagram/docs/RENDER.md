# Render & preview

Run all commands from the **repo root**.

## Quick render

```powershell
.\adhoc\parallel-lines-diagram\render.ps1
```

## Manual commands

### Still PNG (white background)

```powershell
.venv\Scripts\manim.exe --media_dir media/adhoc -ql `
  adhoc/parallel-lines-diagram/manim/diagram.py ParallelLinesStill -o parallel-lines-still
```

Output: `media/adhoc/images/diagram/parallel-lines-still.png`  
Copy also kept at: `adhoc/parallel-lines-diagram/output/parallel-lines-still.png`

### HTML slides (black background, one beat)

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides `
  -Quality ql `
  -MediaDir media/adhoc
```

`render_slides.ps1` also:
- syncs MP4(s) into `slides/index_assets/`
- enables `autoPlayMedia`
- writes `index.html` as **UTF-8 without BOM** (BOM breaks Reveal.js)

## Preview (local server required)

```powershell
python -m http.server 8000
```

| URL | Purpose |
|-----|---------|
| http://localhost:8000/adhoc/parallel-lines-diagram/slides/index.html | manim-slides deck |
| http://localhost:8000/adhoc/parallel-lines-diagram/slides/preview.html | plain `<video>` fallback |

### Segment lengths (9 beats)

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesSegmentLengthsDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/segment-lengths `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/segment-lengths/index.html`

### Angle marks (4 beats)

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesAngleMarksDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/angle-marks `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/angle-marks/index.html`

### Area comparison (9 beats)

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesAreaCompareDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/area-comparison `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/area-comparison/index.html`

### Triangle regions (7 beats)

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesTriangleRegionsDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/triangle-regions `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/triangle-regions/index.html`

### DE ∥ BF parallel (8 beats)

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesDeBfParallelDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/de-bf-parallel `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/de-bf-parallel/index.html`

### CGB angle marks (8 beats)

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesCgbAngleMarksDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/cgb-angle-marks `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/cgb-angle-marks/index.html`

### CHB lift (3 beats)

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesChbLiftDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/chb-lift `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/chb-lift/index.html`

### CHB regions (4 beats)

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesChbRegionsDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/chb-regions `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/chb-regions/index.html`

### CHB regions continuation (1 beat — stub)

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesChbRegionsContDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/chb-regions-cont `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/chb-regions-cont/index.html`

### CHB HBG restore (3 beats)

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesChbHbgRestoreDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/chb-hbg-restore `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/chb-hbg-restore/index.html`

### CHB HBG marks (7 beats)

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesChbHbgMarksDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/chb-hbg-marks `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/chb-hbg-marks/index.html`

### CHB HBG k regions (5 beats)

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesChbHbgKRegionsDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/chb-hbg-k-regions `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/chb-hbg-k-regions/index.html`

### CHB HBG k trim (4 beats)

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesChbHbgKTrimDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/chb-hbg-k-trim `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/chb-hbg-k-trim/index.html`

Hard-refresh (`Ctrl+Shift+R`) if a previous blank deck is cached.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Blank white slide | Missing `index_assets/*.mp4` — re-run `render.ps1` |
| Blank after patch | UTF-8 BOM in `index.html` — re-run `render_slides.ps1` (writes no-BOM) |
| `preview.html` works, `index.html` does not | Same as above; confirm no BOM (`EF BB BF` bytes at file start) |
