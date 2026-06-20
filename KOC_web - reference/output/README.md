# Output — final HTML deliverables

**This folder holds the finished, ready-to-open HTML page.** Open it in a browser.

| File | What it is |
|------|------------|
| `index.html` | The interactive solver for the parallelogram-area problem. Open this. |

## What `index.html` shows

```
┌───────────────────────────────┬──────────────────────┐
│  Main Simulation  (iframe)     │                      │
│  → big-picture full figure     │  Solution Derivation │
│  resource/.../slides/index.html│  (question + 7 steps)│
├───────────────────────────────┤                      │
│  Diagram Analysis (iframe)     │  Click a step or use │
│  → focused per-step animation  │  PREV / NEXT to walk │
│  switches with the active step │  through the proof   │
└───────────────────────────────┴──────────────────────┘
```

- **Main Simulation** = the whole evolving figure (big picture).
- **Diagram Analysis** = a focused Manim animation that changes with each solution step.
- Navigate with the **NEXT STEP / PREV** buttons, the arrow keys, or by clicking a step card.
- The chevron button hides the solution panel; the **expand** button on the main panel maximizes the animations.

## Sources this page pulls from

| Content | Source |
|---------|--------|
| Question (LaTeX) | `../resource/geometry_parallelogram_question.html` |
| Solution steps (LaTeX) | `../resource/geometry_parallelogram_solution.md` |
| Animations | `../resource/parallel-lines-diagram/slides/<deck>/index.html` |

## Step → animation deck map (all 14 decks used)

**Main Simulation** shows the overall figure — the base deck by default, or a
full-figure deck when a step highlights something globally. **Diagram Analysis**
switches per step to the zoomed / extracted-triangle deck:

