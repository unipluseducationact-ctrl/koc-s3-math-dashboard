# Triangle regions — △GBF & △GCB (7 steps)

Scene: `ParallelLinesTriangleRegionsDraw` in `manim/diagram.py`

Deck: `slides/triangle-regions/index.html`

Continues from the **end of** `ParallelLinesAngleMarksDraw` (step 7).

## Steps

| Step | Animation | What on screen |
|------|-----------|----------------|
| 0 | (static) | Base diagram — all lines + labels |
| 1 | `FadeIn` △GBF, △GCB | Green △**GBF** + blue △**GCB** |
| 2 | `Create` dash + altitudes | △GCB: dashed horiz. through **G** + blue height **B** ⟂; △GBF: green height **G** ⟂ **BF** |
| 3 | `FadeOut` labels + lines (one-by-one) | Keep △fills, heights, dash, labels **G, C, B, F** only |
| 4 | `FadeOut` altitude dash → `shift` → `FadeIn` duplicate **G/B** → `Create` height dash | △GCB left of △GBF; duplicate **G/B** match originals; dashed line joins tops of blue + green altitudes |
| 5 | `Create(hi_cb)` → `FadeIn(lbl_7k)` → `Create(hi_bf)` → `FadeIn(lbl_5k)` | blue **CB** + **7k** below (△GCB); yellow **BF** + **5k** below (△GBF) |
| 6 | `FadeOut` dash + altitudes → `FadeIn` area labels | **300 cm²** in △GBF; **420 cm²** same size + **y**, left inside △GCB (`AREA_GCB_AREA_X_FRAC` on horizontal span) |

## Step 3 — removed (one `FadeOut` each)

| # | Target | User segment / note |
|---|--------|---------------------|
| 1–4 | `labels[D,E,A,H]` | point labels |
| 5 | `left_DC` | **DC** |
| 6 | `diag_DB` | **HD** (H → D) |
| 7 | `top_DA` | **EA** (E → A) + **DG** (D → E) |
| 8 | `right_AB` | **GA** (G → A) |
| 9–11 | `seg_CG`, `bottom_CF`, `seg_EF` | remaining white ink |

## Step 4 — side-by-side compare

- `gcb_unit` = △GCB + blue altitude + label **C** + duplicate **G, B** (no dash in unit)
- `labels["G"]`, `labels["B"]`, `labels["F"]` stay with △GBF (anchor)
- `_comparison_shift_grounded(tri_gcb, tri_gbf, gap=GCB_COMPARE_GAP)` — same bottom **y**, △GCB left of △GBF
- Duplicate **G/B**: `_label_like_orig` — `match_height` scaled originals + same centre offset from vertex
- Labels placed **after** shift (not in `gcb_body`) so **B** stays level with original **B**
- After shift: `_dash_between_heights(ht_gcb, ht_gbf)` — horizontal dash from top of blue altitude to top of green altitude (small extension each end)

## Helpers

| Function | Role |
|----------|------|
| `_gcb_altitude_dash(tri, buff)` | horizontal dashed reference for △GCB height |
| `_comparison_shift_grounded` | grounded left-of shift |
| `_label_at_vertex` | outward duplicate **G/B** on △GCB |

## Render

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesTriangleRegionsDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/triangle-regions `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/triangle-regions/index.html`
