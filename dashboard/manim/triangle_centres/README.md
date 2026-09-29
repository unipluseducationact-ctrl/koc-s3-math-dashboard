# JM28 Special Lines and Centres in Triangles — Manim slides

Concept & Formula decks for `topics/triangle_centres/`.

## Files

| File | What it is |
|------|------------|
| `tc_common.py` | Palette, geometry (mid-point, foot, centres) and marking helpers (ticks, arcs, right-angle marks). |
| `special_lines.py` | `TriangleSpecialLines` deck: median, altitude, angle bisector, perpendicular bisector, then a recap. |
| `centres.py` | `TriangleCentres` deck: centroid (2 : 1), orthocentre, in-centre (incircle), circumcentre (circumcircle), then right-angled / obtuse cases and a summary table. |

## Colour convention

Same line type = same colour in both decks:

| line | colour | centre |
|------|--------|--------|
| median | amber | centroid `G` |
| altitude | blue | orthocentre `H` |
| angle bisector | green | in-centre `I` |
| perpendicular bisector | pink | circumcentre `O` |

Equal lengths use red tick marks; equal angles use matching arcs; right angles use a small square.

## Render

Render from a scratch folder outside the repo so the `slides/` and `media/` build caches are not committed:

```powershell
$m = "<repo>\dashboard\manim\triangle_centres"
$o = "<repo>\dashboard\slides\triangle_centres"
cd $env:TEMP\jm28-manim
python -m manim_slides render "$m\special_lines.py" TriangleSpecialLines --quality h --media_dir media
python -m manim_slides convert TriangleSpecialLines "$o\special-lines\index.html" --to html
python -m manim_slides render "$m\centres.py" TriangleCentres --quality h --media_dir media
python -m manim_slides convert TriangleCentres "$o\centres\index.html" --to html
```

After converting, add `<script src="../../../shared/video-cdn.js"></script>` before `Reveal.initialize` in each deck's `index.html` (the same patch as the other decks) and replace the old `index_assets/` folder.

Output decks:
- `dashboard/slides/triangle_centres/special-lines/index.html`
- `dashboard/slides/triangle_centres/centres/index.html`
