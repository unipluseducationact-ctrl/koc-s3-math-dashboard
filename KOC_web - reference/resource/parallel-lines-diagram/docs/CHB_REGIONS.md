# △regions + k labels — from ChbLift end (4 steps)

Scene: `ParallelLinesChbRegionsDraw` in `manim/diagram.py`

Deck: `slides/chb-regions/index.html`

Continues from the **end of** `ParallelLinesChbLiftDraw` (step 2). Step 0 via `_chb_lift_end_frame()`.

**Next deck:** [`CHB_REGIONS_CONT.md`](CHB_REGIONS_CONT.md) — `ParallelLinesChbRegionsContDraw`

---

## Step summary

| Step | Animation | On screen after beat |
|------|-----------|----------------------|
| 0 | `Wait(0.01)` | ChbLift step-2 end |
| 1 | `Create` × 2 → `FadeIn` × 2 | Blue **CB** + **7k** on lower **CB** and lifted **CB** |
| 2 | `Create` → `FadeIn` | Yellow **BF** + **5k** below |
| 3 | `FadeIn` × 3 → `FadeIn` × 3 | Blue △**GCB** + **420 cm²**; green △**GBF** + **300 cm²**; orange lifted △**HCB** + **245 cm²** |

---

## Code map — animation → line

> Line numbers drift when editing; search for `# ── STEP n` in `ParallelLinesChbRegionsDraw.construct`.

### Step 0 — static ChbLift end frame

| What | Code |
|------|------|
| Base diagram | `_add_base_diagram(self)` |
| ChbLift decorations | `_chb_lift_end_frame(self, lines, labels)` |
| First slide beat | `self.play(Wait(0.01), …)` → `self.next_slide()` |

**On screen:** white ink **C,G,B,F** + **CG,GB,GF,CB/BF**; lifted duplicate △**HCB** (**C,H,B** + arcs **GCB,CHB,CBH**); original ∠**GCB** at **C**; original **HB**, label **H**, ∠**CHB**, ∠**CBH** removed; label **B** kept on lower figure.

### Step 1 — both **CB** blue + **7k**

Build mobs once: `_build_chb_regions_k_highlights(v, seg_cb_dup)`.

| # | Animation | Mobject | Segment / notes |
|---|-----------|---------|-----------------|
| 1 | `Create` | `hi_cb_low` | `v["C"]` → `v["B"]`, `COL_CB` |
| 2 | `FadeIn` | `lbl_7k_low` | blue **7k** below lower **CB** |
| 3 | `Create` | `hi_cb_lift` | lifted `seg_cb_dup`, `COL_CB` |
| 4 | `FadeIn` | `lbl_7k_lift` | blue **7k** below lifted **CB** |

`run_time`: 0.55 / 0.45 / 0.55 / 0.45

### Step 2 — **BF** yellow + **5k**

Uses same `k_mobs` dict from step 1.

| # | Animation | Mobject | Segment / notes |
|---|-----------|---------|-----------------|
| 1 | `Create` | `hi_bf` | `v["B"]` → `v["F"]`, `COL_BF` |
| 2 | `FadeIn` | `lbl_5k_bf` | yellow **5k** below **BF** |

`run_time`: 0.65 / 0.45

### Step 3 — △fills + area labels

Build: `_build_chb_regions_fills_and_areas(v, h_pt_lift, cb_lift_p1, cb_lift_p2)`.

| # | Animation | Mobject | Content |
|---|-----------|---------|---------|
| 1 | `FadeIn` × 3 | `tri_gcb`, `tri_gbf`, `tri_hcb` | blue **G,C,B**; green **G,B,F**; orange lifted **H,C,B** |
| 2 | `FadeIn` | `area_gbf` | **300 cm²** (`_area_label_in_triangle`) |
| 3 | `FadeIn` | `area_gcb` | **420 cm²** (`_area_label_inside_at_y`) |
| 4 | `FadeIn` | `area_hcb` | **245 cm²** (`_area_label_matched_inside_tri`) |

Fills added with `self.add` + `bring_to_back` before `FadeIn`. `run_time`: 0.8 then 0.45 × 3.

---

## Helpers

| Function | Purpose |
|----------|---------|
| `_build_chb_regions_k_highlights(v, seg_cb_dup)` | Step 1–2 highlights + k labels |
| `_build_chb_regions_fills_and_areas(…)` | Step 3 fills + area labels |
| `_chb_regions_end_frame(scene, lines, labels)` | Static step-3 end (all of the above on screen) |

## Colours

| Element | Constant | Colour |
|---------|----------|--------|
| **CB** highlight + **7k** | `COL_CB` | blue |
| **BF** highlight + **5k** | `COL_BF` | yellow |
| △**GCB** fill | `COL_TRI_GCB` | blue |
| △**GBF** fill | `COL_TRI_GBF` | green |
| △**HCB** fill (lifted) | `COL_TRI_HCB` | orange |
| **245 cm²** placement | `AREA_HCB_X_FRAC`, `AREA_HCB_Y_FRAC` | inside lifted △**HCB** |

## Render

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesChbRegionsDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/chb-regions `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/chb-regions/index.html`
