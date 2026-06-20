# △EAG / △GBF + k labels (5 steps)

Scene: `ParallelLinesChbHbgKRegionsDraw` in `manim/diagram.py`

Deck: `slides/chb-hbg-k-regions/index.html`

Continues from the **end of** `ParallelLinesChbHbgMarksDraw` (step 6). Step 0 via `_chb_hbg_marks_end_frame()`.

## Step summary

| Step | Animation | On screen after beat |
|------|-----------|----------------------|
| 0 | `Wait(0.01)` | ChbHbgMarks step-6 end |
| 1 | `FadeIn` × 2 | Pink △**EAG**, green △**GBF** |
| 2 | `Create` + `FadeIn` × 4 | Green **EA**/**AG** + **2k** (above / right) |
| 3 | `Create` + `FadeIn` × 4 | Yellow **BF**/**BG** + **5k** (below / right) |
| 4 | `Create` + `FadeIn` × 2 | Blue **DC** + **7k** (left) |

**Throughout:** teal △**CDH**, angle pairs, red △**HBG** + **175 cm²**, // marks stay on screen.

## Colours (same as earlier decks)

| Region / segment | Colour | Label |
|------------------|--------|-------|
| △**EAG** | Pink | — |
| △**GBF** | Green | — |
| **EA**, **AG** | Green | **2k** |
| **BF**, **BG** | Yellow | **5k** |
| **DC** | Blue | **7k** (left) |

## Helpers

| Function | Purpose |
|----------|---------|
| `_chb_hbg_marks_end_frame` | Static ChbHbgMarks step-6 end |
| `_build_chb_hbg_k_region_mobs` | Triangle fills + segment highlights + k labels |

## Render

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesChbHbgKRegionsDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/chb-hbg-k-regions `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/chb-hbg-k-regions/index.html`

**Next deck:** [`CHB_HBG_K_TRIM.md`](CHB_HBG_K_TRIM.md) — `ParallelLinesChbHbgKTrimDraw`
