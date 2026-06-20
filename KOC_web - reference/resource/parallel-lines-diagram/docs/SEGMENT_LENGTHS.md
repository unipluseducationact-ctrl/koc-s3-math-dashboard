# Segment lengths animation — 9 steps

Scene: `ParallelLinesSegmentLengthsDraw` in `manim/diagram.py`

Build-only variant (steps 1–8, no teardown): `ParallelLinesSegmentLengthsBuildDraw` → `slides/segment-lengths-build/`

Base frame: full diagram (white ink on black). Each step adds one highlight or one label.

| Step | Animation | Segment | Line colour | Label | Label colour |
|------|-----------|---------|-------------|-------|--------------|
| 1 | `Create(hi_de)` | **DE** | yellow | — | — |
| 2 | `FadeIn(lbl_de)` | **DE** | yellow | `5k` above | yellow |
| 3 | `Create(hi_ea)` | **EA** | green | — | — |
| 4 | `FadeIn(lbl_ea)` | **EA** | green | `2k` above | green |
| 5 | `Create(hi_cb)` | **CB** | blue | — | — |
| 6 | `FadeIn(lbl_cb)` | **CB** | blue | `7k` below | blue |
| 7 | `Create(hi_bf)` | **BF** | yellow | — | — |
| 8 | `FadeIn(lbl_bf)` | **BF** | yellow | `5k` below | yellow |
| 9 | `FadeOut` × 23 (one mob each) | all | — | — | black screen |

Step 9 removes in reverse order: k labels → coloured highlights → lines (EF…DA) → point labels (H…D). Each `FadeOut` targets a single mobject — not a `VGroup`.

## Helpers

| Function | Creates |
|----------|---------|
| `_laid_out_subsegment(top_da, D, E, D, A)` | endpoints on scaled white ink |
| `_highlight_seg(p1, p2, COL_DE)` | thick coloured `Line` on those endpoints |
| `_length_label(r"5k", p1, p2, UP)` | `MathTex` at midpoint of laid-out segment |
| `_add_base_diagram(self)` | full figure before step 1 |

Highlights use `_laid_out_subsegment` so coloured strokes **overlap** the white
lines (base diagram is scale-to-fit; raw `D`/`E`/… constants alone would float off).

## Render

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesSegmentLengthsDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/segment-lengths `
  -Quality ql `
  -MediaDir media/adhoc
```
