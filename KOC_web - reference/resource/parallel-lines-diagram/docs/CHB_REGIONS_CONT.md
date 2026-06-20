# ChbRegions continuation — merge HCB + △HBG (6 steps)

Scene: `ParallelLinesChbRegionsContDraw` in `manim/diagram.py`

Deck: `slides/chb-regions-cont/index.html`

Continues from the **end of** `ParallelLinesChbRegionsDraw` (step 3). Step 0 via `_chb_regions_end_frame()`.

## Step summary

| Step | Animation | On screen after beat |
|------|-----------|----------------------|
| 0 | `Wait(0.01)` | ChbRegions step-3 end |
| 1 | `FadeOut` × 8 | ∠**CGF**, ∠**CFG**, duplicate ∠**CHB**/**CBH** gone; ∠**GCB** kept |
| 2 | `FadeOut` × 5 + trim **CB** | **F**, **GF**, **BF**/**5k**, green △**GBF** gone; label **G** kept; bottom ink **CB** only |
| 3 | `FadeOut` × 3 | **420**, **300**, **245 cm²** gone |
| 4 | `shift` `DOWN * lift` → `FadeOut` dup **CB**/**7k** | Lifted △**HCB** lowered until **CB** segments coincide |
| 5 | `FadeOut` blue/orange → `FadeIn` red + area | Red △**HBG** + **175 cm²** |

---

## Code map — animation → line

> Search `# ── STEP` in `ParallelLinesChbRegionsContDraw.construct`.

### Step 0 — static ChbRegions end

| What | Code |
|------|------|
| Full end state | `_chb_regions_end_frame(self, lines, labels)` |

### Step 1 — remove ∠**CGF**, ∠**CFG**, duplicate ∠**CHB**/**CBH** (keep ∠**GCB**)

| Animation | Mobject |
|-----------|---------|
| `FadeOut` each | `ang_cgf` — purple ∠**CGF** at **G** |
| `FadeOut` each | `ang_cfg` — blue ∠**CFG** at **F** |
| `FadeOut` each | `_chb_dup_angle_mobs(chb_dup, include_gcb=False)` — ∠**CHB**, ∠**CBH** on lifted copy |
| **Kept** | `ang_gcb` + duplicate ∠**GCB** at **C** |

### Step 2 — remove **F**, **GF**, **BF**, green △**GBF** (keep label **G**)

| # | Animation | Mobject |
|---|-----------|---------|
| 1 | `FadeOut` | `labels["F"]` |
| 2 | `FadeOut` | `lines["seg_EF"]` (**GF**) |
| 3 | `FadeOut` | `hi_bf`, `lbl_5k_bf` |
| 4 | trim (no anim) | `bottom_CF` → **C**→**B** only |
| 5 | `FadeOut` | `tri_gbf` |
| **Kept** | — | `labels["G"]` |

### Step 3 — remove area labels

| # | Animation | Mobject |
|---|-----------|---------|
| 1 | `FadeOut` | `area_gcb` (**420 cm²**) |
| 2 | `FadeOut` | `area_gbf` (**300 cm²**) |
| 3 | `FadeOut` | `area_hcb` (**245 cm²**) |

### Step 4 — lower lifted △**HCB**

| Animation | Mobjects |
|-----------|----------|
| `shift` `DOWN * lift` | `chb_dup`, `hi_cb_lift`, `lbl_7k_lift`, `tri_hcb` |
| `FadeOut` | `hi_cb_lift`, `lbl_7k_lift` (overlap lower **CB**/**7k**) |

`lift` from `_chb_lift_end_frame` (same amount used in ChbLift step 1).

### Step 5 — red △**HBG** + **175 cm²**

| # | Animation | Mobject |
|---|-----------|---------|
| 1 | `FadeOut` × 2 + `FadeIn` | `tri_gcb` (blue), `tri_hcb` (orange) → `tri_hbg` (`COL_TRI_HBG` red) |
| 2 | `FadeIn` | `area_hbg` — **175 cm²** inside △**HBG**, `LEFT * AREA_HBG_H_SHIFT + UP * AREA_HBG_V_SHIFT` |

Vertices: **H** = `h_pt`, **B** = `v["B"]`, **G** = `v["G"]`.

## Render

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesChbRegionsContDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/chb-regions-cont `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/chb-regions-cont/index.html`

**Next deck:** [`CHB_HBG_RESTORE.md`](CHB_HBG_RESTORE.md) — `ParallelLinesChbHbgRestoreDraw`