| Step | Topic | Main-simulation deck | Diagram-analysis deck |
|------|-------|----------------------|------------------------|
| 1 | Mark $DE=5k$, $EA=2k$, $CB=7k$, $BF=5k$ | `segment-lengths-angle-marks` slides 0–7 | *(empty)* |
| 2 | // marks → △EAG/△GBF fills (main) → isolated view + AAA angles (sub, synced to main slides 10–12) | `segment-lengths-angle-marks` slides 8–12 | `eag-gbf-angles` slides 0–3 |
| 3 | Side-by-side compare, $(2/5)^2 = 48/[\triangle BFG]$ → $300$ (sub pulls △EAG; main holds until areas) | `segment-lengths-angle-marks` slides 12–14 | `eag-gbf-angles` slides 3–9 (main sync: fade angles → hold → areas) |
| 4 | Same height, bases $7:5$ → $[\triangle CBG]=420$ | `segment-lengths-angle-marks` slides 14–16 hold, 17 = 420 | `gcb-gbf-regions` slides 0–4 (420 synced on final beat) |
| 5 | $DE = BF$, $DE \parallel BF$ → ▱$DEFB$ → $DB \parallel EF$ | `segment-lengths-angle-marks` slide 17 hold → 18 (HB/GF //) | `de-bf-parallel` (sync: sub slide 6 → main 18) |
| 6 | Corr. angles + common angle → $\triangle CHB \sim \triangle CGF$ (AAA); lift $\triangle CHB$ | `segment-lengths-angle-marks` slide 18 (HB/GF //) | `cgb-angle-marks` |
| 7 | $(7/12)^2 \times 720$ → $[\triangle CHB]=245$ | `segment-lengths-angle-marks` slide 17 (hold) | `chb-regions` |
| 8 | Overlay back: $[\triangle GBH] = 420-245 = 175$ | `segment-lengths-angle-marks` slide 17 (hold) | `chb-regions-cont` |
| 9 | Restore full figure + // marks (keep red $\triangle HBG$) | `segment-lengths-angle-marks` slide 17 (hold) | `chb-hbg-restore` |
| 10 | $CD \parallel GB$: alt. + vert. opp. angles → $\triangle CDH \sim \triangle GBH$ (AAA) | `segment-lengths-angle-marks` slide 17 (hold) | `chb-hbg-marks` |
| 11 | $AG=2k$, $GB=5k$, $CD=7k$ | `segment-lengths-angle-marks` slide 17 (hold) | `chb-hbg-k-regions` |
| 12 | $(5/7)^2 = 175/[\triangle CDH]$ → $[\triangle CDH]=343\ \text{cm}^2$ | `segment-lengths-angle-marks` slide 17 (hold) | `chb-hbg-k-trim` |

Rendered so far: base, `segment-lengths`, `angle-marks`, `eag-gbf-angles`
(steps 1–2 fully animated). The remaining decks render the same way — see
`docs/EAG_GBF_ANGLES.md` for the command pattern.

> Note: the manim source previously labelled $\triangle CHB$ as 255 cm²; this was corrected
> to **245 cm²** in `manim/diagram.py` and the docs (since $(7/12)^2 \times 720 = 245$,
> consistent with $420 - 245 = 175$).

## Note on the animations

The slide decks are Manim-Slides / Reveal.js pages whose background videos live in each
deck's `index_assets/*.mp4`. The decks for steps 1–2 (base figure, `segment-lengths`,
`angle-marks`, `eag-gbf-angles`) are **already rendered**. The remaining decks still
need rendering from `resource/parallel-lines-diagram/manim/diagram.py`:

```powershell
.\.venv\Scripts\manim-slides.exe render resource\parallel-lines-diagram\manim\diagram.py <SceneName> -ql
.\.venv\Scripts\manim-slides.exe convert --to=html <SceneName> resource\parallel-lines-diagram\slides\<deck>\index.html
```

Scene-name ↔ deck mapping is in `resource/parallel-lines-diagram/README.md`.
Once converted, the page picks them up automatically — no change needed in `index.html`.

## Similar Triangles in Parallelogram tab

Header tab **Similar Triangles in Parallelogram** opens an interactive SVG lab (no Manim iframes). Three modes:

| Mode | Triangles | Pattern |
|------|-----------|---------|
| Bowtie · EAG ~ GBF | △EAG, △GBF | Opposite parallel bases EA / BF; bowtie at G |
| Bowtie · CDH ~ GBH | △CDH, △GBH | Opposite sides CD / GB; bowtie at H |
| Common Angle · CHB ~ CGF | △CHB, △CGF | Shared ∠GCB at C |

Toggle AAA angle pairs, show/hide dimmed figure ink, and read live side-ratio math in the right panel. Geometry matches `resource/parallel-lines-diagram/manim/diagram.py` reference coordinates.

## Label overlap audit

Diagram labels in the **Equal Height / Equal Base** and **Similar Triangles in Parallelogram** tabs are checked by an automated script that mirrors the SVG layout math in `index.html`.

```powershell
node scripts/audit-label-overlap.js
```

**What it checks (90 scenarios):** 3 triangle-lab configs × 5 steps × 3 slider corners, plus 3 parallelogram-sim modes × 5 steps × 3 slider corners.

**Per label:**

| Kind | Rule |
|------|------|
| Interior (area / side length inside shaded triangles) | Anchor point inside the triangle; ≥ 10 px from each edge |
| Exterior (dimensions, annotations) | No pairwise overlap between non-vertex labels (4 px gap) |

Exit code `0` = pass; `1` = failures printed with `{ tab, mode, step, corner, labelId, failureType }`.

**Placement rules in code:**

- Shared helpers: `LabelGeom` (`triCentroid`, `triLabelPoint`, `nudgeToInterior`) in `index.html`
- Interior labels use barycentric inset + edge clearance, not fixed pixel nudges on slopes
- Vertex labels offset per mode/step via `computeLabelOffsets`
- Leader annotations (`bowtie at H`, `∠GCB common`) only on the step that introduces the concept (step 2 / step 1)
