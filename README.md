# KOC S3 Math Dashboard (Summer 2026)

Interactive math dashboards for five S3 summer topics: **Factorization**, **Inequality**, **Percentages**, **Area & Volume**, and **Probability**.

## Open the dashboard

**Local:** open [`dashboard/index.html`](dashboard/index.html) in a browser.

**GitHub Pages:** after Pages is enabled, use:

`https://unipluseducationact-ctrl.github.io/koc-s3-math-dashboard/dashboard/index.html`

## Structure

| Path | Description |
|------|-------------|
| `dashboard/index.html` | Hub gallery — click a topic card |
| `dashboard/topics/*` | Per-topic tabs: Concept, Tools, Game, Worked Solutions |
| `dashboard/slides/*` | Manim Reveal decks + PowerPoint video exports (`*-main-deck/`) |
| `S3 MATH summer 2026/` | Source PowerPoints and lesson materials |

## Worked Solutions (PowerPoint videos)

Export guide: [`dashboard/slides/PPT_VIDEO_EXPORTS.md`](dashboard/slides/PPT_VIDEO_EXPORTS.md)

Automated export (Windows + PowerPoint):

```powershell
cd dashboard
.\tools\export_ppt_video.ps1 -Pptx "..\S3 MATH summer 2026\...\PPT\....pptx" -OutMp4 "slides\...\main.mp4"
```
