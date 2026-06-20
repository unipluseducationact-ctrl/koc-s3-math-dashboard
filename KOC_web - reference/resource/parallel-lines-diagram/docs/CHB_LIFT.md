# △CHB lift — from CgbAngleMarks end (3 steps)

Scene: `ParallelLinesChbLiftDraw` in `manim/diagram.py`

Deck: `slides/chb-lift/index.html`

Continues from the **end of** `ParallelLinesCgbAngleMarksDraw` (step 7). Step 0 via `_cgb_angle_marks_end_frame()`.

## Steps

| Step | Animation | On screen |
|------|-----------|-----------|
| 0 | (static) | CgbAngleMarks step-7 end |
| 1 | `shift` △CHB copy `UP` | Duplicate **CHB** + **C,H,B** + arcs **GCB,CHB,CBH** lifted |
| 2 | `FadeOut` × 6 | Original: remove **HB**, **H**, ∠**CHB**, ∠**CBH** (label **B** stays) |

Lift distance: `_chb_lift_amount(chb_dup, v, h_pt)` — clears max(**G**, **H**) + `CHB_LIFT_CLEAR` + `CHB_LIFT_EXTRA`, capped to frame top (floor `CHB_LIFT_GAP` = 3.60).

## Duplicate △CHB contents (`_chb_triangle_copy`)

| Part | Source |
|------|--------|
| **CH** | `Line(C, H)` — exact vertices only |
| **HB** | `Line(H, B)` |
| **CB** | `Line(C, B)` — exact vertices only |
| Labels | `_label_like_orig` for **C**, **H**, **B** |
| Arcs | fresh `∠GCB`, `∠CHB`, `∠CBH` at duplicate vertices |

Original **CH** / **CB** ink is **not** trimmed before lift (avoids disconnecting **C** from **CG**).

## Step 2 — removed from original only

| # | Target |
|---|--------|
| 1 | `lines["diag_DB"]` (**HB**) |
| 2 | `labels["H"]` |
| 3–4 | `ang_chb` (wedge + arc) |
| 5–6 | `ang_cbh` (wedge + arc) |

**Kept on original:** labels **B**, **C**, ∠**GCB**, **G**, **F**, **CG**, **GB**, **GF**, **CB/BF**, lifted △CHB copy (duplicate **B** on lifted copy).

## Code map — animation → line

Search `# ── STEP` in `ParallelLinesChbLiftDraw.construct`.

| Step | Animation | Code |
|------|-----------|------|
| 0 | `Wait(0.01)` | `_add_base_diagram` + `_cgb_angle_marks_end_frame` |
| 1 | `chb_dup.animate.shift(UP * lift)` | `_chb_triangle_copy(…)` + `_chb_lift_amount(chb_dup, v, h_pt)` |
| 2 | `FadeOut(diag_DB)` | `self.play(FadeOut(lines["diag_DB"]), …)` |
| 2 | `FadeOut` label | `labels["H"]` only (duplicate **B** rides with `chb_dup`) |
| 2 | `FadeOut` arcs | each mob in `ang_chb`, `ang_cbh` |

## Render

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesChbLiftDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/chb-lift `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/chb-lift/index.html`

**Next deck:** [`CHB_REGIONS.md`](CHB_REGIONS.md) — `ParallelLinesChbRegionsDraw`
