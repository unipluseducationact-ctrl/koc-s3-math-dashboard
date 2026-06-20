# Parallel DE ∥ BF — ▱DEBF + cleanup + restore (8 steps)

Scene: `ParallelLinesDeBfParallelDraw` in `manim/diagram.py`

Deck: `slides/de-bf-parallel/index.html`

Continues from the **end of** `ParallelLinesAngleMarksDraw` (step 7).

## Steps

| Step | Animation | What on screen |
|------|-----------|----------------|
| 0 | (static) | Base diagram |
| 1 | `Create` // chevrons | **DE** ∥ **BF** |
| 2 | yellow **DE** + **5k** above | |
| 3 | yellow **BF** + **5k** below | |
| 4 | `FadeIn` ▱**DEBF** | Orange fill **D–E–F–B** |
| 5 | `FadeOut` × 10 (one mob each) | Remove HG, EA, AG, DC, HC, BC + labels H, A, G, C |
| 6 | `Create` double // arrows | **DB** (tips → **D**), **EF** (tips → **E**) |
| 7 | `Create`/`FadeIn` restore | Full ink + labels **H, A, G, C** back; orange ▱ + ∥ arrows stay |

## Step 5 — removed segments

| # | Target | Segment / label |
|---|--------|-----------------|
| 1 | `seg_hg` | **HG** (H → G on CG) |
| 2 | `labels["H"]` | **H** |
| 3 | `top_DA` | **EA** (E → A) |
| 4 | `labels["A"]` | **A** |
| 5 | `right_AB` | **AG** (A → G) |
| 6 | `labels["G"]` | **G** |
| 7 | `left_DC` | **DC** |
| 8 | `seg_hc` | **HC** (H → C on CG) |
| 9 | `bottom_CF` | **BC** (B → C) |
| 10 | `labels["C"]` | **C** |

**DE** / **BF** yellow highlights and 5k labels remain. **DB**, **EF** kept for step 6.

## Step 6 — double parallel arrows

`_double_parallel_arrow_mark(tip_at, tail_at)` — two chevrons; tips point toward `tip_at`.

| Line | tip_at | tail_at |
|------|--------|---------|
| **DB** | **D** | **B** |
| **EF** | **E** | **F** |

## Step 7 — restore original graph

Reverse of step 5 (one mob each): bring back **BC**, **C**, **CG**, **DC**, **AG**, **G**, **EA**, **A**, **H**. Orange ▱**DEBF**, DB/EF double // arrows, yellow **DE**/**BF** + 5k, and step-1 chevrons all remain.

## Render

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesDeBfParallelDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/de-bf-parallel `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/de-bf-parallel/index.html`
