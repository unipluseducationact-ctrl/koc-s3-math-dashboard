# Revised // marks + △CDH + angle pairs (7 steps)

Scene: `ParallelLinesChbHbgMarksDraw` in `manim/diagram.py`

Deck: `slides/chb-hbg-marks/index.html`

Continues from the **end of** `ParallelLinesChbHbgRestoreDraw` (step 3). Step 0 via `_chb_hbg_restore_end_frame()`.

## Step summary

| Step | Animation | On screen after beat |
|------|-----------|----------------------|
| 0 | `Wait(0.01)` | HbgRestore step-3 end |
| 1 | `FadeOut` × 5 | Remove // on **BF**, **EF**, **DB**; blue **CB**/**7k** |
| 2 | `Create` × 2 | matched double // **CD** and **AB** |
| 3 | `FadeIn` | Teal △**CDH** |
| 4 | `Create` × 2 | Gold ∠**CDB**, ∠**GBH** |
| 5 | `Create` × 2 | Pink ∠**DCH**, ∠**HGB** |
| 6 | `Create` × 2 | Maroon ∠**DHC**, ∠**GHB** |

**Throughout:** red △**HBG**, **175 cm²**, // on **DE** stay on screen.

## Step 1 — arrow removal

| Removed | Segment |
|---------|---------|
| `arr_bf` | **BF** |
| `arr_ef` | **EF** (parallel pair with **DB**; user “**GF**” = G–F slant on **EF**) |
| `arr_db` | **DB** |

## Step 2 — new parallel marks

| Mark | Segment | Style |
|------|---------|-------|
| `arr_cd` | **CD** | double // (tips toward **D**) |
| `arr_ab` | **AB** | matched double // (tips toward **A**; no // on **GB**) |

## Step 3 — △CDH fill

Teal (`COL_TRI_CDH`) — not used elsewhere on this figure.

## Steps 4–6 — angle pairs

| Pair | Arcs | Colour |
|------|------|--------|
| 1 | ∠**CDB** at **D**, ∠**GBH** at **B** | Gold |
| 2 | ∠**DCH** at **C**, ∠**HGB** at **G** | Pink |
| 3 | ∠**DHC** at **H**, ∠**GHB** at **H** | Maroon |

## Helpers

| Function | Purpose |
|----------|---------|
| `_chb_hbg_restore_end_frame` | Static HbgRestore step-3 end |
| `_double_parallel_arrow_mark_matched_pair` | Matched double // on parallel segments |
| `_build_chb_hbg_marks_arrow_marks` | **CD** / **AB** // marks |
| `_build_chb_hbg_marks_angle_arcs` | Six interior arcs in three pairs |

## Render

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesChbHbgMarksDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/chb-hbg-marks `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/chb-hbg-marks/index.html`

**Next deck:** [`CHB_HBG_K_REGIONS.md`](CHB_HBG_K_REGIONS.md) — `ParallelLinesChbHbgKRegionsDraw`
