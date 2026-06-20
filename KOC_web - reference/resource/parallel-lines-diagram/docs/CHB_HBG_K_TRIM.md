# Trim △EAG / △GBF + EA / BF ink + △CDH area + cleanup (4 steps)

Scene: `ParallelLinesChbHbgKTrimDraw` in `manim/diagram.py`

Deck: `slides/chb-hbg-k-trim/index.html`

Continues from the **end of** `ParallelLinesChbHbgKRegionsDraw` (step 4). Step 0 via `_chb_hbg_k_regions_end_frame()`.

## Step summary

| Step | Animation | On screen after beat |
|------|-----------|----------------------|
| 0 | `Wait(0.01)` | ChbHbgKRegions step-4 end |
| 1 | `FadeOut` × 6 | Remove △**EAG**, **EA**/**2k**, **BF**/**5k**, △**GBF** |
| 2 | `FadeIn` | **343 cm²** inside teal △**CDH** |
| 3 | `FadeOut` × N | CDH-only frame (**D**, **H**, **C**, △**CDH**, **343 cm²**) |

## Step 1 — removed

| Mobject | What |
|---------|------|
| `tri_eag` | Pink △**EAG** fill |
| `hi_ea`, `lbl_2k_ea` | Green **EA** + **2k** above |
| `hi_bf`, `lbl_5k_bf` | Yellow **BF** + **5k** below |
| `tri_gbf` | Green △**GBF** fill |

## Kept after step 1

| Mobject | What |
|---------|------|
| `hi_ag`, `lbl_2k_ag` | Green **AG** + **2k** right |
| `hi_bg`, `lbl_5k_bg` | Yellow **BG** + **5k** right |
| `hi_dc`, `lbl_7k_dc` | Blue **DC** + **7k** left |
| (prior deck) | Teal △**CDH**, angle pairs, red △**HBG** + **175 cm²**, // marks |

## Step 2 — △CDH area

| Mobject | What |
|---------|------|
| `area_cdh` | **343 cm²** centred inside △**CDH** (`tri_cdh`) |

## Step 3 — CDH-only cleanup

**Kept:** **D**, **H**, **C**; teal △**CDH**; **343 cm²**; white **DC**, **DH**, **HC**.

**Removed:** other diagram lines; labels **E**, **A**, **B**, **F**, **G**; red △**HBG** + **175 cm²**; **AG**/**BG**/**DC** k ink; // marks; all six angle arcs.

| Helper | Purpose |
|--------|---------|
| `_trim_cdh_triangle_ink` | Trim **DB**→**DH**, **CG**→**HC**; keep **DC** |
| `_chb_hbg_k_final_cleanup_mobs` | List of mobjects to `FadeOut` |

## Helpers

| Function | Purpose |
|----------|---------|
| `_chb_hbg_k_regions_end_frame` | Static ChbHbgKRegions step-4 end |
| `_chb_hbg_k_trim_end_frame` | Static step-2 end (△CDH + **343 cm²**) |
| `_chb_hbg_k_cdh_only_end_frame` | Static step-3 end (CDH-only final frame) |

**Chain index:** [CHB_DECK_CHAIN.md](CHB_DECK_CHAIN.md)

**Terminal deck** — next continuation should use `_chb_hbg_k_cdh_only_end_frame()` as step 0.

## Render

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesChbHbgKTrimDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/chb-hbg-k-trim `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/chb-hbg-k-trim/index.html`
