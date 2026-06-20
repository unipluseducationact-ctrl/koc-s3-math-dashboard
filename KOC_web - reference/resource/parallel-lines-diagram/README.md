# Parallel-lines diagram

Self-contained ad hoc package: exam-style figure with parallel horizontals, quadrilateral **ABCD**, and intersections **G**, **H**.

## Folder layout

```
parallel-lines-diagram/
  README.md              ← this file
  render.ps1             ← one-command still + slides
  manim/
    diagram.py           ← Manim source (lines, labels, scenes)
  docs/
    CODE_MAP.md          ← which code creates which element
    GEOMETRY.md          ← topology + coordinates
    RENDER.md            ← render commands + troubleshooting
    CREATION_NOTES.md    ← build history + approved settings
  slides/
    index.html                  ← base diagram draw (1 beat)
    segment-lengths/index.html  ← k-label highlights (9 beats)
    angle-marks/index.html      ← parallel marks + angles + shaded regions (7 beats)
    area-comparison/index.html  ← △EAG vs △GBF compare + teardown (9 beats)
    triangle-regions/index.html ← △compare + k labels + areas (7 beats)
    de-bf-parallel/index.html   ← // DEBF + cleanup + restore (8 beats)
    cgb-angle-marks/index.html  ← angle pairs + ink trim (8 beats)
    chb-lift/index.html         ← △CHB lift + trim original (3 beats)
    chb-regions/index.html      ← k labels + △fills + 245 cm² (4 beats)
    chb-regions-cont/index.html ← merge HCB + red △HBG 175 cm² (6 beats)
    chb-hbg-restore/index.html  ← full graph + // marks + △HBG 175 cm² (4 beats)
    chb-hbg-marks/index.html    ← revised // + △CDH + angle pairs (7 beats)
    chb-hbg-k-regions/index.html ← △EAG/△GBF + k segment labels (5 beats)
    chb-hbg-k-trim/index.html   ← trim ink + △CDH 343 cm² + CDH-only frame (4 beats)
    eag-gbf-angles/index.html   ← isolated △EAG/△GBF + // + 3 angle pairs (7 beats)
    preview.html                ← plain video fallback
    index_assets/               ← slide MP4(s) (generated)
  output/
    parallel-lines-still.png   ← latest still (copy from media/)
```

## Quick start

```powershell
# From repo root
.\adhoc\parallel-lines-diagram\render.ps1
python -m http.server 8000
# → http://localhost:8000/adhoc/parallel-lines-diagram/slides/index.html
```

## Code → element map (summary)

| You want to change… | Edit in `manim/diagram.py` |
|---------------------|----------------------------|
| Vertex positions | `*_REF` constants |
| A line segment | `build_lines()` dict entry |
| A point label | `build_labels()` dict entry |
| Draw order | `LINE_ORDER` / `LABEL_ORDER` |
| Still colours | `INK`, `BG` |
| Slide colours | `DRAW_INK`, `DRAW_BG` |

Full tables: [`docs/CODE_MAP.md`](docs/CODE_MAP.md)

## Documentation

| Doc | Contents |
|-----|----------|
| [CODE_MAP.md](docs/CODE_MAP.md) | Line / label / point → code mapping |
| [GEOMETRY.md](docs/GEOMETRY.md) | Figure topology and coordinates |
| [RENDER.md](docs/RENDER.md) | Render, preview, blank-slide fixes |
| [CREATION_NOTES.md](docs/CREATION_NOTES.md) | How this was built and approved choices |
| [SEGMENT_LENGTHS.md](docs/SEGMENT_LENGTHS.md) | 9-step DE/EA/CB/BF highlight + k labels + teardown |
| [PARALLEL_ANGLES.md](docs/PARALLEL_ANGLES.md) | // marks + angle pairs + shaded regions |
| [AREA_COMPARISON.md](docs/AREA_COMPARISON.md) | △EAG / △GBF outline → colour → rotate compare |
| [TRIANGLE_REGIONS.md](docs/TRIANGLE_REGIONS.md) | △GBF + △GCB region highlights (from angle-marks end) |
| [PARALLEL_DE_BF.md](docs/PARALLEL_DE_BF.md) | // marks on DE & BF + 5k labels (from angle-marks end) |
| [CGB_ANGLE_MARKS.md](docs/CGB_ANGLE_MARKS.md) | ∠marks deck — full step/code map |
| [CHB_LIFT.md](docs/CHB_LIFT.md) | △CHB duplicate lift from CgbAngleMarks end |
| [CHB_REGIONS.md](docs/CHB_REGIONS.md) | CB/BF k labels + △GCB/△GBF/△HCB fills from ChbLift end |
| [CHB_REGIONS_CONT.md](docs/CHB_REGIONS_CONT.md) | ChbRegions end → merge HCB, red △HBG |
| [CHB_HBG_RESTORE.md](docs/CHB_HBG_RESTORE.md) | Restore F/GF/BF on original graph, keep △HBG |
| [CHB_HBG_MARKS.md](docs/CHB_HBG_MARKS.md) | Revised // marks + △CDH + three angle pairs |
| [CHB_HBG_K_REGIONS.md](docs/CHB_HBG_K_REGIONS.md) | △EAG/△GBF fills + k segment labels |
| [CHB_HBG_K_TRIM.md](docs/CHB_HBG_K_TRIM.md) | Trim EAG/GBF ink + △CDH area + CDH-only cleanup |
| [EAG_GBF_ANGLES.md](docs/EAG_GBF_ANGLES.md) | Isolated △EAG/△GBF + // marks + 3 angle pairs |
| [CHB_DECK_CHAIN.md](docs/CHB_DECK_CHAIN.md) | **Agent index:** full CHB chain, helpers, final frame |
