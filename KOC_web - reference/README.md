# KOC_web

Workspace for **Manim animations**, **Manim Slides**, **web design**, **LaTeX math**, and **UI design** — aligned with the existing DSE geometry tools in `resource/`.

## Folder layout

| Path | Purpose |
|------|---------|
| **`output/`** | **Finished HTML deliverables — open `output/index.html`** |
| `manim/scenes/` | Manim Community animation scenes |
| `manim-slides/presentations/` | Live slide presentations |
| `web/` | Vite + Tailwind + KaTeX web projects |
| `latex/templates/` | Reusable LaTeX article & Beamer templates |
| `latex/documents/` | Your math documents |
| `ui/tokens/` | Shared design tokens (colors, spacing) |
| `ui/components/` | UI component showcase |
| `resource/` | Source material: question, solution, Manim slide decks |
| `scripts/` | Helper scripts for render & build |

## The math solver (main deliverable)

The finished interactive page lives in **[`output/index.html`](output/index.html)**. It pairs the
parallelogram-area problem with a step-by-step solution and two Manim animation panels
(big-picture "Main Simulation" + focused "Diagram Analysis"). See [`output/README.md`](output/README.md)
for the step → animation map. Source material is under `resource/`:

| Content | Source |
|---------|--------|
| Question (LaTeX) | `resource/geometry_parallelogram_question.html` |
| Solution steps (LaTeX) | `resource/geometry_parallelogram_solution.md` |
| Animations (Manim slide decks) | `resource/parallel-lines-diagram/slides/` |

## Quick start

### Python (Manim + Slides)

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
```

**Render a Manim scene (preview):**
```powershell
.\.venv\Scripts\manim -c manim\manim.cfg -ql manim\scenes\sample_scene.py QuadraticFormula
```

**Build & present slides:**
```powershell
.\.venv\Scripts\manim-slides render manim-slides\presentations\sample_slides.py
.\.venv\Scripts\manim-slides present MathLessonSlides
```

Or use helper scripts:
```powershell
.\scripts\render-manim.ps1 -SceneFile manim\scenes\sample_scene.py -SceneName QuadraticFormula
.\scripts\render-slides.ps1 -SlidesFile manim-slides\presentations\sample_slides.py -Present
```

### Web

```powershell
cd web
npm install
npm run dev
```

Open `ui/components/showcase.html` in a browser for the UI kit (no build step).

### LaTeX

Requires MiKTeX (already detected on this machine).

```powershell
.\scripts\build-latex.ps1 latex\templates\math_article.tex
.\scripts\build-latex.ps1 latex\documents\example_equation.tex
```

## System requirements

- **ffmpeg** — installed ✓
- **LaTeX (MiKTeX)** — installed ✓
- **Python 3.9+** — `.venv` uses Python 3.14

### Windows note: PyAV / Manim

If `manim` fails with a PyAV DLL error (`ImportError: DLL load failed`), Windows Application Control may be blocking the `av` package binaries. Try:

1. Reinstall: `.\.venv\Scripts\pip install --force-reinstall av`
2. Allow the blocked DLL in Windows Security / App Control
3. Run the terminal as Administrator once to verify

## Design tokens

Brand colors match your existing tools (`#4f46e5` indigo, dark `#0f172a` background). See `ui/tokens/design-tokens.json`.
