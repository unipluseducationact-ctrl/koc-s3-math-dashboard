# Geometry

```
        D ——— E ——— A          ← top parallel (y = 2)
       / \       / \
      /   \     /   \
     C ——— B ——— F             ← bottom parallel (y = −2)
      \   /     \
       \ /       \
        G         EF ∩ AB
        H         DB ∩ CG
```

## Topology

- Top line: **D, E, A** collinear (left → right).
- Bottom line: **C, B, F** collinear (left → right).
- **ABCD** forms a slanted quadrilateral; **DC** and **AB** slope up-right.
- **DB** connects D to B.
- **EF** connects E to F; meets **AB** at **G**.
- **CG** connects C to **G**; meets **DB** at **H**.

## Intersections

| Point | Definition |
|-------|------------|
| **G** | `Line(A, B) ∩ Line(E, F)` |
| **H** | `Line(D, B) ∩ Line(C, G)` |

G and H are **never hand-placed** — always computed in `manim/diagram.py`.

## Reference coordinates

| Point | `[x, y]` |
|-------|----------|
| C | `[-4, -2]` |
| D | `[-2, 2]` |
| B | `[1, -2]` |
| A | `[3, 2]` |
| E | `[1.5, 2]` |
| F | `[4.5, -2]` |

Scene placement uses `SCALE = 0.52` and `CENTER = [0.25, 0, 0]`.

## Angle pairs (animation deck)

| Pair | Vertices | Colour | Reason |
|------|----------|--------|--------|
| ∠DAC = ∠ABF | A (arms AD, AB), B | red | corresponding (DA ∥ CB) |
| ∠AEF = ∠EFB | E, F | green | alternate |
| ∠BGF = ∠EGA | G, G | purple | vertically opposite at G |

## Shaded regions (steps 6–7)

| Region | Vertices | Colour | Step |
|--------|----------|--------|------|
| △EAG | E, A, G | red | 6 `FadeIn`, 7 `FadeOut` (2nd) |
| △GBF | G, B, F | green | 6 `FadeIn`, 7 `FadeOut` (1st) |

## Area comparison deck (`ParallelLinesAreaCompareDraw`)

Same △EAG / △GBF pair; steps 3–8 compare layout + k/area labels; step 9 removes all mobs one-by-one. See `docs/AREA_COMPARISON.md`.

## Triangle regions deck (`ParallelLinesTriangleRegionsDraw`)

| Region | Vertices | Colour |
|--------|----------|--------|
| △GBF | G, B, F | green |
| △GCB | G, C, B | blue |

Steps 2–4: altitudes, ink cleanup (DC/HD/EA/DG/GA), then △GCB shifted left beside △GBF with duplicate **G/B** labels. See `docs/TRIANGLE_REGIONS.md`.
