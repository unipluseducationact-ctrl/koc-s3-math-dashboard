# Creation notes

Ad hoc diagram built from a user-provided exam-style photo (parallel lines + ▱ABCD + intersections G, H).

## Workflow

1. User supplied topology and anchor coordinate framework.
2. **G** and **H** computed from line intersections — no invented geometry.
3. Iterative label tuning (**H** final offset: `UP + LEFT * (-0.03)`).
4. Slide beats collapsed to **one beat** (all lines, then all labels).
5. Draw scene uses **black BG / white ink** so Reveal.js background video is visible.
6. Fixed blank `index.html` caused by UTF-8 BOM from PowerShell `Set-Content`.

## Approved settings (keep)

- Anchor coords: see `docs/GEOMETRY.md`
- Single-slide draw animation
- `LINE_ORDER` includes `seg_CG` early so G connection is complete
- `render_slides.ps1` post-process: asset sync, `autoPlayMedia`, no-BOM write

## Animation decks

| Deck | Scene | Steps |
|------|-------|-------|
| Base draw | `ParallelLinesDraw` | 1 |
| Segment lengths | `ParallelLinesSegmentLengthsDraw` | 9 (8 k-label beats + 1 teardown) |
| Angle marks | `ParallelLinesAngleMarksDraw` | 7 (marks, angle fills, △EAG/△GBF, teardowns) |
| Area compare | `ParallelLinesAreaCompareDraw` | 9 (compare → relabel → k/area → teardown) |
| Triangle regions | `ParallelLinesTriangleRegionsDraw` | 7 (… → k labels → 300/420 cm²) |
| DE ∥ BF parallel | `ParallelLinesDeBfParallelDraw` | 8 (… → ▱DEBF → cleanup → ∥ DB/EF → restore) |
| CGB angle marks | `ParallelLinesCgbAngleMarksDraw` | 8 (DeBf end → ∠marks → CH/HB/HG/BF/GF trim) |
| CHB lift | `ParallelLinesChbLiftDraw` | 3 (Cgb end → △CHB lift → trim original) |
| CHB regions | `ParallelLinesChbRegionsDraw` | 4 (ChbLift end → CB/7k, BF/5k, △fills + 245 cm²) |
| CHB regions cont | `ParallelLinesChbRegionsContDraw` | 6 (cleanup → lower HCB → red △HBG 175 cm²) |
| CHB HBG restore | `ParallelLinesChbHbgRestoreDraw` | 4 (Cont end → full graph + // marks + △HBG) |
| CHB HBG marks | `ParallelLinesChbHbgMarksDraw` | 7 (HbgRestore end → revised // + △CDH + angle pairs) |
| CHB HBG k regions | `ParallelLinesChbHbgKRegionsDraw` | 5 (ChbHbgMarks end → △EAG/△GBF + k labels) |
| CHB HBG k trim | `ParallelLinesChbHbgKTrimDraw` | 4 (KRegions end → trim ink + △CDH + CDH-only frame) |

**CHB chain agent map:** [CHB_DECK_CHAIN.md](CHB_DECK_CHAIN.md) — deck order, end-frame helpers, final slide contents.

Segment highlights use `_laid_out_subsegment` so coloured ink sits on scaled white lines.
Angle arcs use `_laid_out_vertices` + `manim_styles.interior_angle_arc`.

## Not in training registry

This package is self-contained under `adhoc/parallel-lines-diagram/` and is **not** registered in `data/training-registry.json`.
