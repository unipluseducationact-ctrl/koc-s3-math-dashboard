# Isolated △EAG / △GBF + // marks + angle pairs (7 steps)

Scene: `ParallelLinesEagGbfAnglesDraw` in `manim/diagram.py`

Deck: `slides/eag-gbf-angles/index.html`

Companion to the "Prove △AEG ~ △BFG (AAA)" solution step — designed for the
focused **Diagram Analysis** panel while the main panel runs
`ParallelLinesAngleMarksDraw` (// marks on the full figure).

## Steps

| Step | Animation | On screen after beat |
|------|-----------|----------------------|
| 0 | `Wait(0.01)` | Full base diagram (context) |
| 1 | trim + `FadeOut` × 6 | Only △**EAG** + △**GBF** ink; labels **E,A,G,B,F** stay |
| 2 | `Create` × 2 | // chevrons on **EA** and **BF** |
| 3 | `Create`/`FadeIn` × 4 | Green **EA** + **2k** (above); yellow **BF** + **5k** (below) |
| 4 | `FadeIn` × 4 | Green pair ∠**AEG** = ∠**BFG** (alt. ∠s, EA ∥ BF) |
| 5 | `FadeIn` × 4 | Red pair ∠**EAG** = ∠**FBG** (alt. ∠s, EA ∥ BF) |
| 6 | `FadeIn` × 4 | Purple pair ∠**AGE** = ∠**BGF** (vert. opp. ∠s at G) |

Three pairs → six angle arcs total.

## Step 1 — trim detail

Silent trims (`put_start_and_end_on`) before the fade-outs:

| Trim | Line key | Effect |
|------|----------|--------|
| top D—E—A | `lines["top_DA"]` | **DE** dropped → **EA** only |
| bottom C—B—F | `lines["bottom_CF"]` | **CB** dropped → **BF** only |

`FadeOut` one-by-one: `left_DC`, `diag_DB`, `seg_CG`, labels **D**, **C**, **H**.
`right_AB` (contains **AG**/**GB**) and `seg_EF` (contains **EG**/**GF**) stay.

## Colours

| Element | Constant | Colour |
|---------|----------|--------|
| **EA** highlight + **2k** | `COL_EA` | green |
| **BF** highlight + **5k** | `COL_BF` | yellow |
| ∠AEG / ∠BFG | `COL_AEF_EFB` | green |
| ∠EAG / ∠FBG | `COL_DAC_ABF` | red |
| ∠AGE / ∠BGF | `COL_BGF_EGA` | purple |

## Render

```powershell
.\.venv\Scripts\manim-slides.exe render resource\parallel-lines-diagram\manim\diagram.py ParallelLinesEagGbfAnglesDraw -ql
.\.venv\Scripts\manim-slides.exe convert --to=html ParallelLinesEagGbfAnglesDraw resource\parallel-lines-diagram\slides\eag-gbf-angles\index.html
```

> Requires `<repo-root>/manim/manim_styles.py` (provides `interior_angle_arc`).
