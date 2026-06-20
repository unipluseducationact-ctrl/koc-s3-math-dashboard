# Triangle ratio lab — Equal Height / Equal Base

Manim slide decks for the **EQUAL HEIGHT / EQUAL BASE TRIANGLES** tab in `output/index.html`.

| Deck | Manim scene | HTML |
|------|-------------|------|
| Equal height | `EqualHeightTrianglesDraw` | `slides/equal-height/index.html` |
| Equal base (same side) | `EqualBaseSameSideDraw` | `slides/equal-base-same/index.html` |
| Equal base (opposite sides) | `EqualBaseOppositeDraw` | `slides/equal-base-opposite/index.html` |

Source: `manim/scenes/triangle_ratio_lab.py` — all diagram labels use `MathTex` (LaTeX).

## Re-render

```powershell
cd C:\Users\Kinny\Desktop\KOC_web
.\.venv\Scripts\manim-slides.exe render manim\scenes\triangle_ratio_lab.py EqualHeightTrianglesDraw EqualBaseSameSideDraw EqualBaseOppositeDraw -ql
.\.venv\Scripts\manim-slides.exe convert --to=html EqualHeightTrianglesDraw resource\triangle-ratio-lab\slides\equal-height\index.html
.\.venv\Scripts\manim-slides.exe convert --to=html EqualBaseSameSideDraw resource\triangle-ratio-lab\slides\equal-base-same\index.html
.\.venv\Scripts\manim-slides.exe convert --to=html EqualBaseOppositeDraw resource\triangle-ratio-lab\slides\equal-base-opposite\index.html
```
