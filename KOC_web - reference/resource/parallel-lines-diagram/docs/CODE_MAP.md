# Code map — which code creates which element

Source file: [`manim/diagram.py`](../manim/diagram.py)

## Points

| Point | How created | Reference `[x, y]` |
|-------|-------------|-------------------|
| **C** | `C_REF` → `_to_frame()` | `[-4, -2]` |
| **D** | `D_REF` → `_to_frame()` | `[-2, 2]` |
| **B** | `B_REF` → `_to_frame()` | `[1, -2]` |
| **A** | `A_REF` → `_to_frame()` | `[3, 2]` |
| **E** | `E_REF` → `_to_frame()` | `[1.5, 2]` |
| **F** | `F_REF` → `_to_frame()` | `[4.5, -2]` |
| **G** | `_line_intersection(A,B,E,F)` | computed |
| **H** | `_line_intersection(D,B,C,G)` | computed |

## Lines (`build_lines()`)

| Dict key | Code | Segment | Notes |
|----------|------|---------|-------|
| `top_DA` | `_seg(D, A)` | D—A | top parallel; E on line |
| `bottom_CF` | `_seg(C, F)` | C—F | bottom parallel; B on line |
| `left_DC` | `_seg(C, D)` | C—D | left side of ▱ABCD |
| `right_AB` | `_seg(A, B)` | A—B | right slant |
| `seg_CG` | `_seg(C, G)` | C—G | ends at intersection G |
| `diag_DB` | `_seg(D, B)` | D—B | crosses CG at H |
| `seg_EF` | `_seg(E, F)` | E—F | crosses AB at G |

Draw animation order: `LINE_ORDER` in `diagram.py`.

## Labels (`build_labels()`)

| Dict key | Code | Placed at | Offset |
|----------|------|-----------|--------|
| `D` | `_point_label("D", D, …)` | D | `UP + RIGHT * 0.25` |
| `E` | `_point_label("E", E, …)` | E | `UP + RIGHT * 0.15` |
| `A` | `_point_label("A", A, …)` | A | `UP + RIGHT * 0.25` |
| `C` | `_point_label("C", C, …)` | C | `DOWN + LEFT * 0.35` |
| `B` | `_point_label("B", B, …)` | B | `DOWN` |
| `F` | `_point_label("F", F, …)` | F | `DOWN + LEFT * 0.2` |
| `G` | `_point_label("G", G, …)` | G | `RIGHT` |
| `H` | `_point_label("H", H, …)` | H | `UP + LEFT * (-0.03)` |

Fade-in order: `LABEL_ORDER` in `diagram.py`.

## Scenes

| Class | Background | Slides | Output |
|-------|------------|--------|--------|
| `ParallelLinesStill` | white (`BG`) | — | PNG still |
| `ParallelLinesDraw` | black (`DRAW_BG`) | 1 | base draw-out |
| `ParallelLinesSegmentLengthsDraw` | black | 9 | k-label highlights + teardown |
| `ParallelLinesAngleMarksDraw` | black | 7 | marks + angles + shaded △ + teardowns |
| `ParallelLinesAreaCompareDraw` | black | 9 | compare + k/area labels + final teardown |
| `ParallelLinesTriangleRegionsDraw` | black | 7 | △compare + k labels + area labels |
| `ParallelLinesDeBfParallelDraw` | black | 8 | // DEBF orange + cleanup + restore |
| `ParallelLinesCgbAngleMarksDraw` | black | 8 | DeBf end → ∠marks → trim to CH/HB/HG/BF/GF |
| `ParallelLinesChbLiftDraw` | black | 3 | Cgb end → △CHB lift → trim HB/H/B arcs |
| `ParallelLinesChbRegionsDraw` | black | 4 | ChbLift end → CB/7k, BF/5k, △fills + 245 cm² |
| `ParallelLinesChbRegionsContDraw` | black | 6 | ChbRegions end → cleanup → merge HCB → △HBG 175 cm² |
| `ParallelLinesChbHbgRestoreDraw` | black | 4 | Cont end → remove arcs → full graph + // marks + △HBG |
| `ParallelLinesChbHbgMarksDraw` | black | 7 | HbgRestore end → revised // + △CDH + three angle pairs |
| `ParallelLinesChbHbgKRegionsDraw` | black | 5 | ChbHbgMarks end → △EAG/△GBF + k segment labels |
| `ParallelLinesChbHbgKTrimDraw` | black | 4 | ChbHbgKRegions end → trim ink + △CDH + CDH-only cleanup |

## Helpers

