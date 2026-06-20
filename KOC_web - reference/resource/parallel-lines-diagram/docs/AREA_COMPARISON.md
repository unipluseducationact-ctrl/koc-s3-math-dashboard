# Area comparison — △EAG vs △GBF (9 steps)

Scene: `ParallelLinesAreaCompareDraw` in `manim/diagram.py`

Deck: `slides/area-comparison/index.html`

## Build steps (1–8)

| Step | Animation | What on screen |
|------|-----------|----------------|
| 1 | `Create` triangles + `FadeIn` E/A/G labels | Base diagram + outlines △**EAG**, △**GBF**; **E**, **A**, **G** track △EAG |
| 2 | `set_fill` | △EAG **red**, △GBF **green** |
| 3 | `Rotate(eag_unit, PI)` then `shift` | △EAG rotates 180°; same ground as △GBF, left of it |
| 4 | `FadeOut` diagram ink (one-by-one) | Only the two coloured triangles remain |
| 5 | `FadeIn` vertex labels | △EAG: **G**, **A**, **E** — △GBF: **G**, **B**, **F** |
| 6 | `Create(hi_bf)` → `FadeIn(lbl_5k_bf)` | yellow **BF** + **5k** below |
| 7 | `Create(hi_ea)` → `FadeIn(lbl_2k_ea)` | green **EA** + **2k** below |
| 8 | `FadeIn(area_eag)`, `FadeIn(area_gbf)` | **48 cm²** in △EAG; **300 cm²** in △GBF |

### Area label offsets

| Constant | Effect |
|----------|--------|
| `AREA_EAG_VERT_SHIFT` | nudge 48 cm² down inside red △ |
| `AREA_LABEL_H_SHIFT` | nudge 48 cm² left inside red △ |
| `AREA_GBF_H_SHIFT` | nudge 300 cm² left inside green △ |
| `AREA_LABEL_FILL` | scale area text to triangle inradius |

## Step 4 — diagram teardown (one `FadeOut` each)

| # | Target | Removed |
|---|--------|---------|
| 1–7 | `lines[…]` | EF, DB, CG, AB, DC, bottom_CF, top_DA |
| 8–12 | `labels[D,C,B,F,H]` + `lbl_e/a/g` | diagram point labels |

## Step 9 — final teardown (one `FadeOut` each)

One slide beat. Reverse order of steps 5–8 additions, then triangles.

| # | `FadeOut` target | What disappears |
|---|------------------|-----------------|
| 1 | `area_gbf` | **300 cm²** area label (△GBF) |
| 2 | `area_eag` | **48 cm²** area label (△EAG) |
| 3 | `lbl_2k_ea` | green **2k** label (below EA) |
| 4 | `hi_ea` | green highlight on **EA** |
| 5 | `lbl_5k_bf` | yellow **5k** label (below BF) |
| 6 | `hi_bf` | yellow highlight on **BF** |
| 7 | `lbl_f_fin` | point label **F** (△GBF) |
| 8 | `lbl_b_fin` | point label **B** (△GBF) |
| 9 | `lbl_g_gbf` | point label **G** (△GBF) |
| 10 | `lbl_e_fin` | point label **E** (△EAG) |
| 11 | `lbl_a_fin` | point label **A** (△EAG) |
| 12 | `lbl_g_eag` | point label **G** (△EAG) |
| 13 | `tri_gbf` | green filled △**GBF** |
| 14 | `tri_eag` | red filled △**EAG** |

After step 9 the frame is black (blank).

## Layout notes

**Step 3** — `_comparison_shift_grounded(tri_eag, tri_gbf, gap=COMPARE_GAP)`:

1. Align bottom y of △EAG with △GBF
2. Place △EAG to the left of △GBF (`COMPARE_GAP = 1.15`)

**Step 5** — `_label_at_vertex` at post-rotate polygon vertices.

| Triangle | Labels | Polygon vertex order |
|----------|--------|----------------------|
| △EAG (red) | G, A, E | `[2]`, `[1]`, `[0]` |
| △GBF (green) | G, B, F | `[0]`, `[1]`, `[2]` |

## Helpers

| Function | Role |
|----------|------|
| `_triangle_outline` | unfilled triangle on ink |
| `_comparison_shift_grounded` | grounded left-of shift vector |
| `_label_at_vertex` | outward vertex label |
| `_area_label_in_triangle` | scaled area MathTex inside triangle |
| `_highlight_seg` / `_length_label` | k-length marks (steps 6–7) |

## Render

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesAreaCompareDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/area-comparison `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/area-comparison/index.html`
