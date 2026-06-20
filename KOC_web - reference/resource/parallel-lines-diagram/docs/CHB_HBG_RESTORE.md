# Restore graph — from ChbRegionsCont end (4 steps)

Scene: `ParallelLinesChbHbgRestoreDraw` in `manim/diagram.py`

Deck: `slides/chb-hbg-restore/index.html`

Continues from the **end of** `ParallelLinesChbRegionsContDraw` (step 5). Step 0 via `_chb_regions_cont_end_frame()`.

## Step summary

| Step | Animation | On screen after beat |
|------|-----------|----------------------|
| 0 | `Wait(0.01)` | ChbRegionsCont step-5 end |
| 1 | `FadeOut` × 8 | All ∠**GCB** arcs removed |
| 2 | restore + cleanup | Full graph ink + **D,E,A,F,H**; duplicate △**HCB** ink removed |
| 3 | `Create` × 4 | // **DE**/**BF**; double // **DB**/**EF** |

**Throughout:** red △**HBG**, **175 cm²**, blue **CB**/**7k** stay on screen.

## Step 2 — full graph restored

| Part | Restored |
|------|----------|
| Labels | **D**, **E**, **A**, **F**, **H** |
| Lines | **DC**, **DA**, **AB**, **DB**, **EF**, **CG**, **CF** (full endpoints) |
| Removed | `chb_dup` white **CH/HB/CB** + duplicate **C,H,B** labels (edges now on full lines) |

**Kept:** **C**, **G**, **B** labels; **CB**/**7k** highlight; red △**HBG** + **175 cm²**.

## Step 3 — parallel marks

| Mark | Segments |
|------|----------|
| Single // | **DE**, **BF** |
| Double // | **DB**, **EF** |

No yellow **5k** or orange ▱**DEBF** (those belong to `ParallelLinesDeBfParallelDraw`).

## Helpers

| Function | Purpose |
|----------|---------|
| `_chb_regions_cont_end_frame` | Static Cont step-5 end |
| `_restore_full_parallel_graph_ink` | Full figure ink + labels |
| `_build_parallel_graph_arrow_marks` | // arrows only |

## Render

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesChbHbgRestoreDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/chb-hbg-restore `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/chb-hbg-restore/index.html`

**Next deck:** [`CHB_HBG_MARKS.md`](CHB_HBG_MARKS.md) — `ParallelLinesChbHbgMarksDraw`
