# CGB angle pairs — from DeBf end frame (8 steps)

Scene: `ParallelLinesCgbAngleMarksDraw` in `manim/diagram.py`

Deck: `slides/cgb-angle-marks/index.html`

Continues from the **end of** `ParallelLinesDeBfParallelDraw` (step 7). Step 0 uses `_de_bf_parallel_end_frame()`.

## Step summary

| Step | Animation | On screen after beat |
|------|-----------|----------------------|
| 0 | `Wait(0.01)` | DeBf step-7 end (orange ▱, // marks, yellow 5k, full ink) |
| 1 | `FadeOut(quad_debf)` | Orange ▱ gone |
| 2 | `FadeOut(arr_db)` + `Create(arr_hb)` | // on **HB** (tips → **H**) |
| 3 | `FadeOut` × 4 | Yellow **DE**/**BF** + **5k** gone |
| 4 | `FadeIn` purple × 2 | ∠**CGF** + ∠**CHB** |
| 5 | `FadeIn` blue × 2 | ∠**CFG** + ∠**CBH** |
| 6 | `FadeIn` green × 1 | ∠**GCB** |
| 7 | trim + `FadeOut` | **C,H,G,B,F** + arcs + **CH/HG,GB,HB,CB,BF,GF** |

Arc radius: `CGB_ANGLE_RADIUS` (0.44).

---

## Code map — animation → line (diagram.py)

> Line numbers drift when editing; search for `# ── STEP n` in `ParallelLinesCgbAngleMarksDraw.construct`.

### Step 0 — static DeBf end frame

| What | Code |
|------|------|
| Base diagram | `_add_base_diagram(self)` |
| DeBf decorations | `_de_bf_parallel_end_frame(self, lines, labels)` |
| First slide beat | `self.play(Wait(0.01), …)` → `self.next_slide()` |

### Step 1 — remove orange ▱DEBF

| Animation | Mobject | Code |
|-----------|---------|------|
| `FadeOut` | `quad_debf` | `self.play(FadeOut(quad_debf), run_time=0.5)` |

### Step 2 — // arrows DB → HB

| Animation | Mobject | Code |
|-----------|---------|------|
| `FadeOut` | `arr_db` | `self.play(FadeOut(arr_db), Create(arr_hb), …)` |
| `Create` | `arr_hb` | `_double_parallel_arrow_mark(h_pt, v["B"])` |

### Step 3 — remove yellow highlights + 5k

| # | Animation | Mobject |
|---|-----------|---------|
| 1 | `FadeOut` | `hi_de` |
| 2 | `FadeOut` | `lbl_de` |
| 3 | `FadeOut` | `hi_bf` |
| 4 | `FadeOut` | `lbl_bf` |

Each: `self.play(FadeOut(…), run_time=rt)` with `rt = 0.28`.

### Step 4 — purple ∠CGF + ∠CHB

| Animation | Mobject | Helper |
|-----------|---------|--------|
| `FadeIn` × 2 | `ang_cgf` (wedge + arc) | `_build_cgb_angle_arcs` → `"cgf"` |
| `FadeIn` × 2 | `ang_chb` (wedge + arc) | `_build_cgb_angle_arcs` → `"chb"` |

### Step 5 — blue ∠CFG + ∠CBH

| Animation | Mobject | Helper key |
|-----------|---------|------------|
| `FadeIn` × 2 | `ang_cfg` | `"cfg"` |
| `FadeIn` × 2 | `ang_cbh` | `"cbh"` |

### Step 6 — green ∠GCB

| Animation | Mobject | Helper key |
|-----------|---------|------------|
| `FadeIn` × 2 | `ang_gcb` | `"gcb"` |

### Step 7 — ink trim + fade extras

**Silent trims** (before animations; `put_start_and_end_on`):

| Trim | Line key | Effect |
|------|----------|--------|
| `diag_DB` | `lines["diag_DB"]` | **D–H** dropped → **HB** only |
| `seg_EF` | `lines["seg_EF"]` | **E–G** dropped → **GF** only |
| `right_AB` | `lines["right_AB"]` | **A–G** dropped → **GB** only |

**Animated `FadeOut`s** (one mob each):

| # | Mobject |
|---|---------|
| 1–4 | `arr_de`, `arr_bf`, `arr_hb`, `arr_ef` |
| 5–7 | `labels["D"]`, `labels["E"]`, `labels["A"]` |
| 8–9 | `lines["top_DA"]`, `lines["left_DC"]` |

---

## Angle definitions

| Angle | Vertex | Rays | Colour | Step |
|-------|--------|------|--------|------|
| ∠CGF | **G** | GC, GF | purple | 4 |
| ∠CHB | **H** | HC, HB | purple | 4 |
| ∠CFG | **F** | FC, FG | blue | 5 |
| ∠CBH | **B** | BC, BH | blue | 5 |
| ∠GCB | **C** | CG, CB | green | 6 |

## Helpers

| Function | Purpose |
|----------|---------|
| `_build_cgb_angle_arcs(v, h_pt, ang_r)` | All five angle VGroups |
| `_cgb_angle_marks_end_frame(scene, lines, labels)` | Static step-7 end (used by `ParallelLinesChbLiftDraw`) |

## Render

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesCgbAngleMarksDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/cgb-angle-marks `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/cgb-angle-marks/index.html`

**Next deck:** [`CHB_LIFT.md`](CHB_LIFT.md) — `ParallelLinesChbLiftDraw`
