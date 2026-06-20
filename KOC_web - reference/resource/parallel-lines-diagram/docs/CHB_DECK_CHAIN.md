# CHB deck chain — agent map

Source: [`manim/diagram.py`](../manim/diagram.py)  
All `ParallelLinesChb*` scenes share black BG (`DRAW_BG`), white ink (`DRAW_INK`).

## Deck order (continue from the previous scene’s last step)

| # | Scene class | Slides | HTML deck | Step-0 helper | Doc |
|---|-------------|--------|-----------|---------------|-----|
| 1 | `ParallelLinesChbLiftDraw` | 3 | `slides/chb-lift/` | `_cgb_angle_marks_end_frame` | [CHB_LIFT.md](CHB_LIFT.md) |
| 2 | `ParallelLinesChbRegionsDraw` | 4 | `slides/chb-regions/` | `_chb_lift_end_frame` | [CHB_REGIONS.md](CHB_REGIONS.md) |
| 3 | `ParallelLinesChbRegionsContDraw` | 6 | `slides/chb-regions-cont/` | `_chb_regions_end_frame` | [CHB_REGIONS_CONT.md](CHB_REGIONS_CONT.md) |
| 4 | `ParallelLinesChbHbgRestoreDraw` | 4 | `slides/chb-hbg-restore/` | `_chb_regions_cont_end_frame` | [CHB_HBG_RESTORE.md](CHB_HBG_RESTORE.md) |
| 5 | `ParallelLinesChbHbgMarksDraw` | 7 | `slides/chb-hbg-marks/` | `_chb_hbg_restore_end_frame` | [CHB_HBG_MARKS.md](CHB_HBG_MARKS.md) |
| 6 | `ParallelLinesChbHbgKRegionsDraw` | 5 | `slides/chb-hbg-k-regions/` | `_chb_hbg_marks_end_frame` | [CHB_HBG_K_REGIONS.md](CHB_HBG_K_REGIONS.md) |
| 7 | `ParallelLinesChbHbgKTrimDraw` | 4 | `slides/chb-hbg-k-trim/` | `_chb_hbg_k_regions_end_frame` | [CHB_HBG_K_TRIM.md](CHB_HBG_K_TRIM.md) |

**Current chain end:** `ParallelLinesChbHbgKTrimDraw` step 3 → `_chb_hbg_k_cdh_only_end_frame()`.

## How to add the next deck

1. Read the **previous** doc + search `# ── STEP` in the previous `ParallelLinesChb*` class.
2. Add or reuse an `_…_end_frame(scene, lines, labels)` that reproduces the prior last slide **without animation**.
3. New class: step 0 = `Wait(0.01)` after that helper; further steps = `construct()` animations.
4. Document in `docs/CHB_*.md`, update this file, `CODE_MAP.md`, `CREATION_NOTES.md`, `RENDER.md`, `README.md`.
5. Render with `scripts/render_slides.ps1` (see [RENDER.md](RENDER.md)).

## End-frame helper chain

```
_cgb_angle_marks_end_frame
  └─ _chb_lift_end_frame
       └─ _chb_regions_end_frame
            └─ _chb_regions_cont_end_frame
                 └─ _chb_hbg_restore_end_frame
                      └─ _chb_hbg_marks_end_frame
                           └─ _chb_hbg_k_regions_end_frame
                                └─ _chb_hbg_k_trim_end_frame
                                     └─ _chb_hbg_k_cdh_only_end_frame  ← final
```

Each helper returns a `dict` merged from its parent (keys include `v`, `h_pt`, mobject refs).

## Builder helpers (by topic)

| Topic | Functions |
|-------|-----------|
| △CHB lift | `_chb_triangle_copy`, `_chb_lift_amount`, `_chb_dup_angle_mobs` |
| k + △fills (regions) | `_build_chb_regions_k_highlights`, `_build_chb_regions_fills_and_areas` |
| △HBG + 175 cm² | `_build_chb_hbg_final_mobs` |
| Full graph restore | `_restore_full_parallel_graph_ink`, `_build_parallel_graph_arrow_marks` |
| Revised // marks | `_double_parallel_arrow_mark_matched_pair`, `_build_chb_hbg_marks_arrow_marks` |
| △CDH + angle pairs | `_build_chb_hbg_marks_angle_arcs` |
| k labels (EAG/GBF deck) | `_build_chb_hbg_k_region_mobs` |
| CDH-only cleanup | `_trim_cdh_triangle_ink`, `_chb_hbg_k_final_cleanup_mobs`, `CDH_KEEP_LINE_KEYS` |

## Colour constants (CHB chain)

| Constant | Use |
|----------|-----|
| `COL_TRI_HCB` | Orange lifted △HCB |
| `COL_TRI_HBG` | Red △HBG |
| `COL_TRI_CDH` | Teal △CDH |
| `COL_TRI_EAG_K` | Pink △EAG (KRegions deck only; `COL_TRI_EAG` = red elsewhere) |
| `COL_TRI_GBF` | Green △GBF |
| `COL_ANGLE_CDB_GBH` | Gold ∠CDB / ∠GBH |
| `COL_ANGLE_DCH_HGB` | Pink ∠DCH / ∠HGB |
| `COL_ANGLE_DHC_GHB` | Maroon ∠DHC / ∠GHB |
| `COL_EA` / `COL_BF` / `COL_DC` | Green / yellow / blue segment highlights |

Area label tuning: `AREA_HBG_*`, `AREA_CDH_H_SHIFT` (343 cm² nudge right).

## Final slide (KTrim step 3) — on screen

| Kept | Keys / ink |
|------|------------|
| Labels | `labels["D"]`, `labels["H"]`, `labels["C"]` |
| Lines | `left_DC` (**DC**), `diag_DB` trimmed **D→H**, `seg_CG` trimmed **C→H** |
| Fill | `tri_cdh` (teal △CDH) |
| Area | `area_cdh` — **343 cm²** |

Everything else from the full figure is removed in step 3 (`_chb_hbg_k_final_cleanup_mobs`).

## Render (full CHB tail)

```powershell
# Example: re-render current chain end
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesChbHbgKTrimDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/chb-hbg-k-trim `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/chb-hbg-k-trim/index.html`
