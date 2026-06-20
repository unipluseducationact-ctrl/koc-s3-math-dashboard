# KOC_test — Interview exercise setup

## Purpose

This folder is a **self-contained package for technical interview candidates**. Each interviewee receives **only** this `KOC_test` folder.

The exercise: candidates work on `index.html` here and try to restore it to match the **final, correct version** of the interactive geometry lab page.

## Reference answer (do not give to interviewees)

The finalized, correct page lives in the parent repository at:

```
../output/index.html
```

That file is the **ground truth**. Any future edits to `KOC_test/index.html` should be designed so that a skilled candidate can diagnose gaps and bring their copy back to functional parity with `output/index.html`.

## What is in this folder

| Path | Role |
|------|------|
| `index.html` | Starting copy of the finished page. **Currently identical** to `output/index.html` — not yet modified for the interview. |
| `manim-slides/` | Duplicate of the repo’s `manim-slides` folder (Manim-Slides sample / tooling). Included so candidates have the same ancillary assets the project uses. |

## Instructions for the preparing agent

1. **Do not modify `index.html` until the interview variant is ready.** As of setup, it is a byte-for-byte duplicate of the reference.
2. When preparing the interview version, deliberately break, simplify, or remove parts of `KOC_test/index.html` (and adjust paths or bundled assets as needed) so the page no longer fully matches `output/index.html`.
3. Ensure interviewees can open and work on `index.html` from this folder alone — they will **not** have access to `output/` or the rest of the repo.
4. Document any intentional omissions or broken behaviour in a separate brief for interviewers (not in this file, unless you replace this section).

## Notes on the page

`index.html` is an interactive **Geometry Lab: Parallelogram Area** page. In the full repo it references slide decks under `../resource/parallel-lines-diagram/slides/`. When stripping this folder down for interviews, consider whether those assets must be copied in, inlined, or mocked — otherwise iframe-based animations will not load.

See `../output/README.md` in the parent repo for a full description of tabs, step-to-deck mapping, and behaviour of the finished page.

## Current status

- [x] `KOC_test` folder created
- [x] `index.html` copied from `output/index.html` (unchanged)
- [x] `manim-slides/` copied from repo root
- [ ] Interview variant of `index.html` prepared (intentional diffs from reference)
- [ ] Interviewer brief / scoring rubric (optional)