| Function | Purpose |
|----------|---------|
| `_line_intersection(p1,p2,p3,p4)` | Infinite-line intersection |
| `_to_frame(raw)` | Reference coords → Manim scene coords |
| `_seg(p1, p2, ink)` | Single `Line` mobject |
| `_point_label(letter, at, direction, ink)` | Italic `Tex` label |
| `_layout(lines, labels)` | Scale-to-fit + centre on origin |
| `_laid_out_subsegment(line, …)` | Sub-segment endpoints on scaled ink |
| `_laid_out_vertices(lines)` | Vertex dict after scale-to-fit |
| `_laid_out_point_on_line(line, pt, …)` | One point mapped onto scaled line |
| `_parallel_arrow_mark(p_from, p_to, …)` | Parallel chevron at segment midpoint |
| `_interior_angle_fill(vertex, p1, p2, inside, color)` | Filled wedge + interior arc via `manim_styles` |
| `_highlight_seg(p1, p2, color)` | Thick coloured overlay line |
| `_length_label(tex, p1, p2, direction, ink)` | `MathTex` k-label at segment midpoint |
| `_filled_triangle(p1, p2, p3, color)` | Filled `Polygon` behind diagram ink |
| `_foot_to_horizontal(from_pt, y_level)` | Foot of vertical to horizontal y |
| `_dashed_horizontal(y, x_left, x_right, ink)` | Horizontal `DashedLine` reference |
| `_altitude_seg(from_pt, to_pt, color)` | Coloured altitude `Line` above fills |
| `_gcb_altitude_dash(tri, buff)` | Horizontal dash for △GCB altitude (step 2) |
| `_label_like_orig(letter, vertex, orig, ref_vertex)` | Duplicate label: scaled like diagram label |
| `_dash_between_heights(ht_left, ht_right)` | Horizontal dash connecting tops of two altitudes |
| `_double_parallel_arrow_mark(tip, tail)` | Pair of // chevrons; tips toward `tip` |
| `_filled_quad(p1…p4, color)` | Filled quadrilateral behind ink |
| `_de_bf_parallel_end_frame(scene, lines, labels)` | Static DeBf step-7 end decorations |
| `_build_cgb_angle_arcs(v, h_pt, ang_r)` | Five interior-angle VGroups |
| `_cgb_angle_marks_end_frame(scene, lines, labels)` | Static CgbAngleMarks step-7 end |
| `_chb_triangle_copy(…)` | Duplicate △CHB ink + labels + 3 arcs |
| `_chb_lift_amount(chb_dup, v, h_pt)` | Large vertical lift above lower apex, capped to frame |
| `_chb_lift_end_frame(scene, lines, labels)` | Static ChbLift step-2 end (lifted copy + trimmed original) |
| `_build_chb_regions_k_highlights(v, seg_cb_dup)` | CB/BF segment highlights + 7k/5k labels |
| `_build_chb_regions_fills_and_areas(…)` | △GCB/△GBF/△HCB fills + 420/300/245 cm² |
| `_chb_regions_end_frame(scene, lines, labels)` | Static ChbRegions step-3 end |
| `_build_chb_hbg_final_mobs(v, h_pt)` | Red △HBG + **175 cm²** label |
| `_chb_regions_cont_end_frame(scene, lines, labels)` | Static ChbRegionsCont step-5 end |
| `_restore_full_parallel_graph_ink(lines, labels, v)` | Full figure ink + **D…H** labels |
| `_build_parallel_graph_arrow_marks(lines, v)` | // **DE**/**BF** + double // **DB**/**EF** |
| `_tri_x_span_at_y(tri, y)` | Triangle left/right x at horizontal y |
| `_area_label_inside_at_y(ref, tri, tex, x_frac)` | Area label inside tri at ref y, x_frac from left |
| `_area_label_matched_inside_tri(ref, tri, tex, x_frac, y_frac)` | Match ref height; place inside tri at local y slice |
| `_triangle_outline(p1, p2, p3)` | Unfilled `Polygon` on top of ink |
| `_comparison_shift_grounded(guest, anchor, gap)` | Shift vector: guest left of anchor, same bottom y |
| `_label_at_vertex(letter, vertex, centroid)` | Outward vertex label (post-rotation safe) |
| `_area_label_in_triangle(tri, tex, color)` | Area MathTex scaled to triangle inradius |
| `_add_base_diagram(scene)` | Add scaled figure; return `lines`, `labels`, `diagram` |
| `_double_parallel_arrow_mark_matched_pair(…)` | Matched double // on parallel segments |
| `_chb_hbg_restore_end_frame` | Static ChbHbgRestore step-3 end |
| `_chb_hbg_marks_end_frame` | Static ChbHbgMarks step-6 end |
| `_build_chb_hbg_marks_arrow_marks(v)` | // on **CD** / **AB** (matched) |
| `_build_chb_hbg_marks_angle_arcs(v, h_pt)` | Six interior arcs (three colour pairs) |
| `_build_chb_hbg_k_region_mobs(v)` | △EAG/△GBF + EA/AG/BF/BG/DC k ink |
| `_chb_hbg_k_regions_end_frame` | Static ChbHbgKRegions step-4 end |
| `_chb_hbg_k_trim_end_frame` | Static ChbHbgKTrim step-2 end |
| `_trim_cdh_triangle_ink(lines, v, h_pt)` | White **DC**, **DH**, **HC** only |
| `_chb_hbg_k_final_cleanup_mobs(…)` | Mobjects to remove for CDH-only frame |
| `_chb_hbg_k_cdh_only_end_frame` | Static ChbHbgKTrim step-3 end (chain terminus) |

**CHB deck chain (all scenes + end-frame order):** [CHB_DECK_CHAIN.md](CHB_DECK_CHAIN.md)

## Region / label colours (CHB tail)

| Constant | Colour | Used for |
|----------|--------|----------|
| `COL_TRI_CDH` | Teal | △CDH fill |
| `COL_TRI_EAG_K` | Pink | △EAG (KRegions deck) |
| `COL_TRI_GBF` | Green | △GBF fill |
| `COL_TRI_HBG` | Red | △HBG fill |
| `AREA_CDH_H_SHIFT` | — | Nudge **343 cm²** right inside △CDH |
