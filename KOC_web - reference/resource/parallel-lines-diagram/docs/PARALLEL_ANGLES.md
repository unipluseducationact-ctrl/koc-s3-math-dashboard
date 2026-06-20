# Parallel marks, angle pairs & shaded regions — 7 steps

Scene: `ParallelLinesAngleMarksDraw` in `manim/diagram.py`

Base frame: full diagram (white ink on black). Steps 1–4 add marks; step 5 removes them one-by-one.

## Build steps (1–4)

| Step | Animation | Marks | Colour | Equal pair |
|------|-----------|-------|--------|------------|
| 1 | `Create(arr_da)`, `Create(arr_cb)` | parallel chevrons on **DA** and **CB** midpoints (tip on ink) | white | — |
| 2 | `FadeIn` filled ∠**DAC**, ∠**ABF** | A: rays AD + **AB**; B: BA + BF | red | corresponding |
| 3 | `FadeIn` filled ∠**AEF**, ∠**EFB** | E: EA + EF; F: FE + FB | green | alternate |
| 4 | `FadeIn` filled ∠**BGF**, ∠**EGA** | G: GB + GF; G: GE + GA | purple | vertically opposite |

## Teardown step (5)

One slide beat. Each row is one `FadeOut` — **not** a batched `VGroup`. Order is reverse of build.

| # | `FadeOut` target | What disappears |
|---|------------------|-----------------|
| 1 | `ang_ega[0]` | purple filled wedge ∠EGA (at G) |
| 2 | `ang_ega[1]` | purple arc outline ∠EGA (at G) |
| 3 | `ang_bgf[0]` | purple filled wedge ∠BGF (at G) |
| 4 | `ang_bgf[1]` | purple arc outline ∠BGF (at G) |
| 5 | `ang_efb[0]` | green filled wedge ∠EFB (at F) |
| 6 | `ang_efb[1]` | green arc outline ∠EFB (at F) |
| 7 | `ang_aef[0]` | green filled wedge ∠AEF (at E) |
| 8 | `ang_aef[1]` | green arc outline ∠AEF (at E) |
| 9 | `ang_abf[0]` | red filled wedge ∠ABF (at B) |
| 10 | `ang_abf[1]` | red arc outline ∠ABF (at B) |
| 11 | `ang_dac[0]` | red filled wedge ∠DAC (at A) |
| 12 | `ang_dac[1]` | red arc outline ∠DAC (at A) |
| 13 | `arr_cb` | parallel arrow on **CB** |
| 14 | `arr_da` | parallel arrow on **DA** |

After step 5 only the base diagram (white lines + point labels) remains.

## Shaded regions step (6)

| Step | Animation | Region | Colour | Vertices |
|------|-----------|--------|--------|----------|
| 6 | `FadeIn(tri_eag)`, `FadeIn(tri_gbf)` | △**EAG** | red | E, A, G |
| 6 | (same beat) | △**GBF** | green | G, B, F |

Fills use `_filled_triangle` at `z_index = -1` so white diagram ink stays on top.

User note: “rectangle GBF” in the brief maps to △**GBF** (three named vertices G, B, F).

## Shaded regions teardown (7)

One slide beat. Each row is one `FadeOut` — **not** a batched `VGroup`. Order is reverse of step 6.

| # | `FadeOut` target | What disappears |
|---|------------------|-----------------|
| 1 | `tri_gbf` | green fill △**GBF** (G, B, F) |
| 2 | `tri_eag` | red fill △**EAG** (E, A, G) |

After step 7 only the base diagram (white lines + point labels) remains.

Each filled angle is `VGroup(wedge, arc)` from `_interior_angle_fill`:
- `[0]` = filled `VMobject` wedge
- `[1]` = `interior_angle_arc` outline

## Geometry notes

| Angle | Vertex | Rays | `inside_point` |
|-------|--------|------|----------------|
| ∠DAC | A | A→D, A→**B** (along drawn AB) | centroid △ADB |
| ∠ABF | B | B→A, B→F | centroid △ABF |
| ∠AEF | E | E→A, E→F | centroid △AEF |
| ∠EFB | F | F→E, F→B | centroid △EFB |
| ∠BGF | G | G→B, G→F | centroid △BGF |
| ∠EGA | G | G→E, G→A | centroid △EGA |

Vertex positions come from `_laid_out_vertices(lines)` — post scale-to-fit endpoints, not raw `*_REF` constants.

## Helpers

| Function | Creates |
|----------|---------|
| `_laid_out_vertices(lines)` | dict D…G on scaled diagram |
| `_parallel_arrow_mark(p_from, p_to)` | chevron at segment midpoint (tip on ink) |
| `_interior_angle_fill(vertex, p1, p2, inside_point, color)` | `VGroup(wedge, arc)` |
| `_filled_triangle(p1, p2, p3, color)` | filled `Polygon` behind ink |

## Render

```powershell
.\scripts\render_slides.ps1 `
  -SceneFile adhoc/parallel-lines-diagram/manim/diagram.py `
  -SceneName ParallelLinesAngleMarksDraw `
  -OutputDir adhoc/parallel-lines-diagram/slides/angle-marks `
  -Quality ql `
  -MediaDir media/adhoc
```

Preview: `http://localhost:8000/adhoc/parallel-lines-diagram/slides/angle-marks/index.html`
