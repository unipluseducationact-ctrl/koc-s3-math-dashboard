"""Parallel-lines diagram — ABCD with internal intersections G and H.

Element registry
----------------
  Lines   → build_lines()     keys in LINE_ORDER
  Labels  → build_labels()    keys match point names
  Points  → C…F anchors; G, H computed (never hand-placed)

Scenes
------
  ParallelLinesStill                 white BG, full diagram (PNG still)
  ParallelLinesDraw                  black BG, one slide: lines then labels
  ParallelLinesSegmentLengthsDraw    black BG, 9 steps: segment k labels + teardown
  ParallelLinesSegmentLengthsBuildDraw black BG, 8 steps: segment k labels only (no teardown)
  ParallelLinesSegmentLengthsAngleMarksDraw black BG, 15 steps: segment k labels then // + angles (no redraw)
  ParallelLinesAngleMarksDraw        black BG, 7 steps: marks + angles + shaded regions
  ParallelLinesAreaCompareDraw       black BG, 9 steps: compare + k + area + teardown
  ParallelLinesTriangleRegionsDraw   black BG, 7 steps: △compare + k labels + areas
  ParallelLinesDeBfParallelDraw      black BG, 8 steps: // DEBF + cleanup + restore
  ParallelLinesCgbAngleMarksDraw     black BG, 10 steps: DeBf end → ∠marks → △CHB lift
  ParallelLinesChbLiftDraw           black BG, 3 steps: (legacy) △CHB lift only
  ParallelLinesChbRegionsDraw        black BG, 4 steps: k labels + △fills + 245 cm²
  ParallelLinesChbRegionsContDraw    black BG, 6 steps: merge HCB→GCB, △HBG 175 cm²
  ParallelLinesChbHbgRestoreDraw     black BG, 4 steps: full graph + △HBG 175 cm²
  ParallelLinesChbHbgMarksDraw       black BG, 7 steps: revised // marks + △CDH + angle pairs
  ParallelLinesChbHbgKRegionsDraw    black BG, 5 steps: △EAG/△GBF + k segment labels
  ParallelLinesChbHbgKTrimDraw        black BG, 4 steps: trim ink + △CDH + CDH-only frame
  ParallelLinesEagGbfAnglesDraw      black BG, 7 steps: isolate △EAG/△GBF + // + angle pairs

CHB deck chain (△CHB lift → △CDH final): see `docs/CHB_DECK_CHAIN.md`.
Search `# ── STEP` inside each `ParallelLinesChb*` class for slide beats.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from manim import *
from manim_slides import Slide

_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_ROOT / "manim"))
import manim_styles as s

# ══════════════════════════════════════════════════════════════════════════════
# STYLE
# ══════════════════════════════════════════════════════════════════════════════
INK = BLACK          # still: line + label colour
BG = WHITE           # still: scene background
DRAW_INK = WHITE     # slides: line + label colour
DRAW_BG = BLACK      # slides: scene background (Reveal.js background video)
STROKE = 2.5
HIGHLIGHT_STROKE = 8.0
FONT = 34
LENGTH_FONT = 36
AREA_FONT = 38
AREA_LABEL_FILL = 0.38  # label height ≤ fill × 2× inradius of host triangle
AREA_LABEL_MIN_HEIGHT = 0.15  # floor so long labels (e.g. 420 cm²) stay readable
AREA_GCB_FILL = 0.50  # △GCB is wider — allow larger area text
AREA_EAG_VERT_SHIFT = 0.14  # nudge 48 cm² down inside red △EAG (side-by-side sub)
AREA_LABEL_H_SHIFT = 0.12  # nudge 48 cm² left inside red △EAG (side-by-side sub)
AREA_EAG_MAIN_H_SHIFT = 0.10  # card 3 main: nudge 48 cm² right toward centre
AREA_EAG_MAIN_V_SHIFT = 0.34  # card 3 main: nudge 48 cm² up toward centre
AREA_EAG_MAIN_SIZE_SCALE = 1.2  # card 3 main: 48 cm² font +20%
G_LABEL_COMPARE_UP = 0.14  # card 3 sub: nudge both G labels upward
G_LABEL_COMPARE_LEFT = 0.16  # card 3 sub: nudge both G labels leftward
AREA_GBF_H_SHIFT = 0.20  # nudge 300 cm² further left inside green △GBF
AREA_GCB_AREA_X_FRAC = 0.46  # 420 cm²: inside △GCB at same y as 300 cm² (higher → righter)
AREA_HCB_X_FRAC = 0.68  # 245 cm²: right-of-centre inside lifted △HCB
AREA_HCB_Y_FRAC = 0.52  # vertical fraction between base CB and apex H
AREA_HBG_H_SHIFT = 0.14  # nudge 175 cm² left inside red △HBG
AREA_HBG_V_SHIFT = 0.26  # nudge 175 cm² up inside red △HBG
AREA_CDH_H_SHIFT = 0.18  # nudge 343 cm² right inside teal △CDH
FIT_HEIGHT = 0.72
LABEL_BUFF = 0.22

# Segment highlight colours (on black draw background)
COL_DE = YELLOW
COL_EA = GREEN
COL_CB = BLUE
COL_DC = BLUE  # **DC** + **7k** (ChbHbgKRegions) — same ink as prior **CB**/**7k**
COL_BF = YELLOW

# Angle-pair colours (ParallelLinesAngleMarksDraw)
COL_DAC_ABF = RED
COL_AEF_EFB = GREEN
COL_BGF_EGA = PURPLE

# Shaded regions
COL_TRI_EAG = RED
COL_TRI_EAG_K = PINK  # △EAG on ChbHbgKRegions (full figure)
COL_TRI_GBF = GREEN
COL_TRI_GCB = BLUE
COL_TRI_HCB = ORANGE  # lifted △HCB fill — unused elsewhere on ChbRegions deck
COL_TRI_HBG = RED     # △HBG after lowering HCB onto GCB (ChbRegionsCont)
COL_TRI_CDH = TEAL    # △CDH (ChbHbgMarks) — unused elsewhere on this figure
COL_ANGLE_CDB_GBH = GOLD   # ∠CDB / ∠GBH pair (ChbHbgMarks)
COL_ANGLE_DCH_HGB = PINK   # ∠DCH / ∠HGB pair (ChbHbgMarks)
COL_ANGLE_DHC_GHB = MAROON   # ∠DHC / ∠GHB pair (ChbHbgMarks)
COL_DEBF = ORANGE
COL_CGB_CHB = PURPLE
COL_CFG_CBH = BLUE
COL_GCB_ANGLE = GREEN
REGION_FILL_OPACITY = 0.48
HEIGHT_DASH_LENGTH = 0.10
HEIGHT_DASH_BUFF = 0.15  # extend dashed horizontal past foot / through G
G_LABEL_DASH_BUFF = 0.12  # extend connecting dash slightly past right G label
G_VERTEX_DASH_BUFF = 0.18  # extend connecting dash left past △GCB vertex G
GCB_COMPARE_GAP = 0.45  # △GCB left of △GBF (smaller → closer / less overshoot)
COMPARE_GAP = 1.15  # horizontal gap between △EAG and △GBF (clear vertex labels)

PARALLEL_ARROW_SIZE = 0.36
PARALLEL_ARROW_STROKE = 3.5
# Double // marks: chevron centres as fractions along tip→tail (closer = smaller gap).
DOUBLE_PARALLEL_ARROW_FRAC_1 = 0.44
DOUBLE_PARALLEL_ARROW_FRAC_2 = 0.56
ANGLE_RADIUS = 0.30
CGB_ANGLE_RADIUS = 0.44  # larger arcs in ParallelLinesCgbAngleMarksDraw
CHB_LIFT_GAP = 3.60  # minimum vertical shift for duplicated △CHB
CHB_LIFT_CLEAR = 1.35  # clearance above lower apex (H / G) after lift
CHB_LIFT_EXTRA = 1.10  # additional lift on top of auto clearance
ANGLE_STROKE = 2.5
ANGLE_FILL_OPACITY = 0.55

# ══════════════════════════════════════════════════════════════════════════════
# ANCHOR POINTS (reference space — edit these to reshape the figure)
# ══════════════════════════════════════════════════════════════════════════════
# Top parallel (y = 2)
D_REF = np.array([-2.0, 2.0, 0.0])
E_REF = np.array([1.5, 2.0, 0.0])   # on DA
A_REF = np.array([3.0, 2.0, 0.0])
# Bottom parallel (y = -2)
C_REF = np.array([-4.0, -2.0, 0.0])
B_REF = np.array([1.0, -2.0, 0.0])  # on CF
F_REF = np.array([4.5, -2.0, 0.0])

SCALE = 0.52
CENTER = np.array([0.25, 0.0, 0.0])


def _line_intersection(p1, p2, p3, p4) -> np.ndarray:
    x1, y1, _ = p1
    x2, y2, _ = p2
    x3, y3, _ = p3
    x4, y4, _ = p4
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    return np.array([x1 + t * (x2 - x1), y1 + t * (y2 - y1), 0.0])


# ══════════════════════════════════════════════════════════════════════════════
# COMPUTED POINTS (do not hand-place)
# ══════════════════════════════════════════════════════════════════════════════
G_REF = _line_intersection(A_REF, B_REF, E_REF, F_REF)  # AB ∩ EF
H_REF = _line_intersection(D_REF, B_REF, C_REF, G_REF)  # DB ∩ CG


def _to_frame(raw: np.ndarray) -> np.ndarray:
    v = raw - CENTER
    return np.array([v[0] * SCALE, v[1] * SCALE, 0.0])


# Scene coordinates — used by lines and labels below
C = _to_frame(C_REF)
D = _to_frame(D_REF)
B = _to_frame(B_REF)
A = _to_frame(A_REF)
E = _to_frame(E_REF)
F = _to_frame(F_REF)
G = _to_frame(G_REF)
H = _to_frame(H_REF)

# ══════════════════════════════════════════════════════════════════════════════
# DRAW ORDER (ParallelLinesDraw lagged Create sequence)
# ══════════════════════════════════════════════════════════════════════════════
LINE_ORDER = [
    "top_DA",      # top parallel  D — E — A
    "bottom_CF",   # bottom parallel C — B — F
    "left_DC",     # left slant C → D
    "right_AB",    # right slant A → B  (side of ▱ABCD)
    "seg_CG",      # C → G (closes to intersection)
    "diag_DB",     # D → B
    "seg_EF",      # E → F  (crosses AB at G)
]

LABEL_ORDER = ["D", "E", "A", "C", "B", "F", "G", "H"]



_REMOVE_RT = 1 / 15  # one frame at 480p15 — reads as instant


def _remove(scene: Slide, *mobs: Mobject) -> None:
    """Remove mobs instantly (no fade); slide boundary records one short hold."""
    to_drop = [m for m in mobs if m is not None]
    if not to_drop:
        return
    scene.remove(*to_drop)
    scene._rm_dirty = True  # type: ignore[attr-defined]


_orig_slide_play = Slide.play
_orig_slide_next = Slide.next_slide


def _slide_play(self: Slide, *anims, **kwargs):
    self._rm_dirty = False  # type: ignore[attr-defined]
    return _orig_slide_play(self, *anims, **kwargs)


def _slide_next(self: Slide, *args, **kwargs):
    if getattr(self, "_rm_dirty", False):
        _orig_slide_play(self, Wait(_REMOVE_RT), run_time=_REMOVE_RT)
        self._rm_dirty = False  # type: ignore[attr-defined]
    return _orig_slide_next(self, *args, **kwargs)


Slide.play = _slide_play  # type: ignore[method-assign]
Slide.next_slide = _slide_next  # type: ignore[method-assign]


def _seg(p1: np.ndarray, p2: np.ndarray, ink: ManimColor = INK) -> Line:
    return Line(p1, p2, color=ink, stroke_width=STROKE)


def _point_label(
    letter: str,
    at: np.ndarray,
    direction: np.ndarray,
    ink: ManimColor = INK,
    buff: float = 0.14,
) -> Tex:
    return Tex(rf"\textit{{{letter}}}", color=ink, font_size=FONT).next_to(at, direction, buff=buff)


def _label_at_vertex(
    letter: str,
    vertex: np.ndarray,
    centroid: np.ndarray,
    ink: ManimColor = DRAW_INK,
    buff: float = 0.14,
) -> Tex:
    """Point label pushed outward from triangle centroid (works after rotation)."""
    direction = vertex - centroid
    norm = float(np.linalg.norm(direction[:2]))
    if norm < 1e-8:
        direction = UP
    else:
        direction = direction / norm
    return _point_label(letter, vertex, direction, ink, buff=buff)


def _label_like_orig(
    letter: str,
    vertex: np.ndarray,
    orig_label: Tex,
    ref_vertex: np.ndarray,
    ink: ManimColor = DRAW_INK,
) -> Tex:
    """Duplicate label: match scaled height + centre offset from ref_vertex."""
    lbl = Tex(rf"\textit{{{letter}}}", color=ink, font_size=FONT)
    lbl.match_height(orig_label)
    lbl.move_to(vertex + (orig_label.get_center() - ref_vertex))
    return lbl


def _altitude_top(pt_a: np.ndarray, pt_b: np.ndarray) -> np.ndarray:
    """Upper endpoint of a vertical (or near-vertical) altitude segment."""
    return pt_a if pt_a[1] >= pt_b[1] else pt_b


def _dash_between_heights(
    ht_left: Line,
    ht_right: Line,
    left_buff: float = G_VERTEX_DASH_BUFF,
    right_buff: float = G_LABEL_DASH_BUFF,
    ink: ManimColor = DRAW_INK,
) -> DashedLine:
    """Horizontal dash from top of left altitude to top of right altitude."""
    top_l = _altitude_top(ht_left.get_start(), ht_left.get_end())
    top_r = _altitude_top(ht_right.get_start(), ht_right.get_end())
    y = top_l[1]
    x_lo = top_l[0] - left_buff
    x_hi = top_r[0] + right_buff
    dash = _dashed_horizontal(y, x_lo, x_hi, ink=ink)
    dash.set_z_index(2)
    return dash


def build_lines(ink: ManimColor = INK) -> dict[str, Line]:
    """Return named Line mobjects. Keys match LINE_ORDER + CODE_MAP.md."""
    return {
        # ── Parallel horizontals ──────────────────────────────────────────
        "top_DA": _seg(D, A, ink),       # passes through E
        "bottom_CF": _seg(C, F, ink),    # passes through B
        # ── Quadrilateral ABCD ────────────────────────────────────────────
        "left_DC": _seg(C, D, ink),
        "right_AB": _seg(A, B, ink),
        # ── Internal segments ───────────────────────────────────────────
        "diag_DB": _seg(D, B, ink),      # crosses CG at H
        "seg_EF": _seg(E, F, ink),       # crosses AB at G
        "seg_CG": _seg(C, G, ink),       # ends at G
    }


def build_labels(ink: ManimColor = INK) -> dict[str, Tex]:
    """Return named Tex labels. Keys match LABEL_ORDER + CODE_MAP.md."""
    return {
        # ── Top line ──────────────────────────────────────────────────────
        "D": _point_label("D", D, UP + RIGHT * 0.25, ink),
        "E": _point_label("E", E, UP + RIGHT * 0.15, ink),
        "A": _point_label("A", A, UP + RIGHT * 0.25, ink),
        # ── Bottom line ───────────────────────────────────────────────────
        "C": _point_label("C", C, DOWN + LEFT * 0.35, ink),
        "B": _point_label("B", B, DOWN, ink),
        "F": _point_label("F", F, DOWN + LEFT * 0.2, ink),
        # ── Intersections (offsets tuned by eye) ────────────────────────────
        "G": _point_label("G", G, RIGHT, ink),
        "H": _point_label("H", H, UP + LEFT * (-0.03), ink, buff=0.12),
    }


def _layout(lines: VGroup, labels: VGroup) -> VGroup:
    diagram = VGroup(lines, labels)
    diagram.scale_to_fit_height(config.frame_height * FIT_HEIGHT)
    diagram.move_to(ORIGIN)
    return diagram


def _midpoint(p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
    return (p1 + p2) / 2


def _ratio_along(p_start: np.ndarray, p_end: np.ndarray, p_on: np.ndarray) -> float:
    """Unit-interval position of p_on on the collinear segment p_start→p_end."""
    vec = p_end - p_start
    denom = float(np.dot(vec[:2], vec[:2]))
    if denom < 1e-12:
        return 0.0
    return float(np.dot((p_on - p_start)[:2], vec[:2]) / denom)


def _laid_out_point_on_line(
    line: Line,
    pt: np.ndarray,
    anchor_start: np.ndarray,
    anchor_end: np.ndarray,
) -> np.ndarray:
    """Map a reference point onto an already scaled Line mobject."""
    t = _ratio_along(anchor_start, anchor_end, pt)
    p_start = line.get_start()
    p_end = line.get_end()
    return p_start + (p_end - p_start) * t


def _laid_out_vertices(lines: dict[str, Line]) -> dict[str, np.ndarray]:
    """Vertex positions after scale-to-fit (use for arcs and arrows)."""
    top = lines["top_DA"]
    bot = lines["bottom_CF"]
    return {
        "D": top.get_start().copy(),
        "A": top.get_end().copy(),
        "C": bot.get_start().copy(),
        "F": bot.get_end().copy(),
        "E": _laid_out_point_on_line(top, E, D, A),
        "B": _laid_out_point_on_line(bot, B, C, F),
        "G": lines["seg_CG"].get_end().copy(),
    }


def _parallel_arrow_mark(
    p_from: np.ndarray,
    p_to: np.ndarray,
    ink: ManimColor = DRAW_INK,
    size: float = PARALLEL_ARROW_SIZE,
    stroke_width: float = PARALLEL_ARROW_STROKE,
) -> VGroup:
    """Chevron on segment midpoint — tip sits on the line at the exact centre."""
    mid = (p_from + p_to) / 2
    d = p_to - p_from
    d = d / np.linalg.norm(d)
    perp = np.array([-d[1], d[0], 0.0])
    tip = mid
    wing = size * 0.30
    heel = mid - d * size * 0.50
    return VGroup(
        Line(heel + perp * wing, tip, color=ink, stroke_width=stroke_width),
        Line(heel - perp * wing, tip, color=ink, stroke_width=stroke_width),
    )


def _chevron_toward(
    at: np.ndarray,
    toward: np.ndarray,
    ink: ManimColor = DRAW_INK,
    size: float = PARALLEL_ARROW_SIZE,
    stroke_width: float = PARALLEL_ARROW_STROKE,
) -> VGroup:
    """Chevron with tip at `at`, opening toward `toward`."""
    d = toward - at
    d = d / np.linalg.norm(d)
    perp = np.array([-d[1], d[0], 0.0])
    wing = size * 0.30
    heel = at - d * size * 0.50
    return VGroup(
        Line(heel + perp * wing, at, color=ink, stroke_width=stroke_width),
        Line(heel - perp * wing, at, color=ink, stroke_width=stroke_width),
    )


def _double_parallel_arrow_mark(
    tip_at: np.ndarray,
    tail_at: np.ndarray,
    ink: ManimColor = DRAW_INK,
    size: float = PARALLEL_ARROW_SIZE,
    stroke_width: float = PARALLEL_ARROW_STROKE,
) -> VGroup:
    """Pair of chevrons on a segment; both tips point toward `tip_at`."""
    span = tail_at - tip_at
    dist = float(np.linalg.norm(span))
    if dist < 1e-9:
        return VGroup()
    d_hat = span / dist
    pos1 = tip_at + d_hat * (dist * DOUBLE_PARALLEL_ARROW_FRAC_1)
    pos2 = tip_at + d_hat * (dist * DOUBLE_PARALLEL_ARROW_FRAC_2)
    return VGroup(
        _chevron_toward(pos1, tip_at, ink, size, stroke_width),
        _chevron_toward(pos2, tip_at, ink, size, stroke_width),
    )


def _double_parallel_arrow_mark_matched_pair(
    tip_primary: np.ndarray,
    tail_primary: np.ndarray,
    tip_parallel: np.ndarray,
    tail_parallel: np.ndarray,
    ink: ManimColor = DRAW_INK,
    size: float = PARALLEL_ARROW_SIZE,
    stroke_width: float = PARALLEL_ARROW_STROKE,
) -> tuple[VGroup, VGroup]:
    """Double // on two parallel segments; copy uses same tip-ward distances and gap."""
    span_p = tail_primary - tip_primary
    dist_p = float(np.linalg.norm(span_p))
    if dist_p < 1e-9:
        empty = VGroup()
        return empty, empty
    d_hat_p = span_p / dist_p
    d1 = dist_p * DOUBLE_PARALLEL_ARROW_FRAC_1
    d2 = dist_p * DOUBLE_PARALLEL_ARROW_FRAC_2
    arr_primary = VGroup(
        _chevron_toward(tip_primary + d_hat_p * d1, tip_primary, ink, size, stroke_width),
        _chevron_toward(tip_primary + d_hat_p * d2, tip_primary, ink, size, stroke_width),
    )
    span_q = tail_parallel - tip_parallel
    dist_q = float(np.linalg.norm(span_q))
    if dist_q < 1e-9:
        return arr_primary, VGroup()
    d_hat_q = span_q / dist_q
    arr_parallel = VGroup(
        _chevron_toward(tip_parallel + d_hat_q * d1, tip_parallel, ink, size, stroke_width),
        _chevron_toward(tip_parallel + d_hat_q * d2, tip_parallel, ink, size, stroke_width),
    )
    return arr_primary, arr_parallel


def _filled_quad(
    p1: np.ndarray,
    p2: np.ndarray,
    p3: np.ndarray,
    p4: np.ndarray,
    color: ManimColor,
    fill_opacity: float = REGION_FILL_OPACITY,
) -> Polygon:
    """Filled quadrilateral behind diagram ink."""
    quad = Polygon(
        p1, p2, p3, p4,
        fill_color=color,
        fill_opacity=fill_opacity,
        stroke_width=0,
    )
    quad.set_z_index(-1)
    return quad


def _interior_angle_fill(
    vertex: np.ndarray,
    p1: np.ndarray,
    p2: np.ndarray,
    inside_point: np.ndarray,
    color: ManimColor,
    radius: float = ANGLE_RADIUS,
    fill_opacity: float = ANGLE_FILL_OPACITY,
    stroke_width: float = ANGLE_STROKE,
) -> VGroup:
    """Filled interior wedge + matching outline arc."""
    arc = s.interior_angle_arc(
        vertex, p1, p2, inside_point,
        radius=radius, color=color, stroke_width=stroke_width,
    )
    wedge_pts = np.vstack([vertex.reshape(1, 3), arc.points, vertex.reshape(1, 3)])
    wedge = VMobject(
        stroke_width=0,
        fill_color=color,
        fill_opacity=fill_opacity,
    )
    wedge.set_points_as_corners(wedge_pts)
    return VGroup(wedge, arc)


def _filled_triangle(
    p1: np.ndarray,
    p2: np.ndarray,
    p3: np.ndarray,
    color: ManimColor,
    fill_opacity: float = REGION_FILL_OPACITY,
) -> Polygon:
    """Filled triangle behind diagram ink (z_index below lines)."""
    tri = Polygon(
        p1, p2, p3,
        fill_color=color,
        fill_opacity=fill_opacity,
        stroke_width=0,
    )
    tri.set_z_index(-1)
    return tri


def _foot_to_horizontal(from_pt: np.ndarray, y_level: float) -> np.ndarray:
    """Foot of the vertical drop/rise from from_pt to the horizontal y = y_level."""
    return np.array([from_pt[0], y_level, 0.0])


def _dashed_horizontal(
    y_level: float,
    x_left: float,
    x_right: float,
    ink: ManimColor = DRAW_INK,
) -> DashedLine:
    """Horizontal dashed reference line at fixed y."""
    return DashedLine(
        np.array([x_left, y_level, 0.0]),
        np.array([x_right, y_level, 0.0]),
        color=ink,
        dash_length=HEIGHT_DASH_LENGTH,
        stroke_width=STROKE,
    )


def _altitude_seg(
    from_pt: np.ndarray,
    to_pt: np.ndarray,
    color: ManimColor,
    stroke_width: float = HIGHLIGHT_STROKE,
) -> Line:
    """Coloured altitude segment drawn above diagram fills."""
    seg = Line(from_pt, to_pt, color=color, stroke_width=stroke_width)
    seg.set_z_index(2)
    return seg


def _gcb_altitude_dash(
    tri_gcb: Polygon,
    buff: float = HEIGHT_DASH_BUFF,
) -> DashedLine:
    """Horizontal dashed reference for △GCB altitude (spans triangle + buff)."""
    verts = tri_gcb.get_vertices()
    g_v, c_v, b_v = verts[0], verts[1], verts[2]
    foot = _foot_to_horizontal(b_v, g_v[1])
    x_lo = min(foot[0], g_v[0], c_v[0]) - buff
    x_hi = max(foot[0], g_v[0], c_v[0]) + buff
    dash = _dashed_horizontal(g_v[1], x_lo, x_hi)
    dash.set_z_index(2)
    return dash


def _triangle_outline(
    p1: np.ndarray,
    p2: np.ndarray,
    p3: np.ndarray,
    ink: ManimColor = DRAW_INK,
    stroke_width: float = STROKE,
) -> Polygon:
    """Unfilled triangle on top of diagram ink."""
    tri = Polygon(
        p1, p2, p3,
        color=ink,
        stroke_width=stroke_width,
        fill_opacity=0,
    )
    tri.set_z_index(1)
    return tri


def _comparison_shift_grounded(
    guest: Mobject,
    anchor: Mobject,
    gap: float = 0.42,
) -> np.ndarray:
    """Shift guest left of anchor with both sharing the same bottom y (ground)."""
    a_verts = anchor.get_vertices()
    g_verts = guest.get_vertices()
    ground_y = min(p[1] for p in a_verts)
    g_bottom = min(p[1] for p in g_verts)
    dy = ground_y - g_bottom
    anchor_left = min(p[0] for p in a_verts)
    guest_right = max(p[0] for p in g_verts)
    dx = (anchor_left - gap) - guest_right
    return np.array([dx, dy, 0.0])


def _laid_out_subsegment(
    parallel_line: Line,
    pt_from: np.ndarray,
    pt_to: np.ndarray,
    anchor_start: np.ndarray,
    anchor_end: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Map reference sub-segment onto the already scaled parallel Line mobject.

    Highlights and k-labels must use these endpoints so they sit exactly on
    the white ink (base diagram is scale-to-fit; raw D/E/C… coords are not).
    """
    t0 = _ratio_along(anchor_start, anchor_end, pt_from)
    t1 = _ratio_along(anchor_start, anchor_end, pt_to)
    p_start = parallel_line.get_start()
    p_end = parallel_line.get_end()
    return p_start + (p_end - p_start) * t0, p_start + (p_end - p_start) * t1


def _highlight_seg(
    p1: np.ndarray,
    p2: np.ndarray,
    color: ManimColor,
    stroke_width: float = HIGHLIGHT_STROKE,
) -> Line:
    """Coloured overlay on a sub-segment (drawn above base ink)."""
    return Line(p1, p2, color=color, stroke_width=stroke_width)


def _length_label(
    tex: str,
    p1: np.ndarray,
    p2: np.ndarray,
    direction: np.ndarray,
    ink: ManimColor = DRAW_INK,
    buff: float = LABEL_BUFF,
) -> MathTex:
    """Algebra label at horizontal midpoint of segment p1–p2."""
    mid = _midpoint(p1, p2)
    label = MathTex(tex, color=ink, font_size=LENGTH_FONT)
    label.next_to(mid, direction, buff=buff)
    return label


def _dist_point_to_segment(p: np.ndarray, v0: np.ndarray, v1: np.ndarray) -> float:
    edge = v1 - v0
    denom = float(np.dot(edge[:2], edge[:2]))
    if denom < 1e-12:
        return float(np.linalg.norm((p - v0)[:2]))
    t = float(np.dot((p - v0)[:2], edge[:2]) / denom)
    t = max(0.0, min(1.0, t))
    closest = v0 + t * edge
    return float(np.linalg.norm((p - closest)[:2]))


def _triangle_inradius(tri: Polygon) -> float:
    """Centre-to-nearest-edge distance (inscribed-circle radius estimate)."""
    verts = tri.get_vertices()
    c = tri.get_center()
    return min(
        _dist_point_to_segment(c, verts[i], verts[(i + 1) % 3])
        for i in range(3)
    )


def _area_label_in_triangle(
    tri: Polygon,
    tex: str,
    color: ManimColor = DRAW_INK,
    fill_frac: float = AREA_LABEL_FILL,
    shift: np.ndarray | None = None,
    min_height: float = AREA_LABEL_MIN_HEIGHT,
) -> MathTex:
    """Area label scaled to fit inside triangle without hitting edges."""
    label = MathTex(tex, color=color, font_size=AREA_FONT)
    ir = _triangle_inradius(tri)
    max_h = max(ir * 2.0 * fill_frac, min_height)
    if label.height > max_h:
        label.scale_to_fit_height(max_h)
    elif label.height < min_height:
        label.scale_to_fit_height(min_height)
    verts = tri.get_vertices()
    span = max(float(np.linalg.norm(verts[i][:2] - verts[j][:2]))
               for i in range(3) for j in range(i + 1, 3))
    max_w = span * 0.72
    if label.width > max_w:
        label.scale_to_fit_width(max_w)
    label.move_to(tri.get_center())
    if shift is not None:
        label.shift(shift)
    return label


def _tri_x_span_at_y(tri: Polygon, y: float) -> tuple[float, float] | None:
    """Left/right x where horizontal line y meets the triangle boundary."""
    verts = tri.get_vertices()
    xs: list[float] = []
    for i in range(3):
        p1, p2 = verts[i], verts[(i + 1) % 3]
        y1, y2 = float(p1[1]), float(p2[1])
        if abs(y2 - y1) < 1e-9:
            if abs(y - y1) < 1e-9:
                xs.extend([float(p1[0]), float(p2[0])])
            continue
        y_lo, y_hi = min(y1, y2), max(y1, y2)
        if y < y_lo - 1e-9 or y > y_hi + 1e-9:
            continue
        t = (y - y1) / (y2 - y1)
        xs.append(float(p1[0] + t * (p2[0] - p1[0])))
    if len(xs) < 2:
        return None
    return min(xs), max(xs)


def _area_label_inside_at_y(
    ref: MathTex,
    tri: Polygon,
    tex: str,
    x_frac: float = 0.5,
    ink: ManimColor = DRAW_INK,
) -> MathTex:
    """Area label: match ref height; place inside tri at ref y, x_frac from left span."""
    label = MathTex(tex, color=ink, font_size=AREA_FONT)
    label.match_height(ref)
    y = float(ref.get_center()[1])
    span = _tri_x_span_at_y(tri, y)
    if span is not None:
        x_lo, x_hi = span
        x = x_lo + (x_hi - x_lo) * x_frac
    else:
        verts = tri.get_vertices()
        x_lo = min(float(v[0]) for v in verts)
        x_hi = max(float(v[0]) for v in verts)
        x = x_lo + (x_hi - x_lo) * x_frac
    label.move_to(np.array([x, y, 0.0]))
    return label


def _area_label_matched_inside_tri(
    ref: MathTex,
    tri: Polygon,
    tex: str,
    x_frac: float = 0.5,
    y_frac: float = 0.5,
    ink: ManimColor = DRAW_INK,
) -> MathTex:
    """Match ref height; place inside tri using local vertical slice (not ref y)."""
    label = MathTex(tex, color=ink, font_size=AREA_FONT)
    label.match_height(ref)
    verts = tri.get_vertices()
    y_lo = min(float(v[1]) for v in verts)
    y_hi = max(float(v[1]) for v in verts)
    y = y_lo + (y_hi - y_lo) * y_frac
    span = _tri_x_span_at_y(tri, y)
    if span is None:
        label.move_to(tri.get_center())
        return label
    x_lo, x_hi = span
    pad = label.width * 0.52
    usable_lo = x_lo + pad
    usable_hi = x_hi - pad
    if usable_hi <= usable_lo:
        label.move_to(np.array([(x_lo + x_hi) / 2, y, 0.0]))
        return label
    x = usable_lo + (usable_hi - usable_lo) * x_frac
    label.move_to(np.array([x, y, 0.0]))
    return label


def _de_bf_parallel_end_frame(
    scene: Scene,
    lines: dict[str, Line],
    labels: dict[str, Tex],
) -> dict[str, Mobject | np.ndarray]:
    """Static frame matching `ParallelLinesDeBfParallelDraw` step 7 end."""
    v = _laid_out_vertices(lines)
    top_da = lines["top_DA"]
    bot_cf = lines["bottom_CF"]
    de_p1, de_p2 = _laid_out_subsegment(top_da, D, E, D, A)
    bf_p1, bf_p2 = _laid_out_subsegment(bot_cf, B, F, C, F)
    db = lines["diag_DB"]
    ef = lines["seg_EF"]
    h_pt = _line_intersection(
        db.get_start(), db.get_end(),
        lines["seg_CG"].get_start(), lines["seg_CG"].get_end(),
    )
    arr_de = _parallel_arrow_mark(de_p1, de_p2, ink=DRAW_INK)
    arr_bf = _parallel_arrow_mark(bf_p1, bf_p2, ink=DRAW_INK)
    hi_de = _highlight_seg(de_p1, de_p2, COL_DE)
    lbl_de = _length_label(r"5k", de_p1, de_p2, UP, ink=COL_DE)
    hi_bf = _highlight_seg(bf_p1, bf_p2, COL_BF)
    lbl_bf = _length_label(r"5k", bf_p1, bf_p2, DOWN, ink=COL_BF)
    quad_debf = _filled_quad(v["D"], v["E"], v["F"], v["B"], COL_DEBF)
    arr_db = _double_parallel_arrow_mark(db.get_start(), db.get_end())
    arr_ef = _double_parallel_arrow_mark(ef.get_start(), ef.get_end())
    for mob in (arr_de, arr_bf, hi_de, lbl_de, hi_bf, lbl_bf, arr_db, arr_ef):
        mob.set_z_index(2)
    lbl_de.set_z_index(3)
    lbl_bf.set_z_index(3)
    scene.add(quad_debf)
    scene.bring_to_back(quad_debf)
    scene.add(arr_de, arr_bf, hi_de, lbl_de, hi_bf, lbl_bf, arr_db, arr_ef)
    return {
        "v": v,
        "h_pt": h_pt,
        "quad_debf": quad_debf,
        "arr_de": arr_de,
        "arr_bf": arr_bf,
        "arr_db": arr_db,
        "arr_ef": arr_ef,
        "hi_de": hi_de,
        "lbl_de": lbl_de,
        "hi_bf": hi_bf,
        "lbl_bf": lbl_bf,
    }


def _build_cgb_angle_arcs(
    v: dict[str, np.ndarray],
    h_pt: np.ndarray,
    ang_r: float = CGB_ANGLE_RADIUS,
) -> dict[str, VGroup]:
    """Five interior angle marks for CgbAngleMarks / end-frame."""
    inside_cgf = (v["C"] + v["G"] + v["F"]) / 3
    inside_chb = (v["C"] + h_pt + v["B"]) / 3
    inside_cfg = (v["C"] + v["F"] + v["G"]) / 3
    inside_cbh = (v["C"] + v["B"] + h_pt) / 3
    inside_gcb = (v["G"] + v["C"] + v["B"]) / 3
    return {
        "cgf": _interior_angle_fill(
            v["G"], v["C"], v["F"], inside_cgf, COL_CGB_CHB, radius=ang_r,
        ),
        "chb": _interior_angle_fill(
            h_pt, v["C"], v["B"], inside_chb, COL_CGB_CHB, radius=ang_r,
        ),
        "cfg": _interior_angle_fill(
            v["F"], v["C"], v["G"], inside_cfg, COL_CFG_CBH, radius=ang_r,
        ),
        "cbh": _interior_angle_fill(
            v["B"], v["C"], h_pt, inside_cbh, COL_CFG_CBH, radius=ang_r,
        ),
        "gcb": _interior_angle_fill(
            v["C"], v["G"], v["B"], inside_gcb, COL_GCB_ANGLE, radius=ang_r,
        ),
    }


def _cgb_isolate_chb_cgf_ink(
    scene: Slide,
    lines: dict[str, Line],
    labels: dict[str, Tex],
    v: dict,
    h_pt: np.ndarray,
    rt: float = 0.28,
) -> None:
    """Drop labels/lines outside △CHB and △CGF (CD, DE, DH, EG, AE, AG, …)."""
    for key in ("D", "E", "A"):
        _remove(scene, labels[key])
    _remove(scene, lines["left_DC"])
    _remove(scene, lines["top_DA"])
    g_pt = v["G"].copy()
    lines["diag_DB"].put_start_and_end_on(h_pt.copy(), lines["diag_DB"].get_end())
    lines["seg_EF"].put_start_and_end_on(g_pt, lines["seg_EF"].get_end())
    lines["right_AB"].put_start_and_end_on(g_pt, lines["right_AB"].get_end())


def _cgb_angle_marks_end_frame(
    scene: Scene,
    lines: dict[str, Line],
    labels: dict[str, Tex],
    ang_r: float = CGB_ANGLE_RADIUS,
) -> dict[str, Mobject | np.ndarray | VGroup]:
    """Static frame matching `ParallelLinesCgbAngleMarksDraw` step 7 end."""
    v = _laid_out_vertices(lines)
    h_pt = _line_intersection(
        lines["diag_DB"].get_start(), lines["diag_DB"].get_end(),
        lines["seg_CG"].get_start(), lines["seg_CG"].get_end(),
    )
    g_pt = lines["seg_CG"].get_end().copy()
    lines["diag_DB"].put_start_and_end_on(h_pt.copy(), lines["diag_DB"].get_end())
    lines["seg_EF"].put_start_and_end_on(g_pt, lines["seg_EF"].get_end())
    lines["right_AB"].put_start_and_end_on(g_pt, lines["right_AB"].get_end())
    for key in ("D", "E", "A"):
        labels[key].set_opacity(0)
    for key in ("top_DA", "left_DC"):
        lines[key].set_opacity(0)
    arcs = _build_cgb_angle_arcs(v, h_pt, ang_r)
    for group in arcs.values():
        for mob in group:
            mob.set_z_index(2)
        scene.add(*group)
    return {"v": v, "h_pt": h_pt, **arcs}


# ══════════════════════════════════════════════════════════════════════════════
# CHB deck helpers (ParallelLinesChb* scenes)
#
# End-frame chain (each step-0 calls the previous scene's end helper):
#   _cgb_angle_marks_end_frame
#     → _chb_lift_end_frame → _chb_regions_end_frame → _chb_regions_cont_end_frame
#     → _chb_hbg_restore_end_frame → _chb_hbg_marks_end_frame
#     → _chb_hbg_k_regions_end_frame → _chb_hbg_k_trim_end_frame
#     → _chb_hbg_k_cdh_only_end_frame  (final slide)
# Map: `docs/CHB_DECK_CHAIN.md`
# ══════════════════════════════════════════════════════════════════════════════


def _chb_lift_amount(
    chb_dup: VGroup, v: dict[str, np.ndarray], h_pt: np.ndarray,
) -> float:
    """Lift △CHB well above lower ink; stay inside the frame."""
    dup_bottom = float(chb_dup.get_bottom()[1])
    dup_top = float(chb_dup.get_top()[1])
    frame_top = float(config.frame_height / 2 - 0.10)
    lower_roof = max(float(v["G"][1]), float(h_pt[1])) + CHB_LIFT_CLEAR
    lift = max(CHB_LIFT_GAP, lower_roof - dup_bottom) + CHB_LIFT_EXTRA
    max_lift = frame_top - dup_top - 0.08
    return min(lift, max_lift)


def _chb_triangle_copy(
    labels: dict[str, Tex],
    v: dict[str, np.ndarray],
    h_pt: np.ndarray,
    ink: ManimColor = DRAW_INK,
) -> VGroup:
    """Duplicate △CHB ink + labels C/H/B + arcs GCB, CHB, CBH."""
    c_pt = v["C"].copy()
    h_pt_d = np.array(h_pt, dtype=float).copy()
    b_pt = v["B"].copy()
    seg_ch = Line(c_pt, h_pt_d, color=ink, stroke_width=STROKE)
    seg_hb = Line(h_pt_d, b_pt, color=ink, stroke_width=STROKE)
    seg_cb = Line(c_pt, b_pt, color=ink, stroke_width=STROKE)
    lbl_c = _label_like_orig("C", c_pt, labels["C"], v["C"], ink)
    lbl_h = _label_like_orig("H", h_pt_d, labels["H"], h_pt, ink)
    lbl_b = _label_like_orig("B", b_pt, labels["B"], v["B"], ink)
    inside_gcb = (v["G"] + c_pt + b_pt) / 3
    inside_chb = (c_pt + h_pt_d + b_pt) / 3
    inside_cbh = (c_pt + b_pt + h_pt_d) / 3
    dup_gcb = _interior_angle_fill(
        c_pt, v["G"], b_pt, inside_gcb, COL_GCB_ANGLE, radius=CGB_ANGLE_RADIUS,
    )
    dup_chb = _interior_angle_fill(
        h_pt_d, c_pt, b_pt, inside_chb, COL_CGB_CHB, radius=CGB_ANGLE_RADIUS,
    )
    dup_cbh = _interior_angle_fill(
        b_pt, c_pt, h_pt_d, inside_cbh, COL_CFG_CBH, radius=CGB_ANGLE_RADIUS,
    )
    body = VGroup(
        seg_ch, seg_hb, seg_cb,
        lbl_c, lbl_h, lbl_b,
        dup_gcb, dup_chb, dup_cbh,
    )
    for mob in (seg_ch, seg_hb, seg_cb):
        mob.set_z_index(2)
    for group in (dup_gcb, dup_chb, dup_cbh):
        for mob in group:
            mob.set_z_index(2)
    for lbl in (lbl_c, lbl_h, lbl_b):
        lbl.set_z_index(3)
    return body


# Indices inside `_chb_triangle_copy` VGroup (seg_ch, seg_hb, seg_cb, labels…, arcs…)
CHB_DUP_SEG_CH = 0
CHB_DUP_SEG_HB = 1
CHB_DUP_SEG_CB = 2
CHB_DUP_ANG_GCB = 6
CHB_DUP_ANG_CHB = 7
CHB_DUP_ANG_CBH = 8
CHB_DUP_LBL_C = 3
CHB_DUP_LBL_H = 4
CHB_DUP_LBL_B = 5


def _chb_dup_angle_mobs(
    chb_dup: VGroup,
    *,
    include_gcb: bool = True,
) -> list[Mobject]:
    """Wedge + arc mobjects on the lifted △HCB duplicate."""
    idxs = [CHB_DUP_ANG_CHB, CHB_DUP_ANG_CBH]
    if include_gcb:
        idxs.insert(0, CHB_DUP_ANG_GCB)
    mobs: list[Mobject] = []
    for idx in idxs:
        for mob in chb_dup[idx]:  # type: ignore[index]
            mobs.append(mob)
    return mobs


def _angle_group_mobs(group: VGroup) -> list[Mobject]:
    """Flatten a two-mob angle VGroup (wedge + arc)."""
    return [mob for mob in group]


def _chb_lift_end_frame(
    scene: Scene,
    lines: dict[str, Line],
    labels: dict[str, Tex],
    ang_r: float = CGB_ANGLE_RADIUS,
) -> dict[str, Mobject | np.ndarray | float | VGroup | Line]:
    """Static frame matching `ParallelLinesCgbAngleMarksDraw` step 9 end
    (also `ParallelLinesChbLiftDraw` step 2 end)."""
    frame = _cgb_angle_marks_end_frame(scene, lines, labels, ang_r)
    v = frame["v"]
    h_pt = frame["h_pt"]
    chb_dup = _chb_triangle_copy(labels, v, h_pt)
    lift = _chb_lift_amount(chb_dup, v, h_pt)
    chb_dup.shift(UP * lift)
    scene.add(chb_dup)
    lines["diag_DB"].set_opacity(0)
    labels["H"].set_opacity(0)
    for mob in frame["chb"]:
        mob.set_opacity(0)
    for mob in frame["cbh"]:
        mob.set_opacity(0)
    h_pt_lift = np.array(h_pt, dtype=float) + UP * lift
    seg_cb_dup: Line = chb_dup[CHB_DUP_SEG_CB]  # type: ignore[assignment]
    return {
        "v": v,
        "h_pt": h_pt,
        "h_pt_lift": h_pt_lift,
        "lift": lift,
        "chb_dup": chb_dup,
        "ang_gcb": frame["gcb"],
        "ang_cgf": frame["cgf"],
        "ang_cfg": frame["cfg"],
        "seg_cb_dup": seg_cb_dup,
    }


def _build_chb_regions_k_highlights(
    v: dict[str, np.ndarray],
    seg_cb_dup: Line,
) -> dict[str, Line | MathTex]:
    """Step 1–2 mobjects: both **CB** (blue + 7k) and **BF** (yellow + 5k)."""
    cb_low_p1, cb_low_p2 = v["C"].copy(), v["B"].copy()
    cb_lift_p1 = seg_cb_dup.get_start().copy()
    cb_lift_p2 = seg_cb_dup.get_end().copy()
    bf_p1, bf_p2 = v["B"].copy(), v["F"].copy()
    hi_cb_low = _highlight_seg(cb_low_p1, cb_low_p2, COL_CB)
    hi_cb_lift = _highlight_seg(cb_lift_p1, cb_lift_p2, COL_CB)
    lbl_7k_low = _length_label(r"7k", cb_low_p1, cb_low_p2, DOWN, ink=COL_CB)
    lbl_7k_lift = _length_label(r"7k", cb_lift_p1, cb_lift_p2, DOWN, ink=COL_CB)
    hi_bf = _highlight_seg(bf_p1, bf_p2, COL_BF)
    lbl_5k_bf = _length_label(r"5k", bf_p1, bf_p2, DOWN, ink=COL_BF)
    for mob in (hi_cb_low, hi_cb_lift, hi_bf):
        mob.set_z_index(2)
    for mob in (lbl_7k_low, lbl_7k_lift, lbl_5k_bf):
        mob.set_z_index(3)
    return {
        "cb_low_p1": cb_low_p1,
        "cb_low_p2": cb_low_p2,
        "cb_lift_p1": cb_lift_p1,
        "cb_lift_p2": cb_lift_p2,
        "hi_cb_low": hi_cb_low,
        "hi_cb_lift": hi_cb_lift,
        "lbl_7k_low": lbl_7k_low,
        "lbl_7k_lift": lbl_7k_lift,
        "hi_bf": hi_bf,
        "lbl_5k_bf": lbl_5k_bf,
    }


def _build_chb_regions_fills_and_areas(
    v: dict[str, np.ndarray],
    h_pt_lift: np.ndarray,
    cb_lift_p1: np.ndarray,
    cb_lift_p2: np.ndarray,
) -> dict[str, Polygon | MathTex]:
    """Step 3 mobjects: △**GCB**, △**GBF**, lifted △**HCB** + area labels."""
    tri_gcb = _filled_triangle(v["G"], v["C"], v["B"], COL_TRI_GCB)
    tri_gbf = _filled_triangle(v["G"], v["B"], v["F"], COL_TRI_GBF)
    tri_hcb = _filled_triangle(h_pt_lift, cb_lift_p1, cb_lift_p2, COL_TRI_HCB)
    area_gbf = _area_label_in_triangle(
        tri_gbf,
        r"\mathbf{300\ \mathrm{cm}^{2}}",
        color=DRAW_INK,
        shift=LEFT * AREA_GBF_H_SHIFT,
    )
    area_gcb = _area_label_inside_at_y(
        area_gbf,
        tri_gcb,
        r"\mathbf{420\ \mathrm{cm}^{2}}",
        x_frac=AREA_GCB_AREA_X_FRAC,
    )
    area_hcb = _area_label_matched_inside_tri(
        area_gbf,
        tri_hcb,
        r"\mathbf{245\ \mathrm{cm}^{2}}",
        x_frac=AREA_HCB_X_FRAC,
        y_frac=AREA_HCB_Y_FRAC,
    )
    for lbl in (area_gbf, area_gcb, area_hcb):
        lbl.set_z_index(5)
    return {
        "tri_gcb": tri_gcb,
        "tri_gbf": tri_gbf,
        "tri_hcb": tri_hcb,
        "area_gbf": area_gbf,
        "area_gcb": area_gcb,
        "area_hcb": area_hcb,
    }


def _chb_regions_end_frame(
    scene: Scene,
    lines: dict[str, Line],
    labels: dict[str, Tex],
    ang_r: float = CGB_ANGLE_RADIUS,
) -> dict[str, Mobject | np.ndarray | float | VGroup | Line | Polygon | MathTex]:
    """Static frame matching `ParallelLinesChbRegionsDraw` step 3 end."""
    lift_frame = _chb_lift_end_frame(scene, lines, labels, ang_r)
    v = lift_frame["v"]
    seg_cb_dup: Line = lift_frame["seg_cb_dup"]  # type: ignore[assignment]
    h_pt_lift = lift_frame["h_pt_lift"]
    k_mobs = _build_chb_regions_k_highlights(v, seg_cb_dup)
    fill_mobs = _build_chb_regions_fills_and_areas(
        v, h_pt_lift, k_mobs["cb_lift_p1"], k_mobs["cb_lift_p2"],
    )
    scene.add(
        fill_mobs["tri_gcb"],
        fill_mobs["tri_gbf"],
        fill_mobs["tri_hcb"],
    )
    scene.bring_to_back(
        fill_mobs["tri_gcb"],
        fill_mobs["tri_gbf"],
        fill_mobs["tri_hcb"],
    )
    scene.add(
        k_mobs["hi_cb_low"],
        k_mobs["hi_cb_lift"],
        k_mobs["lbl_7k_low"],
        k_mobs["lbl_7k_lift"],
        k_mobs["hi_bf"],
        k_mobs["lbl_5k_bf"],
        fill_mobs["area_gbf"],
        fill_mobs["area_gcb"],
        fill_mobs["area_hcb"],
    )
    return {**lift_frame, **k_mobs, **fill_mobs}


def _build_chb_hbg_final_mobs(
    v: dict[str, np.ndarray],
    h_pt: np.ndarray,
) -> dict[str, Polygon | MathTex]:
    """Red △**HBG** + **175 cm²** (ChbRegionsCont step 5)."""
    tri_hbg = _filled_triangle(h_pt, v["B"], v["G"], COL_TRI_HBG)
    area_hbg = _area_label_in_triangle(
        tri_hbg,
        r"\mathbf{175\ \mathrm{cm}^{2}}",
        color=DRAW_INK,
        shift=LEFT * AREA_HBG_H_SHIFT + UP * AREA_HBG_V_SHIFT,
    )
    area_hbg.set_z_index(5)
    return {"tri_hbg": tri_hbg, "area_hbg": area_hbg}


def _chb_regions_cont_end_frame(
    scene: Scene,
    lines: dict[str, Line],
    labels: dict[str, Tex],
    ang_r: float = CGB_ANGLE_RADIUS,
) -> dict[str, Mobject | np.ndarray | float | VGroup | Line | Polygon | MathTex]:
    """Static frame matching `ParallelLinesChbRegionsContDraw` step 5 end."""
    frame = _chb_regions_end_frame(scene, lines, labels, ang_r)
    v = frame["v"]
    h_pt = frame["h_pt"]
    lift = float(frame["lift"])
    chb_dup = frame["chb_dup"]

    for mob in _angle_group_mobs(frame["ang_cgf"]):  # type: ignore[arg-type]
        mob.set_opacity(0)
    for mob in _angle_group_mobs(frame["ang_cfg"]):  # type: ignore[arg-type]
        mob.set_opacity(0)
    for mob in _chb_dup_angle_mobs(chb_dup, include_gcb=False):
        mob.set_opacity(0)

    frame["tri_gbf"].set_opacity(0)
    frame["area_gbf"].set_opacity(0)

    chb_dup.shift(DOWN * lift)
    frame["hi_cb_lift"].shift(DOWN * lift)
    frame["lbl_7k_lift"].shift(DOWN * lift)
    frame["tri_hcb"].shift(DOWN * lift)
    frame["area_hcb"].shift(DOWN * lift)
    frame["hi_cb_lift"].set_opacity(0)
    frame["lbl_7k_lift"].set_opacity(0)
    frame["tri_hcb"].set_opacity(0)
    frame["area_hcb"].set_opacity(0)
    frame["tri_gcb"].set_opacity(0)
    frame["area_gcb"].set_opacity(0)

    hbg = _build_chb_hbg_final_mobs(v, h_pt)
    scene.add(hbg["tri_hbg"])
    scene.bring_to_back(hbg["tri_hbg"])
    scene.add(hbg["area_hbg"])

    return {**frame, **hbg}


def _restore_full_parallel_graph_ink(
    lines: dict[str, Line],
    labels: dict[str, Tex],
    v: dict[str, np.ndarray],
) -> None:
    """Reset all diagram ink + labels to the full scaled figure."""
    lines["top_DA"].put_start_and_end_on(v["D"].copy(), v["A"].copy())
    lines["top_DA"].set_opacity(1)
    lines["bottom_CF"].put_start_and_end_on(v["C"].copy(), v["F"].copy())
    lines["bottom_CF"].set_opacity(1)
    lines["left_DC"].put_start_and_end_on(v["C"].copy(), v["D"].copy())
    lines["left_DC"].set_opacity(1)
    lines["right_AB"].put_start_and_end_on(v["A"].copy(), v["B"].copy())
    lines["right_AB"].set_opacity(1)
    lines["diag_DB"].put_start_and_end_on(v["D"].copy(), v["B"].copy())
    lines["diag_DB"].set_opacity(1)
    lines["seg_EF"].put_start_and_end_on(v["E"].copy(), v["F"].copy())
    lines["seg_EF"].set_opacity(1)
    lines["seg_CG"].put_start_and_end_on(v["C"].copy(), v["G"].copy())
    lines["seg_CG"].set_opacity(1)
    for key in ("D", "E", "A", "F", "H"):
        labels[key].set_opacity(1)


def _build_parallel_graph_arrow_marks(
    lines: dict[str, Line],
    v: dict[str, np.ndarray],
) -> dict[str, Mobject]:
    """// marks on **DE**/**BF** and double // on **DB**/**EF** (no k-labels)."""
    top_da = lines["top_DA"]
    bot_cf = lines["bottom_CF"]
    de_p1, de_p2 = _laid_out_subsegment(top_da, D, E, D, A)
    bf_p1, bf_p2 = _laid_out_subsegment(bot_cf, B, F, C, F)
    db = lines["diag_DB"]
    ef = lines["seg_EF"]
    arr_de = _parallel_arrow_mark(de_p1, de_p2, ink=DRAW_INK)
    arr_bf = _parallel_arrow_mark(bf_p1, bf_p2, ink=DRAW_INK)
    arr_db = _double_parallel_arrow_mark(db.get_start(), db.get_end())
    arr_ef = _double_parallel_arrow_mark(ef.get_start(), ef.get_end())
    for mob in (arr_de, arr_bf, arr_db, arr_ef):
        mob.set_z_index(2)
    return {
        "arr_de": arr_de,
        "arr_bf": arr_bf,
        "arr_db": arr_db,
        "arr_ef": arr_ef,
    }


def _chb_hbg_restore_end_frame(
    scene: Scene,
    lines: dict[str, Line],
    labels: dict[str, Tex],
    ang_r: float = CGB_ANGLE_RADIUS,
) -> dict[str, Mobject | np.ndarray | float | VGroup | Line | Polygon | MathTex]:
    """Static frame matching `ParallelLinesChbHbgRestoreDraw` step 3 end."""
    frame = _chb_regions_cont_end_frame(scene, lines, labels, ang_r)
    v = frame["v"]
    chb_dup = frame["chb_dup"]

    for mob in _angle_group_mobs(frame["ang_gcb"]):  # type: ignore[arg-type]
        mob.set_opacity(0)
    for mob in _chb_dup_angle_mobs(chb_dup, include_gcb=True):
        mob.set_opacity(0)

    _restore_full_parallel_graph_ink(lines, labels, v)

    dup_lines = VGroup(
        chb_dup[CHB_DUP_SEG_CH],
        chb_dup[CHB_DUP_SEG_HB],
        chb_dup[CHB_DUP_SEG_CB],
    )
    dup_lbls = VGroup(
        chb_dup[CHB_DUP_LBL_C],
        chb_dup[CHB_DUP_LBL_H],
        chb_dup[CHB_DUP_LBL_B],
    )
    dup_lines.set_opacity(0)
    dup_lbls.set_opacity(0)

    arrows = _build_parallel_graph_arrow_marks(lines, v)
    scene.add(*arrows.values())

    return {**frame, **arrows}


def _build_chb_hbg_marks_arrow_marks(
    v: dict[str, np.ndarray],
) -> dict[str, Mobject]:
    """Revised // marks: matched double // on **CD** and **AB** (tips toward **D** / **A**)."""
    arr_cd, arr_ab = _double_parallel_arrow_mark_matched_pair(
        v["D"], v["C"], v["A"], v["B"],
    )
    for mob in (arr_cd, arr_ab):
        mob.set_z_index(2)
    return {"arr_cd": arr_cd, "arr_ab": arr_ab}


def _chb_hbg_marks_end_frame(
    scene: Scene,
    lines: dict[str, Line],
    labels: dict[str, Tex],
    ang_r: float = CGB_ANGLE_RADIUS,
) -> dict[str, Mobject | np.ndarray | float | VGroup | Line | Polygon | MathTex]:
    """Static frame matching `ParallelLinesChbHbgMarksDraw` step 6 end."""
    frame = _chb_hbg_restore_end_frame(scene, lines, labels, ang_r)
    v = frame["v"]
    h_pt = frame["h_pt"]

    for key in ("arr_bf", "arr_ef", "arr_db"):
        frame[key].set_opacity(0)
    frame["hi_cb_low"].set_opacity(0)
    frame["lbl_7k_low"].set_opacity(0)

    marks_arrows = _build_chb_hbg_marks_arrow_marks(v)
    scene.add(marks_arrows["arr_cd"], marks_arrows["arr_ab"])

    tri_cdh = _filled_triangle(v["C"], v["D"], h_pt, COL_TRI_CDH)
    scene.add(tri_cdh)
    scene.bring_to_back(tri_cdh)

    arcs = _build_chb_hbg_marks_angle_arcs(v, h_pt, ang_r)
    scene.add(*arcs.values())

    return {**frame, **marks_arrows, "tri_cdh": tri_cdh, **arcs}


def _build_chb_hbg_k_region_mobs(
    v: dict[str, np.ndarray],
) -> dict[str, Line | MathTex | Polygon]:
    """△**EAG**/**GBF** fills + highlighted **EA**/**AG**/**BF**/**BG**/**DC** + k labels."""
    tri_eag = _filled_triangle(v["E"], v["A"], v["G"], COL_TRI_EAG_K)
    tri_gbf = _filled_triangle(v["G"], v["B"], v["F"], COL_TRI_GBF)

    ea_p1, ea_p2 = v["E"].copy(), v["A"].copy()
    ag_p1, ag_p2 = v["A"].copy(), v["G"].copy()
    bf_p1, bf_p2 = v["B"].copy(), v["F"].copy()
    bg_p1, bg_p2 = v["B"].copy(), v["G"].copy()
    dc_p1, dc_p2 = v["D"].copy(), v["C"].copy()

    hi_ea = _highlight_seg(ea_p1, ea_p2, COL_EA)
    lbl_2k_ea = _length_label(r"2k", ea_p1, ea_p2, UP, ink=COL_EA)
    hi_ag = _highlight_seg(ag_p1, ag_p2, COL_EA)
    lbl_2k_ag = _length_label(r"2k", ag_p1, ag_p2, RIGHT, ink=COL_EA)

    hi_bf = _highlight_seg(bf_p1, bf_p2, COL_BF)
    lbl_5k_bf = _length_label(r"5k", bf_p1, bf_p2, DOWN, ink=COL_BF)
    hi_bg = _highlight_seg(bg_p1, bg_p2, COL_BF)
    lbl_5k_bg = _length_label(r"5k", bg_p1, bg_p2, RIGHT, ink=COL_BF)

    hi_dc = _highlight_seg(dc_p1, dc_p2, COL_DC)
    lbl_7k_dc = _length_label(r"7k", dc_p1, dc_p2, LEFT, ink=COL_DC)

    for mob in (hi_ea, hi_ag, hi_bf, hi_bg, hi_dc):
        mob.set_z_index(2)
    for mob in (lbl_2k_ea, lbl_2k_ag, lbl_5k_bf, lbl_5k_bg, lbl_7k_dc):
        mob.set_z_index(3)

    return {
        "tri_eag": tri_eag,
        "tri_gbf": tri_gbf,
        "hi_ea": hi_ea,
        "lbl_2k_ea": lbl_2k_ea,
        "hi_ag": hi_ag,
        "lbl_2k_ag": lbl_2k_ag,
        "hi_bf": hi_bf,
        "lbl_5k_bf": lbl_5k_bf,
        "hi_bg": hi_bg,
        "lbl_5k_bg": lbl_5k_bg,
        "hi_dc": hi_dc,
        "lbl_7k_dc": lbl_7k_dc,
    }


def _chb_hbg_k_regions_end_frame(
    scene: Scene,
    lines: dict[str, Line],
    labels: dict[str, Tex],
    ang_r: float = CGB_ANGLE_RADIUS,
) -> dict[str, Mobject | np.ndarray | float | VGroup | Line | Polygon | MathTex]:
    """Static frame matching `ParallelLinesChbHbgKRegionsDraw` step 4 end."""
    frame = _chb_hbg_marks_end_frame(scene, lines, labels, ang_r)
    v = frame["v"]
    k_mobs = _build_chb_hbg_k_region_mobs(v)  # type: ignore[arg-type]
    scene.add(k_mobs["tri_eag"], k_mobs["tri_gbf"])
    scene.bring_to_back(k_mobs["tri_eag"], k_mobs["tri_gbf"])
    scene.add(
        k_mobs["hi_ea"],
        k_mobs["lbl_2k_ea"],
        k_mobs["hi_ag"],
        k_mobs["lbl_2k_ag"],
        k_mobs["hi_bf"],
        k_mobs["lbl_5k_bf"],
        k_mobs["hi_bg"],
        k_mobs["lbl_5k_bg"],
        k_mobs["hi_dc"],
        k_mobs["lbl_7k_dc"],
    )
    return {**frame, **k_mobs}


def _chb_hbg_k_trim_end_frame(
    scene: Scene,
    lines: dict[str, Line],
    labels: dict[str, Tex],
    ang_r: float = CGB_ANGLE_RADIUS,
) -> dict[str, Mobject | np.ndarray | float | VGroup | Line | Polygon | MathTex]:
    """Static frame matching `ParallelLinesChbHbgKTrimDraw` step 2 end."""
    frame = _chb_hbg_k_regions_end_frame(scene, lines, labels, ang_r)
    for key in ("tri_eag", "hi_ea", "lbl_2k_ea", "hi_bf", "lbl_5k_bf", "tri_gbf"):
        frame[key].set_opacity(0)
    tri_cdh = frame["tri_cdh"]
    area_cdh = _area_label_in_triangle(
        tri_cdh,  # type: ignore[arg-type]
        r"\mathbf{343\ \mathrm{cm}^{2}}",
        shift=RIGHT * AREA_CDH_H_SHIFT,
    )
    area_cdh.set_z_index(5)
    scene.add(area_cdh)
    return {**frame, "area_cdh": area_cdh}


CDH_KEEP_LINE_KEYS = ("left_DC", "diag_DB", "seg_CG")


def _trim_cdh_triangle_ink(
    lines: dict[str, Line],
    v: dict[str, np.ndarray],
    h_pt: np.ndarray,
) -> None:
    """Trim ink to **DC**, **DH** (`diag_DB` D→H), **HC** (`seg_CG` C→H)."""
    lines["left_DC"].put_start_and_end_on(v["C"].copy(), v["D"].copy())
    lines["left_DC"].set_opacity(1)
    lines["diag_DB"].put_start_and_end_on(v["D"].copy(), h_pt.copy())
    lines["diag_DB"].set_opacity(1)
    lines["seg_CG"].put_start_and_end_on(v["C"].copy(), h_pt.copy())
    lines["seg_CG"].set_opacity(1)


def _chb_hbg_k_final_cleanup_mobs(
    frame: dict[str, Mobject | np.ndarray | float | VGroup | Line | Polygon | MathTex],
    lines: dict[str, Line],
    labels: dict[str, Tex],
) -> list[Mobject]:
    """Mobjects to drop for CDH-only frame (**D**, **H**, **C**, △**CDH**, **343 cm²**, **DC**/**DH**/**HC**)."""
    ang_keys = ("ang_cdb", "ang_gbh", "ang_dch", "ang_hgb", "ang_dhc", "ang_ghb")
    remove: list[Mobject] = [
        lines[k] for k in LINE_ORDER if k not in CDH_KEEP_LINE_KEYS
    ]
    for key in ("E", "A", "B", "F", "G"):
        remove.append(labels[key])
    for key in (
        "tri_hbg", "area_hbg",
        "arr_de", "arr_cd", "arr_ab",
        "hi_ag", "lbl_2k_ag", "hi_bg", "lbl_5k_bg", "hi_dc", "lbl_7k_dc",
    ):
        remove.append(frame[key])  # type: ignore[arg-type]
    for key in ang_keys:
        remove.extend(_angle_group_mobs(frame[key]))  # type: ignore[arg-type]
    return remove


def _chb_hbg_k_cdh_only_end_frame(
    scene: Scene,
    lines: dict[str, Line],
    labels: dict[str, Tex],
    ang_r: float = CGB_ANGLE_RADIUS,
) -> dict[str, Mobject | np.ndarray | float | VGroup | Line | Polygon | MathTex]:
    """Static frame matching `ParallelLinesChbHbgKTrimDraw` step 3 end (CDH-only)."""
    frame = _chb_hbg_k_trim_end_frame(scene, lines, labels, ang_r)
    v = frame["v"]
    h_pt = frame["h_pt"]
    _trim_cdh_triangle_ink(lines, v, h_pt)  # type: ignore[arg-type]
    for mob in _chb_hbg_k_final_cleanup_mobs(frame, lines, labels):
        mob.set_opacity(0)
    return frame


def _build_chb_hbg_marks_angle_arcs(
    v: dict[str, np.ndarray],
    h_pt: np.ndarray,
    ang_r: float = CGB_ANGLE_RADIUS,
) -> dict[str, VGroup]:
    """Six interior arcs in three colour-matched pairs (ChbHbgMarks)."""
    inside_cdh = (v["C"] + v["D"] + h_pt) / 3
    inside_hbg = (h_pt + v["G"] + v["B"]) / 3
    inside_dhc = (v["D"] + h_pt + v["C"]) / 3
    return {
        "ang_cdb": _interior_angle_fill(
            v["D"], v["C"], v["B"], inside_cdh, COL_ANGLE_CDB_GBH, radius=ang_r,
        ),
        "ang_gbh": _interior_angle_fill(
            v["B"], v["G"], h_pt, inside_hbg, COL_ANGLE_CDB_GBH, radius=ang_r,
        ),
        "ang_dch": _interior_angle_fill(
            v["C"], v["D"], h_pt, inside_cdh, COL_ANGLE_DCH_HGB, radius=ang_r,
        ),
        "ang_hgb": _interior_angle_fill(
            v["G"], h_pt, v["B"], inside_hbg, COL_ANGLE_DCH_HGB, radius=ang_r,
        ),
        "ang_dhc": _interior_angle_fill(
            h_pt, v["D"], v["C"], inside_dhc, COL_ANGLE_DHC_GHB, radius=ang_r,
        ),
        "ang_ghb": _interior_angle_fill(
            h_pt, v["G"], v["B"], inside_hbg, COL_ANGLE_DHC_GHB, radius=ang_r,
        ),
    }


def _add_base_diagram(
    scene: Scene, ink: ManimColor = DRAW_INK
) -> tuple[dict[str, Line], dict[str, Tex], VGroup]:
    """Full figure (lines + point labels), scaled — returns named mobs + VGroup."""
    lines = build_lines(ink)
    labels = build_labels(ink)
    line_mobs = [lines[k] for k in LINE_ORDER]
    label_mobs = [labels[k] for k in LABEL_ORDER]
    diagram = _layout(VGroup(*line_mobs), VGroup(*label_mobs))
    scene.add(diagram)
    return lines, labels, diagram


class ParallelLinesStill(Scene):
    """White-background still — all lines + labels at once."""

    def construct(self):
        self.camera.background_color = BG
        lines = build_lines(INK)
        labels = build_labels(INK)
        self.add(_layout(VGroup(*lines.values()), VGroup(*labels.values())))


class ParallelLinesDraw(Slide):
    """Black-background draw-out — one slide beat: lines then labels."""

    def construct(self):
        self.camera.background_color = DRAW_BG

        lines = build_lines(DRAW_INK)
        labels = build_labels(DRAW_INK)
        line_mobs = [lines[k] for k in LINE_ORDER]
        label_mobs = [labels[k] for k in LABEL_ORDER]
        _layout(VGroup(*line_mobs), VGroup(*label_mobs))

        self.play(
            LaggedStart(*[Create(m) for m in line_mobs], lag_ratio=0.12),
            run_time=1.4,
        )
        self.play(
            LaggedStart(*[FadeIn(m, scale=0.95) for m in label_mobs], lag_ratio=0.08),
            run_time=0.9,
        )
        self.next_slide()


class ParallelLinesSegmentLengthsDraw(Slide):
    """Nine click-advanced steps: highlights + k labels, then clear frame.

    Steps 1–8: highlight DE, EA, CB, BF and matching-colour k labels.
    Step 9:     remove every element one-by-one (reverse order), then blank slide.

    For build-only (steps 1–8): see `ParallelLinesSegmentLengthsBuildDraw`.
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, labels, _diagram = _add_base_diagram(self)
        mobs = _segment_lengths_build_steps(self, lines, labels)
        self._segment_lengths_teardown(mobs, lines, labels)

    def _segment_lengths_teardown(
        self,
        mobs: dict,
        lines: dict[str, Line],
        labels: dict[str, Tex],
    ) -> None:
        """Step 9 — remove every element one-by-one (reverse of build order)."""
        rt = 0.32
        lbl_bf = mobs["lbl_bf"]
        hi_bf = mobs["hi_bf"]
        lbl_cb = mobs["lbl_cb"]
        hi_cb = mobs["hi_cb"]
        lbl_ea = mobs["lbl_ea"]
        hi_ea = mobs["hi_ea"]
        lbl_de = mobs["lbl_de"]
        hi_de = mobs["hi_de"]

        _remove(self, lbl_bf)
        _remove(self, hi_bf)
        _remove(self, lbl_cb)
        _remove(self, hi_cb)
        _remove(self, lbl_ea)
        _remove(self, hi_ea)
        _remove(self, lbl_de)
        _remove(self, hi_de)
        _remove(self, lines["seg_EF"])
        _remove(self, lines["diag_DB"])
        _remove(self, lines["seg_CG"])
        _remove(self, lines["right_AB"])
        _remove(self, lines["left_DC"])
        _remove(self, lines["bottom_CF"])
        _remove(self, lines["top_DA"])
        _remove(self, labels["H"])
        _remove(self, labels["G"])
        _remove(self, labels["F"])
        _remove(self, labels["B"])
        _remove(self, labels["C"])
        _remove(self, labels["A"])
        _remove(self, labels["E"])
        _remove(self, labels["D"])
        self.next_slide()


class ParallelLinesSegmentLengthsBuildDraw(Slide):
    """Eight click-advanced steps: highlights + k labels only (no teardown).

    Same as `ParallelLinesSegmentLengthsDraw` steps 1–8. Used by card 1 main panel
    so all segment labels stay on screen. Deck: `slides/segment-lengths-build/`.
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, labels, _diagram = _add_base_diagram(self)
        _segment_lengths_build_steps(self, lines, labels)


def _segment_lengths_build_steps(
    scene: Slide,
    lines: dict[str, Line],
    labels: dict[str, Tex],
) -> dict:
    """Steps 1–8: highlight DE, EA, CB, BF and matching-colour k labels."""
    top_da = lines["top_DA"]
    bot_cf = lines["bottom_CF"]
    de_p1, de_p2 = _laid_out_subsegment(top_da, D, E, D, A)
    ea_p1, ea_p2 = _laid_out_subsegment(top_da, E, A, D, A)
    cb_p1, cb_p2 = _laid_out_subsegment(bot_cf, C, B, C, F)
    bf_p1, bf_p2 = _laid_out_subsegment(bot_cf, B, F, C, F)

    hi_de = _highlight_seg(de_p1, de_p2, COL_DE)
    scene.play(Create(hi_de), run_time=0.65)
    scene.next_slide()

    lbl_de = _length_label(r"5k", de_p1, de_p2, UP, ink=COL_DE)
    scene.play(FadeIn(lbl_de, scale=0.95), run_time=0.5)
    scene.next_slide()

    hi_ea = _highlight_seg(ea_p1, ea_p2, COL_EA)
    scene.play(Create(hi_ea), run_time=0.65)
    scene.next_slide()

    lbl_ea = _length_label(r"2k", ea_p1, ea_p2, UP, ink=COL_EA)
    scene.play(FadeIn(lbl_ea, scale=0.95), run_time=0.5)
    scene.next_slide()

    hi_cb = _highlight_seg(cb_p1, cb_p2, COL_CB)
    scene.play(Create(hi_cb), run_time=0.65)
    scene.next_slide()

    lbl_cb = _length_label(r"7k", cb_p1, cb_p2, DOWN, ink=COL_CB)
    scene.play(FadeIn(lbl_cb, scale=0.95), run_time=0.5)
    scene.next_slide()

    hi_bf = _highlight_seg(bf_p1, bf_p2, COL_BF)
    scene.play(Create(hi_bf), run_time=0.65)
    scene.next_slide()

    lbl_bf = _length_label(r"5k", bf_p1, bf_p2, DOWN, ink=COL_BF)
    scene.play(FadeIn(lbl_bf, scale=0.95), run_time=0.5)
    scene.next_slide()

    return {
        "hi_de": hi_de,
        "lbl_de": lbl_de,
        "hi_ea": hi_ea,
        "lbl_ea": lbl_ea,
        "hi_cb": hi_cb,
        "lbl_cb": lbl_cb,
        "hi_bf": hi_bf,
        "lbl_bf": lbl_bf,
    }


def _angle_marks_parallel_da_cb_step(scene: Slide, lines: dict[str, Line]):
    """Single slide: // chevrons on **DA** and **CB** (card 2 main, beat 1)."""
    top_da = lines["top_DA"]
    bot_cf = lines["bottom_CF"]
    da_p1, da_p2 = top_da.get_start(), top_da.get_end()
    cb_p1, cb_p2 = _laid_out_subsegment(bot_cf, C, B, C, F)
    arr_da = _parallel_arrow_mark(da_p1, da_p2, ink=DRAW_INK)
    arr_cb = _parallel_arrow_mark(cb_p1, cb_p2, ink=DRAW_INK)
    scene.play(Create(arr_da), Create(arr_cb), run_time=0.75)
    scene.next_slide()
    return arr_da, arr_cb


def _angle_marks_shade_eag_gbf_step(scene: Slide, lines: dict[str, Line]):
    """Single slide: fill △**EAG** red and △**GBF** green (card 2 main, beat 2)."""
    v = _laid_out_vertices(lines)
    tri_eag = _filled_triangle(v["E"], v["A"], v["G"], COL_TRI_EAG)
    tri_gbf = _filled_triangle(v["G"], v["B"], v["F"], COL_TRI_GBF)
    scene.add(tri_eag, tri_gbf)
    scene.bring_to_back(tri_eag, tri_gbf)
    scene.play(FadeIn(tri_eag), FadeIn(tri_gbf), run_time=0.8)
    scene.next_slide()
    return tri_eag, tri_gbf


def _angle_marks_card2_main_steps(scene: Slide, lines: dict[str, Line]):
    """Card 2 main panel: // marks then shaded △EAG/△GBF (2 slides, no angle arcs)."""
    par_arrows = _angle_marks_parallel_da_cb_step(scene, lines)
    tris = _angle_marks_shade_eag_gbf_step(scene, lines)
    return tris, par_arrows


def _angle_marks_build_steps(scene: Slide, lines: dict[str, Line]) -> None:
    """Steps 1–7: // arrows, angle pairs, teardown, shaded △EAG/△GBF."""
    v = _laid_out_vertices(lines)

    # ── STEP 1 — Parallel arrows on DA and CB midpoints ───────────────────
    top_da = lines["top_DA"]
    bot_cf = lines["bottom_CF"]
    da_p1, da_p2 = top_da.get_start(), top_da.get_end()
    cb_p1, cb_p2 = _laid_out_subsegment(bot_cf, C, B, C, F)
    arr_da = _parallel_arrow_mark(da_p1, da_p2, ink=DRAW_INK)
    arr_cb = _parallel_arrow_mark(cb_p1, cb_p2, ink=DRAW_INK)
    scene.play(Create(arr_da), Create(arr_cb), run_time=0.75)
    scene.next_slide()

    # ── STEP 2 — Red fills ∠DAC and ∠ABF (same angles) ────────────────────
    inside_dac = (v["D"] + v["A"] + v["B"]) / 3
    inside_abf = (v["A"] + v["B"] + v["F"]) / 3
    ang_dac = _interior_angle_fill(v["A"], v["D"], v["B"], inside_dac, COL_DAC_ABF)
    ang_abf = _interior_angle_fill(v["B"], v["A"], v["F"], inside_abf, COL_DAC_ABF)
    scene.play(*[FadeIn(m) for m in ang_dac], *[FadeIn(m) for m in ang_abf], run_time=0.75)
    scene.next_slide()

    # ── STEP 3 — Green fills ∠AEF and ∠EFB (same angles) ────────────────
    inside_aef = (v["A"] + v["E"] + v["F"]) / 3
    inside_efb = (v["E"] + v["F"] + v["B"]) / 3
    ang_aef = _interior_angle_fill(v["E"], v["A"], v["F"], inside_aef, COL_AEF_EFB)
    ang_efb = _interior_angle_fill(v["F"], v["E"], v["B"], inside_efb, COL_AEF_EFB)
    scene.play(*[FadeIn(m) for m in ang_aef], *[FadeIn(m) for m in ang_efb], run_time=0.75)
    scene.next_slide()

    # ── STEP 4 — Purple fills ∠BGF and ∠EGA (same angles) ─────────────────
    inside_bgf = (v["B"] + v["G"] + v["F"]) / 3
    inside_ega = (v["E"] + v["G"] + v["A"]) / 3
    ang_bgf = _interior_angle_fill(v["G"], v["B"], v["F"], inside_bgf, COL_BGF_EGA)
    ang_ega = _interior_angle_fill(v["G"], v["E"], v["A"], inside_ega, COL_BGF_EGA)
    scene.play(*[FadeIn(m) for m in ang_bgf], *[FadeIn(m) for m in ang_ega], run_time=0.75)
    scene.next_slide()

    # ── STEP 5 — Remove marks one-by-one (reverse of steps 1–4) ─────────
    rt = 0.32
    _remove(scene, ang_ega[0])
    _remove(scene, ang_ega[1])
    _remove(scene, ang_bgf[0])
    _remove(scene, ang_bgf[1])
    _remove(scene, ang_efb[0])
    _remove(scene, ang_efb[1])
    _remove(scene, ang_aef[0])
    _remove(scene, ang_aef[1])
    _remove(scene, ang_abf[0])
    _remove(scene, ang_abf[1])
    _remove(scene, ang_dac[0])
    _remove(scene, ang_dac[1])
    _remove(scene, arr_cb)
    _remove(scene, arr_da)
    scene.next_slide()

    # ── STEP 6 — Shade △EAG (red) and △GBF (green) ──────────────────────
    tri_eag = _filled_triangle(v["E"], v["A"], v["G"], COL_TRI_EAG)
    tri_gbf = _filled_triangle(v["G"], v["B"], v["F"], COL_TRI_GBF)
    scene.add(tri_eag, tri_gbf)
    scene.bring_to_back(tri_eag, tri_gbf)
    scene.play(FadeIn(tri_eag), FadeIn(tri_gbf), run_time=0.8)
    scene.next_slide()

    # ── STEP 7 — Remove shaded regions one-by-one (reverse of step 6) ─────
    rt = 0.32
    _remove(scene, tri_gbf)
    _remove(scene, tri_eag)
    scene.next_slide()


def _eag_gbf_angle_pairs_steps(scene: Slide, v: dict) -> list:
    """Three slides: green, red, purple angle pairs for △AEG ~ △GBF (AAA)."""
    angle_mobs: list = []
    inside_aeg = (v["A"] + v["E"] + v["G"]) / 3
    inside_bfg = (v["B"] + v["F"] + v["G"]) / 3
    ang_aeg = _interior_angle_fill(v["E"], v["A"], v["G"], inside_aeg, COL_AEF_EFB)
    ang_bfg = _interior_angle_fill(v["F"], v["B"], v["G"], inside_bfg, COL_AEF_EFB)
    angle_mobs.extend(ang_aeg)
    angle_mobs.extend(ang_bfg)
    scene.play(*[FadeIn(m) for m in ang_aeg], *[FadeIn(m) for m in ang_bfg], run_time=0.75)
    scene.next_slide()

    inside_eag = (v["E"] + v["A"] + v["G"]) / 3
    inside_fbg = (v["F"] + v["B"] + v["G"]) / 3
    ang_eag = _interior_angle_fill(v["A"], v["E"], v["G"], inside_eag, COL_DAC_ABF)
    ang_fbg = _interior_angle_fill(v["B"], v["F"], v["G"], inside_fbg, COL_DAC_ABF)
    angle_mobs.extend(ang_eag)
    angle_mobs.extend(ang_fbg)
    scene.play(*[FadeIn(m) for m in ang_eag], *[FadeIn(m) for m in ang_fbg], run_time=0.75)
    scene.next_slide()

    inside_age = (v["A"] + v["G"] + v["E"]) / 3
    inside_bgf = (v["B"] + v["G"] + v["F"]) / 3
    ang_age = _interior_angle_fill(v["G"], v["A"], v["E"], inside_age, COL_BGF_EGA)
    ang_bgf = _interior_angle_fill(v["G"], v["B"], v["F"], inside_bgf, COL_BGF_EGA)
    angle_mobs.extend(ang_age)
    angle_mobs.extend(ang_bgf)
    scene.play(*[FadeIn(m) for m in ang_age], *[FadeIn(m) for m in ang_bgf], run_time=0.75)
    scene.next_slide()
    return angle_mobs


def _eag_edge_lines(v: dict, ink: ManimColor = DRAW_INK) -> VGroup:
    """Stroke edges EA, EG, AG for △EAG (move with the red triangle)."""
    g = v["G"]
    return VGroup(
        Line(v["E"], v["A"], color=ink, stroke_width=STROKE),
        Line(v["E"], g, color=ink, stroke_width=STROKE),
        Line(v["A"], g, color=ink, stroke_width=STROKE),
    )


def _gcb_edge_lines(v: dict, ink: ManimColor = DRAW_INK) -> VGroup:
    """Stroke edges GC, CB, GB for △GCB (move with the blue triangle)."""
    g, c, b = v["G"], v["C"], v["B"]
    return VGroup(
        Line(c, g, color=ink, stroke_width=STROKE),
        Line(c, b, color=ink, stroke_width=STROKE),
        Line(g, b, color=ink, stroke_width=STROKE),
    )


def _gbf_edge_lines(v: dict, bf_line: Line, ink: ManimColor = DRAW_INK) -> VGroup:
    """Stroke edges GB, GF plus trimmed BF for △GBF (fixed when △GCB shifts)."""
    g = v["G"]
    return VGroup(
        bf_line,
        Line(g, v["B"], color=ink, stroke_width=STROKE),
        Line(g, v["F"], color=ink, stroke_width=STROKE),
    )


def _gbf_edge_lines_explicit(v: dict, ink: ManimColor = DRAW_INK) -> VGroup:
    """GB, GF, BF as separate segments for △GBF (no shared diagram Line refs)."""
    g, b, f = v["G"], v["B"], v["F"]
    return VGroup(
        Line(g, b, color=ink, stroke_width=STROKE),
        Line(g, f, color=ink, stroke_width=STROKE),
        Line(b, f, color=ink, stroke_width=STROKE),
    )


def _trim_g_extensions_from_g(lines: dict[str, Line], v: dict) -> None:
    """Drop GA and GE extensions — keep only GB and GF from vertex G."""
    lines["right_AB"].put_start_and_end_on(v["G"], v["B"])
    lines["seg_EF"].put_start_and_end_on(v["G"], v["F"])


def _swap_gcb_gbf_diagram_ink_for_edge_lines(
    scene: Slide,
    lines: dict[str, Line],
    v: dict,
) -> tuple[VGroup, VGroup]:
    """Replace composite diagram lines with explicit △GCB / △GBF edge groups."""
    gcb_edges = _gcb_edge_lines(v)
    gbf_edges = _gbf_edge_lines_explicit(v)
    _remove(scene, lines["right_AB"], lines["seg_EF"], lines["seg_CG"], lines["bottom_CF"])
    scene.add(gbf_edges)
    return gcb_edges, gbf_edges


def _area_compare_k_and_areas_steps(
    scene: Slide,
    tri_eag: Polygon,
    tri_gbf: Polygon,
    *,
    refresh_k_labels: bool = False,
    hi_bf=None,
    lbl_bf=None,
    hi_ea=None,
    lbl_ea=None,
) -> None:
    """Mark 5k / 2k on grounded △GBF / △EAG, then 48 & 300 cm²."""
    gbf_verts = tri_gbf.get_vertices()
    eag_verts = tri_eag.get_vertices()
    bf_p1, bf_p2 = gbf_verts[1], gbf_verts[2]
    ea_p1, ea_p2 = eag_verts[0], eag_verts[1]

    if refresh_k_labels and hi_bf is not None:
        _remove(scene, hi_bf, lbl_bf)
        hi_bf = None
    if hi_bf is None:
        hi_bf = _highlight_seg(bf_p1, bf_p2, COL_BF)
        hi_bf.set_z_index(2)
        lbl_bf = _length_label(r"5k", bf_p1, bf_p2, DOWN, ink=COL_BF)
        lbl_bf.set_z_index(3)
        scene.play(Create(hi_bf), run_time=0.65)
        scene.play(FadeIn(lbl_bf, scale=0.95), run_time=0.5)
    scene.next_slide()

    if refresh_k_labels and hi_ea is not None:
        _remove(scene, hi_ea, lbl_ea)
        hi_ea = None
    if hi_ea is None:
        hi_ea = _highlight_seg(ea_p1, ea_p2, COL_EA)
        hi_ea.set_z_index(2)
        lbl_ea = _length_label(r"2k", ea_p1, ea_p2, DOWN, ink=COL_EA)
        lbl_ea.set_z_index(3)
        scene.play(Create(hi_ea), run_time=0.65)
        scene.play(FadeIn(lbl_ea, scale=0.95), run_time=0.5)
    scene.next_slide()

    area_eag = _area_label_in_triangle(
        tri_eag,
        r"\mathbf{48\ \mathrm{cm}^{2}}",
        color=DRAW_INK,
        shift=LEFT * AREA_LABEL_H_SHIFT + DOWN * AREA_EAG_VERT_SHIFT,
    )
    area_gbf = _area_label_in_triangle(
        tri_gbf,
        r"\mathbf{300\ \mathrm{cm}^{2}}",
        color=DRAW_INK,
        shift=LEFT * AREA_GBF_H_SHIFT,
    )
    area_eag.set_z_index(4)
    area_gbf.set_z_index(4)
    scene.play(FadeIn(area_eag), FadeIn(area_gbf), run_time=0.6)
    scene.next_slide()


def _area_compare_side_by_side_labels_and_areas(
    scene: Slide,
    tri_eag: Polygon,
    tri_gbf: Polygon,
) -> None:
    """Relabel side-by-side △EAG/△GBF, mark 2k/5k, then 48 & 300 cm²."""
    eag_verts = tri_eag.get_vertices()
    gbf_verts = tri_gbf.get_vertices()
    eag_c = tri_eag.get_center()
    gbf_c = tri_gbf.get_center()
    lbl_g_eag = _label_at_vertex("G", eag_verts[2], eag_c)
    lbl_a_fin = _label_at_vertex("A", eag_verts[1], eag_c)
    lbl_e_fin = _label_at_vertex("E", eag_verts[0], eag_c)
    lbl_g_gbf = _label_at_vertex("G", gbf_verts[0], gbf_c)
    lbl_b_fin = _label_at_vertex("B", gbf_verts[1], gbf_c)
    lbl_f_fin = _label_at_vertex("F", gbf_verts[2], gbf_c)
    scene.play(
        FadeIn(lbl_g_eag),
        FadeIn(lbl_a_fin),
        FadeIn(lbl_e_fin),
        FadeIn(lbl_g_gbf),
        FadeIn(lbl_b_fin),
        FadeIn(lbl_f_fin),
        run_time=0.75,
    )
    scene.next_slide()

    bf_p1, bf_p2 = gbf_verts[1], gbf_verts[2]
    hi_bf = _highlight_seg(bf_p1, bf_p2, COL_BF)
    hi_bf.set_z_index(2)
    lbl_5k_bf = _length_label(r"5k", bf_p1, bf_p2, DOWN, ink=COL_BF)
    lbl_5k_bf.set_z_index(3)
    scene.play(Create(hi_bf), run_time=0.65)
    scene.play(FadeIn(lbl_5k_bf, scale=0.95), run_time=0.5)
    scene.next_slide()

    ea_p1, ea_p2 = eag_verts[0], eag_verts[1]
    hi_ea = _highlight_seg(ea_p1, ea_p2, COL_EA)
    hi_ea.set_z_index(2)
    lbl_2k_ea = _length_label(r"2k", ea_p1, ea_p2, DOWN, ink=COL_EA)
    lbl_2k_ea.set_z_index(3)
    scene.play(Create(hi_ea), run_time=0.65)
    scene.play(FadeIn(lbl_2k_ea, scale=0.95), run_time=0.5)
    scene.next_slide()

    area_eag = _area_label_in_triangle(
        tri_eag,
        r"\mathbf{48\ \mathrm{cm}^{2}}",
        color=DRAW_INK,
        shift=LEFT * AREA_LABEL_H_SHIFT + DOWN * AREA_EAG_VERT_SHIFT,
    )
    area_gbf = _area_label_in_triangle(
        tri_gbf,
        r"\mathbf{300\ \mathrm{cm}^{2}}",
        color=DRAW_INK,
        shift=LEFT * AREA_GBF_H_SHIFT,
    )
    area_eag.set_z_index(4)
    area_gbf.set_z_index(4)
    scene.play(FadeIn(area_eag), FadeIn(area_gbf), run_time=0.6)
    scene.next_slide()


def _area_compare_main_hold_then_areas(
    scene: Slide,
    tri_eag: Polygon,
    tri_gbf: Polygon,
    angle_mobs: list,
) -> tuple:
    """Card 3 main: fade AAA marks, hold full figure, areas only on final beat."""
    if angle_mobs:
        _remove(scene, *angle_mobs)
    scene.next_slide()

    area_eag = _area_label_in_triangle(
        tri_eag,
        r"\mathbf{48\ \mathrm{cm}^{2}}",
        color=DRAW_INK,
        shift=RIGHT * AREA_EAG_MAIN_H_SHIFT + UP * AREA_EAG_MAIN_V_SHIFT,
    )
    area_eag.scale(AREA_EAG_MAIN_SIZE_SCALE)
    area_gbf = _area_label_in_triangle(
        tri_gbf,
        r"\mathbf{300\ \mathrm{cm}^{2}}",
        color=DRAW_INK,
        shift=LEFT * AREA_GBF_H_SHIFT,
    )
    area_eag.set_z_index(4)
    area_gbf.set_z_index(4)
    scene.play(FadeIn(area_eag), FadeIn(area_gbf), run_time=0.6)
    scene.next_slide()
    return area_eag, area_gbf


def _area_compare_from_card2_main_steps(
    scene: Slide,
    lines: dict[str, Line],
    labels: dict[str, Tex],
    v: dict,
    tri_eag: Polygon,
    tri_gbf: Polygon,
    angle_mobs: list,
    extra_fade: list | None = None,
) -> tuple:
    """Card 3 main: fade angles then hold; areas synced with sub final slide."""
    _ = lines, labels, v, extra_fade
    return _area_compare_main_hold_then_areas(scene, tri_eag, tri_gbf, angle_mobs)


def _card4_main_gcb_gbf_steps(
    scene: Slide,
    v: dict,
    tri_eag: Polygon,
    tri_gbf: Polygon,
    area_eag: MathTex,
) -> Polygon:
    """Card 4 main: defill △EAG/△GBF, then highlight △GCB/△GBF (sub opens here)."""
    tri_eag.set_fill(opacity=0)
    tri_gbf.set_fill(opacity=0)
    _remove(scene, area_eag)
    scene.next_slide()

    tri_gcb = _filled_triangle(v["G"], v["C"], v["B"], COL_TRI_GCB)
    scene.add(tri_gcb, tri_gbf)
    scene.bring_to_back(tri_gcb, tri_gbf)
    scene.play(
        tri_gbf.animate.set_fill(COL_TRI_GBF, opacity=REGION_FILL_OPACITY),
        FadeIn(tri_gcb),
        run_time=0.8,
    )
    scene.next_slide()
    return tri_gcb


def _card4_main_420_beat(scene: Slide, tri_gcb: Polygon, area_gbf) -> MathTex:
    """Card 4 main final beat: 420 cm² on △GCB (synced with sub final slide)."""
    area_gcb = _area_label_inside_at_y(
        area_gbf,
        tri_gcb,
        r"\mathbf{420\ \mathrm{cm}^{2}}",
        x_frac=AREA_GCB_AREA_X_FRAC,
    )
    area_gcb.set_z_index(5)
    scene.play(FadeIn(area_gcb), run_time=0.6)
    scene.next_slide()
    return area_gcb


def _card8_main_remove_gbf_300_beat(
    scene: Slide,
    tri_gbf: Polygon,
    area_gbf: MathTex,
) -> None:
    """Card 8 main: remove green △GBF + 300 cm² before △CHB lowers (sync sub step 3)."""
    _remove(scene, tri_gbf, area_gbf)
    scene.next_slide()


def _card8_main_hbg_175_beat(
    scene: Slide,
    lines: dict[str, Line],
    v: dict[str, np.ndarray],
    tri_gcb: Polygon,
    area_gcb: MathTex,
) -> tuple[Polygon, MathTex, np.ndarray]:
    """Card 8 main: red △HBG + 175 cm²; drop **420 cm²** + blue △GCB fill."""
    h_pt = _line_intersection(
        lines["diag_DB"].get_start(), lines["diag_DB"].get_end(),
        lines["seg_CG"].get_start(), lines["seg_CG"].get_end(),
    )
    hbg = _build_chb_hbg_final_mobs(v, h_pt)
    tri_hbg = hbg["tri_hbg"]
    area_hbg = hbg["area_hbg"]
    scene.add(tri_hbg)
    scene.bring_to_back(tri_hbg)
    _remove(scene, tri_gcb, area_gcb)
    scene.play(FadeIn(tri_hbg), FadeIn(area_hbg), run_time=0.8)
    scene.next_slide()
    return tri_hbg, area_hbg, h_pt


def _part3_main_parallel_graph_steps(
    scene: Slide,
    lines: dict[str, Line],
    v: dict[str, np.ndarray],
) -> dict[str, Mobject]:
    """Main part 3: single // on DE/BF only (DB/EF already marked on HB/GF in card 5)."""
    top_da = lines["top_DA"]
    bot_cf = lines["bottom_CF"]
    de_p1, de_p2 = _laid_out_subsegment(top_da, D, E, D, A)
    bf_p1, bf_p2 = _laid_out_subsegment(bot_cf, B, F, C, F)
    arr_de = _parallel_arrow_mark(de_p1, de_p2, ink=DRAW_INK)
    arr_bf = _parallel_arrow_mark(bf_p1, bf_p2, ink=DRAW_INK)
    arr_de.set_z_index(2)
    arr_bf.set_z_index(2)
    scene.play(Create(arr_de), Create(arr_bf), run_time=0.55)
    scene.next_slide()
    return {"arr_de": arr_de, "arr_bf": arr_bf}


def _part3_main_hbg_marks_steps(
    scene: Slide,
    v: dict[str, np.ndarray],
    h_pt: np.ndarray,
    arrows: dict[str, Mobject],
    *,
    hi_cb_low: Mobject | None = None,
    lbl_7k_low: Mobject | None = None,
    ang_r: float = CGB_ANGLE_RADIUS,
) -> dict[str, Mobject]:
    """Main part 3: CD/AB // marks, △CDH fill, three AAA angle pairs."""
    rt = 0.28
    fade_out: list[Mobject] = [arrows["arr_bf"]]
    if hi_cb_low is not None:
        fade_out.append(hi_cb_low)
    if lbl_7k_low is not None:
        fade_out.append(lbl_7k_low)
    _remove(scene, *fade_out)
    scene.next_slide()

    new_arrows = _build_chb_hbg_marks_arrow_marks(v)
    scene.play(
        Create(new_arrows["arr_cd"]),
        Create(new_arrows["arr_ab"]),
        run_time=0.55,
    )
    scene.next_slide()

    tri_cdh = _filled_triangle(v["C"], v["D"], h_pt, COL_TRI_CDH)
    scene.add(tri_cdh)
    scene.bring_to_back(tri_cdh)
    scene.play(FadeIn(tri_cdh), run_time=0.5)
    scene.next_slide()

    arcs = _build_chb_hbg_marks_angle_arcs(v, h_pt, ang_r)
    scene.play(
        Create(arcs["ang_cdb"]),
        Create(arcs["ang_gbh"]),
        run_time=0.55,
    )
    scene.next_slide()
    scene.play(
        Create(arcs["ang_dch"]),
        Create(arcs["ang_hgb"]),
        run_time=0.55,
    )
    scene.next_slide()
    scene.play(
        Create(arcs["ang_dhc"]),
        Create(arcs["ang_ghb"]),
        run_time=0.55,
    )
    scene.next_slide()
    return {"tri_cdh": tri_cdh, **new_arrows, **arcs}


def _part3_main_k_regions_steps(
    scene: Slide,
    v: dict[str, np.ndarray],
) -> dict[str, Mobject]:
    """Main part 3: △EAG/△GBF fills and k length labels."""
    rt = 0.28
    k_mobs = _build_chb_hbg_k_region_mobs(v)
    tri_eag, tri_gbf = k_mobs["tri_eag"], k_mobs["tri_gbf"]
    scene.add(tri_eag, tri_gbf)
    scene.bring_to_back(tri_eag, tri_gbf)
    scene.play(FadeIn(tri_eag), FadeIn(tri_gbf), run_time=0.55)
    scene.next_slide()
    scene.play(Create(k_mobs["hi_ea"]), run_time=rt)
    scene.play(FadeIn(k_mobs["lbl_2k_ea"], scale=0.95), run_time=0.45)
    scene.play(Create(k_mobs["hi_ag"]), run_time=rt)
    scene.play(FadeIn(k_mobs["lbl_2k_ag"], scale=0.95), run_time=0.45)
    scene.next_slide()
    scene.play(Create(k_mobs["hi_bf"]), run_time=rt)
    scene.play(FadeIn(k_mobs["lbl_5k_bf"], scale=0.95), run_time=0.45)
    scene.play(Create(k_mobs["hi_bg"]), run_time=rt)
    scene.play(FadeIn(k_mobs["lbl_5k_bg"], scale=0.95), run_time=0.45)
    scene.next_slide()
    scene.play(Create(k_mobs["hi_dc"]), run_time=rt)
    scene.play(FadeIn(k_mobs["lbl_7k_dc"], scale=0.95), run_time=0.45)
    scene.next_slide()
    return k_mobs


def _part3_main_k_trim_steps(
    scene: Slide,
    lines: dict[str, Line],
    labels: dict[str, Tex],
    v: dict[str, np.ndarray],
    h_pt: np.ndarray,
    tri_hbg: Polygon,
    area_hbg: MathTex,
    marks_mobs: dict[str, Mobject],
    graph_arrows: dict[str, Mobject],
    k_mobs: dict[str, Mobject],
    seg_mobs: dict[str, Mobject],
    *,
    arr_hb: Mobject | None = None,
    arr_gf: Mobject | None = None,
    arr_da: Mobject | None = None,
    arr_cb: Mobject | None = None,
) -> None:
    """Main part 3: trim k regions, 343 cm², CDH-only frame."""
    rt = 0.55
    card1_seg_fade = [
        seg_mobs["hi_de"],
        seg_mobs["lbl_de"],
        seg_mobs["hi_ea"],
        seg_mobs["lbl_ea"],
        seg_mobs["hi_cb"],
        seg_mobs["lbl_cb"],
        seg_mobs["hi_bf"],
        seg_mobs["lbl_bf"],
    ]
    _remove(
        scene,
        k_mobs["tri_eag"],
        k_mobs["tri_gbf"],
        k_mobs["hi_ea"],
        k_mobs["lbl_2k_ea"],
        k_mobs["hi_ag"],
        k_mobs["lbl_2k_ag"],
        k_mobs["hi_bf"],
        k_mobs["lbl_5k_bf"],
    )
    _remove(scene, *card1_seg_fade)
    scene.next_slide()

    tri_cdh = marks_mobs["tri_cdh"]
    area_cdh = _area_label_in_triangle(
        tri_cdh,  # type: ignore[arg-type]
        r"\mathbf{343\ \mathrm{cm}^{2}}",
        shift=RIGHT * AREA_CDH_H_SHIFT,
    )
    area_cdh.set_z_index(5)
    scene.play(FadeIn(area_cdh), run_time=0.45)
    scene.next_slide()

    _trim_cdh_triangle_ink(lines, v, h_pt)
    frame: dict[str, Mobject | np.ndarray] = {
        **k_mobs,
        **marks_mobs,
        "arr_de": graph_arrows["arr_de"],
        "tri_hbg": tri_hbg,
        "area_hbg": area_hbg,
        "area_cdh": area_cdh,
        "v": v,
        "h_pt": h_pt,
    }
    cleanup = _chb_hbg_k_final_cleanup_mobs(frame, lines, labels)  # type: ignore[arg-type]
    extra = [
        m for m in (arr_hb, arr_gf, arr_da, arr_cb) if m is not None
    ]
    _remove(scene, *(cleanup + extra))
    scene.next_slide()


def _gcb_gbf_isolate_reveal(
    scene: Slide,
    lines: dict[str, Line],
    labels: dict[str, Tex],
    v: dict,
    tri_gcb: Polygon,
    tri_gbf: Polygon,
    area_gbf,
) -> None:
    """Sub card 4 beat 0: isolated △GCB + △GBF with 300 cm²; keep △ ink only."""
    rt = 0.30
    scene.play(
        FadeIn(tri_gcb),
        FadeIn(tri_gbf),
        FadeIn(area_gbf),
        run_time=0.75,
    )
    _trim_g_extensions_from_g(lines, v)
    _remove(scene, lines["left_DC"])
    _remove(scene, lines["diag_DB"])
    _remove(scene, lines["top_DA"])
    _remove(scene, labels["D"])
    _remove(scene, labels["E"])
    _remove(scene, labels["A"])
    _remove(scene, labels["H"])
    scene.next_slide()


def _gcb_gbf_regions_sub_steps(
    scene: Slide,
    lines: dict[str, Line],
    labels: dict[str, Tex],
    v: dict,
    tri_gcb: Polygon,
    tri_gbf: Polygon,
    area_gbf,
) -> None:
    """Sub card 4 beats 1–4: altitudes → side-by-side → k labels → 420 cm²."""
    g, b, f = v["G"], v["B"], v["F"]
    foot_gcb = _foot_to_horizontal(b, g[1])
    dash_gcb = _gcb_altitude_dash(tri_gcb)
    ht_gcb = _altitude_seg(b, foot_gcb, COL_TRI_GCB)
    foot_gbf = _foot_to_horizontal(g, b[1])
    ht_gbf = _altitude_seg(g, foot_gbf, COL_TRI_GBF)
    scene.play(Create(dash_gcb), run_time=0.55)
    scene.play(Create(ht_gcb), run_time=0.55)
    scene.play(Create(ht_gbf), run_time=0.55)
    scene.next_slide()

    gcb_edges, _gbf_edges = _swap_gcb_gbf_diagram_ink_for_edge_lines(scene, lines, v)
    gcb_body = VGroup(tri_gcb, gcb_edges, ht_gcb, labels["C"])
    shift = _comparison_shift_grounded(tri_gcb, tri_gbf, gap=GCB_COMPARE_GAP)
    _remove(scene, dash_gcb)
    scene.play(gcb_body.animate.shift(shift), run_time=0.85)
    gcb_verts = tri_gcb.get_vertices()
    lbl_g_gcb = _label_like_orig("G", gcb_verts[0], labels["G"], v["G"])
    lbl_b_gcb = _label_like_orig("B", gcb_verts[2], labels["B"], v["B"])
    lbl_g_gcb.set_z_index(3)
    lbl_b_gcb.set_z_index(3)
    scene.play(FadeIn(lbl_g_gcb), FadeIn(lbl_b_gcb), run_time=0.5)
    dash_heights = _dash_between_heights(ht_gcb, ht_gbf)
    scene.play(Create(dash_heights), run_time=0.55)
    scene.next_slide()

    gcb_verts = tri_gcb.get_vertices()
    gbf_verts = tri_gbf.get_vertices()
    cb_p1, cb_p2 = gcb_verts[1], gcb_verts[2]
    bf_p1, bf_p2 = gbf_verts[1], gbf_verts[2]
    hi_cb = _highlight_seg(cb_p1, cb_p2, COL_CB)
    hi_cb.set_z_index(2)
    lbl_7k_cb = _length_label(r"7k", cb_p1, cb_p2, DOWN, ink=COL_CB)
    lbl_7k_cb.set_z_index(3)
    hi_bf = _highlight_seg(bf_p1, bf_p2, COL_BF)
    hi_bf.set_z_index(2)
    lbl_5k_bf = _length_label(r"5k", bf_p1, bf_p2, DOWN, ink=COL_BF)
    lbl_5k_bf.set_z_index(3)
    scene.play(Create(hi_cb), run_time=0.65)
    scene.play(FadeIn(lbl_7k_cb, scale=0.95), run_time=0.5)
    scene.play(Create(hi_bf), run_time=0.65)
    scene.play(FadeIn(lbl_5k_bf, scale=0.95), run_time=0.5)
    scene.next_slide()

    rt = 0.28
    _remove(scene, dash_heights)
    _remove(scene, ht_gcb)
    _remove(scene, ht_gbf)
    area_gcb = _area_label_inside_at_y(
        area_gbf,
        tri_gcb,
        r"\mathbf{420\ \mathrm{cm}^{2}}",
        x_frac=AREA_GCB_AREA_X_FRAC,
    )
    area_gbf_sub = _area_label_in_triangle(
        tri_gbf,
        r"\mathbf{300\ \mathrm{cm}^{2}}",
        color=DRAW_INK,
        shift=LEFT * AREA_GBF_H_SHIFT,
    )
    area_gcb.set_z_index(5)
    area_gbf_sub.set_z_index(5)
    _remove(scene, area_gbf)
    scene.play(FadeIn(area_gbf_sub), run_time=0.45)
    scene.play(FadeIn(area_gcb), run_time=0.45)
    scene.next_slide()


def _area_compare_from_isolated_steps(
    scene: Slide,
    lines: dict[str, Line],
    labels: dict[str, Tex],
    v: dict,
    tri_eag: Polygon,
    tri_gbf: Polygon,
    angle_mobs: list,
    arr_ea,
    arr_bf,
    hi_ea,
    lbl_ea,
    hi_bf,
    lbl_bf,
) -> None:
    """Card 3 sub: pull △EAG to ground, relabel, k marks, areas (lines stay)."""
    fade_first = [m for m in angle_mobs if m is not None]
    fade_first.extend([arr_ea, arr_bf])
    if fade_first:
        _remove(scene, *fade_first)
    scene.next_slide()

    lbl_e = _point_label("E", v["E"], UP + RIGHT * 0.15, DRAW_INK)
    lbl_a = _point_label("A", v["A"], UP + RIGHT * 0.25, DRAW_INK)
    lbl_g_eag = _point_label("G", v["G"], RIGHT, DRAW_INK)
    _remove(scene, labels["E"], labels["A"], labels["G"])

    eag_edges = _eag_edge_lines(v)
    _remove(scene, lines["top_DA"], lines["right_AB"], lines["seg_EF"])
    gbf_edges = _gbf_edge_lines(v, lines["bottom_CF"])
    scene.add(gbf_edges)

    eag_unit = VGroup(
        tri_eag, eag_edges, hi_ea, lbl_ea, lbl_e, lbl_a, lbl_g_eag,
    )
    scene.play(
        Rotate(eag_unit, angle=PI, about_point=eag_unit.get_center()),
        run_time=0.7,
    )
    shift = _comparison_shift_grounded(tri_eag, tri_gbf, gap=COMPARE_GAP)
    scene.play(eag_unit.animate.shift(shift), run_time=0.85)
    scene.next_slide()

    eag_verts = tri_eag.get_vertices()
    gbf_verts = tri_gbf.get_vertices()
    _remove(scene, lbl_e, lbl_a, lbl_g_eag)
    e_vert, a_vert = eag_verts[0], eag_verts[1]
    if float(e_vert[0]) <= float(a_vert[0]):
        lbl_e_fix = _label_like_orig("E", e_vert, labels["B"], v["B"])
        lbl_a_fix = _label_like_orig("A", a_vert, labels["F"], v["F"])
    else:
        lbl_e_fix = _label_like_orig("E", e_vert, labels["F"], v["F"])
        lbl_a_fix = _label_like_orig("A", a_vert, labels["B"], v["B"])
    lbl_g_eag_fix = _label_like_orig("G", eag_verts[2], labels["G"], v["G"])
    lbl_g_gbf_fix = _label_like_orig("G", gbf_verts[0], labels["G"], v["G"])
    g_nudge = UP * G_LABEL_COMPARE_UP + LEFT * G_LABEL_COMPARE_LEFT
    lbl_g_eag_fix.shift(g_nudge)
    lbl_g_gbf_fix.shift(g_nudge)
    scene.play(
        FadeIn(lbl_e_fix),
        FadeIn(lbl_a_fix),
        FadeIn(lbl_g_eag_fix),
        FadeIn(lbl_g_gbf_fix),
        run_time=0.75,
    )
    scene.next_slide()

    _area_compare_k_and_areas_steps(
        scene,
        tri_eag,
        tri_gbf,
        refresh_k_labels=True,
        hi_bf=hi_bf,
        lbl_bf=lbl_bf,
        hi_ea=hi_ea,
        lbl_ea=lbl_ea,
    )


def _card5_main_hb_gf_parallel_arrows(
    scene: Slide,
    lines: dict[str, Line],
    v: dict,
) -> tuple:
    """Card 5 main: double // on HB and GF (synced when sub marks DB ∥ EF)."""
    cg = lines["seg_CG"]
    h_pt = _line_intersection(
        lines["diag_DB"].get_start(), lines["diag_DB"].get_end(),
        cg.get_start(), cg.get_end(),
    )
    arr_hb = _double_parallel_arrow_mark(h_pt, v["B"])
    arr_gf = _double_parallel_arrow_mark(v["G"], v["F"])
    arr_hb.set_z_index(2)
    arr_gf.set_z_index(2)
    scene.play(Create(arr_hb), Create(arr_gf), run_time=0.75)
    scene.next_slide()
    return arr_hb, arr_gf, h_pt


class ParallelLinesSegmentLengthsAngleMarksDraw(Slide):
    """Thirty-five click-advanced steps: cards 1–11 main simulation (no redraw between cards).

    Steps 1–8: segment k labels.
    Steps 9–13: card 2 — //, △ fills, AAA angle pairs.
    Steps 14–15: card 3 — fade angles, in-place area labels.
    Steps 16–18: card 4 — defill △EAG/△GBF, highlight △GCB/△GBF, 420 cm².
    Step 19: card 5 — double // on HB and GF (synced with sub DB/EF slide).
    Steps 20–21: card 8 — drop green △GBF + 300 cm², then red △HBG + 175 cm² (420 gone).
    Steps 22–33: part 3 — // on DE/BF, △CDH ~ △GBH, k labels, trim, 343 cm².
    Step 34: CDH-only frame (terminal — teal △CDH + 343 cm² + C/D/H labels).
    Deck: `slides/segment-lengths-angle-marks/`.
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, labels, _diagram = _add_base_diagram(self)
        seg_mobs = _segment_lengths_build_steps(self, lines, labels)
        (tri_eag, tri_gbf), (arr_da, arr_cb) = _angle_marks_card2_main_steps(self, lines)
        v = _laid_out_vertices(lines)
        angle_mobs = _eag_gbf_angle_pairs_steps(self, v)
        extra_fade = list(seg_mobs.values()) + [arr_da, arr_cb]
        area_eag, area_gbf = _area_compare_from_card2_main_steps(
            self, lines, labels, v, tri_eag, tri_gbf, angle_mobs, extra_fade,
        )
        tri_gcb = _card4_main_gcb_gbf_steps(self, v, tri_eag, tri_gbf, area_eag)
        area_gcb = _card4_main_420_beat(self, tri_gcb, area_gbf)
        arr_hb, arr_gf, _h_card5 = _card5_main_hb_gf_parallel_arrows(self, lines, v)
        _card8_main_remove_gbf_300_beat(self, tri_gbf, area_gbf)
        tri_hbg, area_hbg, h_pt = _card8_main_hbg_175_beat(self, lines, v, tri_gcb, area_gcb)
        graph_arrows = _part3_main_parallel_graph_steps(self, lines, v)
        marks_mobs = _part3_main_hbg_marks_steps(self, v, h_pt, graph_arrows)
        k_mobs = _part3_main_k_regions_steps(self, v)
        _part3_main_k_trim_steps(
            self, lines, labels, v, h_pt, tri_hbg, area_hbg,
            marks_mobs, graph_arrows, k_mobs, seg_mobs,
            arr_hb=arr_hb, arr_gf=arr_gf, arr_da=arr_da, arr_cb=arr_cb,
        )


class ParallelLinesGcbGbfRegionsDraw(Slide):
    """Isolated △GCB / △GBF same-height area compare (card 4 sub-animation).

    Step 0: isolate △GCB + △GBF with 300 cm² (triangle ink kept).
    Steps 1–4: altitudes, side-by-side, 7k/5k, 420 & 300 cm².
    Deck: `slides/gcb-gbf-regions/`.
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, labels, _diagram = _add_base_diagram(self)
        v = _laid_out_vertices(lines)
        tri_gbf = _filled_triangle(v["G"], v["B"], v["F"], COL_TRI_GBF)
        tri_gcb = _filled_triangle(v["G"], v["C"], v["B"], COL_TRI_GCB)
        self.add(tri_gcb, tri_gbf)
        self.bring_to_back(tri_gcb, tri_gbf)
        area_gbf = _area_label_in_triangle(
            tri_gbf,
            r"\mathbf{300\ \mathrm{cm}^{2}}",
            color=DRAW_INK,
            shift=LEFT * AREA_GBF_H_SHIFT,
        )
        area_gbf.set_z_index(4)
        _gcb_gbf_isolate_reveal(self, lines, labels, v, tri_gcb, tri_gbf, area_gbf)
        _gcb_gbf_regions_sub_steps(
            self, lines, labels, v, tri_gcb, tri_gbf, area_gbf,
        )


class ParallelLinesAngleMarksDraw(Slide):
    """Seven click-advanced steps: marks, angles, teardown, shaded regions.

    Steps 1–4: add // arrows, then red / green / purple filled angle pairs.
    Step 5:     remove every mark one-by-one (reverse order), base diagram stays.
    Step 6:     fill △EAG red and △GBF green behind the white ink.
    Step 7:     remove shaded triangles one-by-one (reverse of step 6).
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, _labels, _diagram = _add_base_diagram(self)
        _angle_marks_build_steps(self, lines)


class ParallelLinesTriangleRegionsDraw(Slide):
    """Continuation from angle-marks step 7: fills, altitudes, cleanup, compare.

    Step 0: base diagram (angle-marks step 7 end).
    Step 1: △GBF green + △GCB blue.
    Step 2: altitudes (GCB dash + heights).
    Step 3: remove labels D/E/A/H and diagram ink (DC, HD, EA, DG, GA, …).
    Step 4: duplicate G/B labels on △GCB; shift △GCB left beside △GBF.
    Step 5: blue **CB** + **7k** below; yellow **BF** + **5k** below.
    Step 6: remove dash + altitudes; **300 cm²** in △GBF, **420 cm²** in △GCB.
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, labels, _diagram = _add_base_diagram(self)
        v = _laid_out_vertices(lines)
        # Beat 0: static base frame (matches angle-marks step 7 end).
        self.play(Wait(0.01), run_time=0.01)
        self.next_slide()

        # ── STEP 1 — Shade △GBF (green) and △GCB (blue) ─────────────────────
        tri_gbf = _filled_triangle(v["G"], v["B"], v["F"], COL_TRI_GBF)
        tri_gcb = _filled_triangle(v["G"], v["C"], v["B"], COL_TRI_GCB)
        self.add(tri_gbf, tri_gcb)
        self.bring_to_back(tri_gbf, tri_gcb)
        self.play(FadeIn(tri_gbf), FadeIn(tri_gcb), run_time=0.8)
        self.next_slide()

        # ── STEP 2 — Altitudes: △GCB (B ⟂ horiz. through G), △GBF (G ⟂ BF) ──
        g, b, f = v["G"], v["B"], v["F"]
        foot_gcb = _foot_to_horizontal(b, g[1])
        dash_gcb = _gcb_altitude_dash(tri_gcb)
        ht_gcb = _altitude_seg(b, foot_gcb, COL_TRI_GCB)
        foot_gbf = _foot_to_horizontal(g, b[1])
        ht_gbf = _altitude_seg(g, foot_gbf, COL_TRI_GBF)
        self.play(Create(dash_gcb), run_time=0.55)
        self.play(Create(ht_gcb), run_time=0.55)
        self.play(Create(ht_gbf), run_time=0.55)
        self.next_slide()

        # ── STEP 3 — Remove extra labels and diagram ink (one mob each) ───────
        rt = 0.28
        # Remove: point label D
        _remove(self, labels["D"])
        # Remove: point label E
        _remove(self, labels["E"])
        # Remove: point label A
        _remove(self, labels["A"])
        # Remove: point label H
        _remove(self, labels["H"])
        # Remove: line DC (C → D)
        _remove(self, lines["left_DC"])
        # Remove: diagonal DB (includes HD, H → D)
        _remove(self, lines["diag_DB"])
        # Remove: top parallel DA (includes EA, E → A, and DG, D → E)
        _remove(self, lines["top_DA"])
        # Remove: slant AB (includes GA, G → A)
        _remove(self, lines["right_AB"])
        # Remove: line CG (C → G)
        _remove(self, lines["seg_CG"])
        # Remove: bottom parallel CF (C — B — F)
        _remove(self, lines["bottom_CF"])
        # Remove: line EF (E → F)
        _remove(self, lines["seg_EF"])
        self.next_slide()

        # ── STEP 4 — Shift △GCB left; duplicate G/B labels; dash joins altitudes ─
        gcb_body = VGroup(tri_gcb, ht_gcb, labels["C"])
        shift = _comparison_shift_grounded(tri_gcb, tri_gbf, gap=GCB_COMPARE_GAP)
        _remove(self, dash_gcb)
        self.play(gcb_body.animate.shift(shift), run_time=0.85)
        gcb_verts = tri_gcb.get_vertices()
        lbl_g_gcb = _label_like_orig("G", gcb_verts[0], labels["G"], v["G"])
        lbl_b_gcb = _label_like_orig("B", gcb_verts[2], labels["B"], v["B"])
        lbl_g_gcb.set_z_index(3)
        lbl_b_gcb.set_z_index(3)
        self.play(
            FadeIn(lbl_g_gcb),
            FadeIn(lbl_b_gcb),
            run_time=0.5,
        )
        dash_heights = _dash_between_heights(ht_gcb, ht_gbf)
        self.play(Create(dash_heights), run_time=0.55)
        self.next_slide()

        # ── STEP 5 — CB (blue) 7k below; BF (yellow) 5k below ───────────────
        gcb_verts = tri_gcb.get_vertices()
        gbf_verts = tri_gbf.get_vertices()
        cb_p1, cb_p2 = gcb_verts[1], gcb_verts[2]  # C → B on △GCB
        bf_p1, bf_p2 = gbf_verts[1], gbf_verts[2]  # B → F on △GBF
        hi_cb = _highlight_seg(cb_p1, cb_p2, COL_CB)
        hi_cb.set_z_index(2)
        lbl_7k_cb = _length_label(r"7k", cb_p1, cb_p2, DOWN, ink=COL_CB)
        lbl_7k_cb.set_z_index(3)
        hi_bf = _highlight_seg(bf_p1, bf_p2, COL_BF)
        hi_bf.set_z_index(2)
        lbl_5k_bf = _length_label(r"5k", bf_p1, bf_p2, DOWN, ink=COL_BF)
        lbl_5k_bf.set_z_index(3)
        self.play(Create(hi_cb), run_time=0.65)
        self.play(FadeIn(lbl_7k_cb, scale=0.95), run_time=0.5)
        self.play(Create(hi_bf), run_time=0.65)
        self.play(FadeIn(lbl_5k_bf, scale=0.95), run_time=0.5)
        self.next_slide()

        # ── STEP 6 — Remove dash + heights; area labels in triangle centres ──
        rt = 0.28
        # Remove: horizontal dashed line between altitudes
        _remove(self, dash_heights)
        # Remove: blue altitude on △GCB
        _remove(self, ht_gcb)
        # Remove: green altitude on △GBF
        _remove(self, ht_gbf)
        area_gbf = _area_label_in_triangle(
            tri_gbf,
            r"\mathbf{300\ \mathrm{cm}^{2}}",
            color=DRAW_INK,
            shift=LEFT * AREA_GBF_H_SHIFT,
        )
        area_gcb = _area_label_inside_at_y(
            area_gbf,
            tri_gcb,
            r"\mathbf{420\ \mathrm{cm}^{2}}",
            x_frac=AREA_GCB_AREA_X_FRAC,
        )
        area_gbf.set_z_index(5)
        area_gcb.set_z_index(5)
        self.play(FadeIn(area_gbf), run_time=0.45)
        self.play(FadeIn(area_gcb), run_time=0.45)
        self.next_slide()


class ParallelLinesAreaCompareDraw(Slide):
    """Nine beats: compare layout, relabel, k marks, areas, final teardown.

    Steps 1–5: outline → colour → grounded rotate → diagram cleanup → relabel.
    Steps 6–8: BF/5k, EA/2k, area labels 48 & 300 cm².
    Step 9:     remove every remaining mob one-by-one (reverse of steps 5–8).
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, labels, diagram = _add_base_diagram(self)
        v = _laid_out_vertices(lines)

        # Movable E, A, G labels (replace static diagram copies).
        lbl_e = _point_label("E", v["E"], UP + RIGHT * 0.15, DRAW_INK)
        lbl_a = _point_label("A", v["A"], UP + RIGHT * 0.25, DRAW_INK)
        lbl_g = _point_label("G", v["G"], RIGHT, DRAW_INK)
        _remove(self, labels["E"], labels["A"], labels["G"])

        # ── STEP 1 — △EAG and △GBF at original positions (outline only) ───────
        tri_eag = _triangle_outline(v["E"], v["A"], v["G"])
        tri_gbf = _triangle_outline(v["G"], v["B"], v["F"])
        eag_unit = VGroup(tri_eag, lbl_e, lbl_a, lbl_g)
        self.play(
            Create(tri_eag),
            Create(tri_gbf),
            FadeIn(lbl_e),
            FadeIn(lbl_a),
            FadeIn(lbl_g),
            run_time=0.85,
        )
        self.next_slide()

        # ── STEP 2 — Colour the two triangles ─────────────────────────────────
        self.play(
            tri_eag.animate.set_fill(COL_TRI_EAG, opacity=REGION_FILL_OPACITY),
            tri_gbf.animate.set_fill(COL_TRI_GBF, opacity=REGION_FILL_OPACITY),
            run_time=0.75,
        )
        self.next_slide()

        # ── STEP 3 — Rotate △EAG 180°; align ground with △GBF; shift left ─────
        self.play(
            Rotate(eag_unit, angle=PI, about_point=eag_unit.get_center()),
            run_time=0.7,
        )
        shift = _comparison_shift_grounded(tri_eag, tri_gbf, gap=COMPARE_GAP)
        self.play(eag_unit.animate.shift(shift), run_time=0.85)
        self.next_slide()

        # ── STEP 4 — Remove diagram ink and all labels; keep two triangles ────
        rt = 0.28
        # Remove: line EF (E → F)
        _remove(self, lines["seg_EF"])
        # Remove: line DB (D → B, diagonal)
        _remove(self, lines["diag_DB"])
        # Remove: line CG (C → G)
        _remove(self, lines["seg_CG"])
        # Remove: line AB (A → B)
        _remove(self, lines["right_AB"])
        # Remove: line DC (C → D)
        _remove(self, lines["left_DC"])
        # Remove: bottom parallel C — B — F
        _remove(self, lines["bottom_CF"])
        # Remove: top parallel D — E — A
        _remove(self, lines["top_DA"])
        # Remove: point labels D, C, B, F, H (diagram)
        _remove(self, labels["D"])
        _remove(self, labels["C"])
        _remove(self, labels["B"])
        _remove(self, labels["F"])
        _remove(self, labels["H"])
        # Remove: movable labels E, A, G (tracked with △EAG)
        _remove(self, lbl_e)
        _remove(self, lbl_a)
        _remove(self, lbl_g)
        self.next_slide()

        # ── STEP 5 — Relabel vertices on the two triangles ────────────────────
        # △EAG (red): G, A, E — △GBF (green): G, B, F (at current polygon verts).
        eag_verts = tri_eag.get_vertices()
        gbf_verts = tri_gbf.get_vertices()
        eag_c = tri_eag.get_center()
        gbf_c = tri_gbf.get_center()
        # Polygon built E, A, G — after rotate/shift: verts[0]=E, [1]=A, [2]=G
        lbl_g_eag = _label_at_vertex("G", eag_verts[2], eag_c)
        lbl_a_fin = _label_at_vertex("A", eag_verts[1], eag_c)
        lbl_e_fin = _label_at_vertex("E", eag_verts[0], eag_c)
        # Polygon built G, B, F
        lbl_g_gbf = _label_at_vertex("G", gbf_verts[0], gbf_c)
        lbl_b_fin = _label_at_vertex("B", gbf_verts[1], gbf_c)
        lbl_f_fin = _label_at_vertex("F", gbf_verts[2], gbf_c)
        self.play(
            FadeIn(lbl_g_eag),
            FadeIn(lbl_a_fin),
            FadeIn(lbl_e_fin),
            FadeIn(lbl_g_gbf),
            FadeIn(lbl_b_fin),
            FadeIn(lbl_f_fin),
            run_time=0.75,
        )
        self.next_slide()

        # ── STEP 6 — Highlight BF (yellow) + label 5k below midpoint ──────────
        gbf_verts = tri_gbf.get_vertices()
        bf_p1, bf_p2 = gbf_verts[1], gbf_verts[2]  # B → F on △GBF
        hi_bf = _highlight_seg(bf_p1, bf_p2, COL_BF)
        hi_bf.set_z_index(2)
        lbl_5k_bf = _length_label(r"5k", bf_p1, bf_p2, DOWN, ink=COL_BF)
        lbl_5k_bf.set_z_index(3)
        self.play(Create(hi_bf), run_time=0.65)
        self.play(FadeIn(lbl_5k_bf, scale=0.95), run_time=0.5)
        self.next_slide()

        # ── STEP 7 — Highlight EA (green) + label 2k below midpoint ─────────
        eag_verts = tri_eag.get_vertices()
        ea_p1, ea_p2 = eag_verts[0], eag_verts[1]  # E → A on △EAG
        hi_ea = _highlight_seg(ea_p1, ea_p2, COL_EA)
        hi_ea.set_z_index(2)
        lbl_2k_ea = _length_label(r"2k", ea_p1, ea_p2, DOWN, ink=COL_EA)
        lbl_2k_ea.set_z_index(3)
        self.play(Create(hi_ea), run_time=0.65)
        self.play(FadeIn(lbl_2k_ea, scale=0.95), run_time=0.5)
        self.next_slide()

        # ── STEP 8 — Area labels: 48 cm² in △EAG, 300 cm² in △GBF ───────────
        area_eag = _area_label_in_triangle(
            tri_eag,
            r"\mathbf{48\ \mathrm{cm}^{2}}",
            color=DRAW_INK,
            shift=LEFT * AREA_LABEL_H_SHIFT + DOWN * AREA_EAG_VERT_SHIFT,
        )
        area_gbf = _area_label_in_triangle(
            tri_gbf,
            r"\mathbf{300\ \mathrm{cm}^{2}}",
            color=DRAW_INK,
            shift=LEFT * AREA_GBF_H_SHIFT,
        )
        area_eag.set_z_index(4)
        area_gbf.set_z_index(4)
        self.play(FadeIn(area_eag), FadeIn(area_gbf), run_time=0.6)
        self.next_slide()

        # ── STEP 9 — Remove all elements one-by-one (reverse of steps 5–8) ────
        # Each FadeOut targets a single mobject — not a VGroup batch.
        rt = 0.28

        # Remove: area label 300 cm² (△GBF)
        _remove(self, area_gbf)
        # Remove: area label 48 cm² (△EAG)
        _remove(self, area_eag)
        # Remove: length label 2k (below EA)
        _remove(self, lbl_2k_ea)
        # Remove: green highlight on segment EA
        _remove(self, hi_ea)
        # Remove: length label 5k (below BF)
        _remove(self, lbl_5k_bf)
        # Remove: yellow highlight on segment BF
        _remove(self, hi_bf)
        # Remove: point label F (△GBF)
        _remove(self, lbl_f_fin)
        # Remove: point label B (△GBF)
        _remove(self, lbl_b_fin)
        # Remove: point label G (△GBF)
        _remove(self, lbl_g_gbf)
        # Remove: point label E (△EAG)
        _remove(self, lbl_e_fin)
        # Remove: point label A (△EAG)
        _remove(self, lbl_a_fin)
        # Remove: point label G (△EAG)
        _remove(self, lbl_g_eag)
        # Remove: green filled △GBF
        _remove(self, tri_gbf)
        # Remove: red filled △EAG
        _remove(self, tri_eag)
        self.next_slide()


class ParallelLinesDeBfParallelDraw(Slide):
    """Continuation from angle-marks step 7: // DEBF, cleanup, ∥ DB/EF, restore.

    Steps 0–3: base → // DE/BF → yellow **DE**/**BF** + 5k.
    Step 4: orange fill ▱**DEBF**.
    Step 5: remove HG, EA, AG, DC, HC, BC + labels H, A, G, C (one mob each).
    Step 6: double // arrows on **DB** (tip → D) and **EF** (tip → E).
    Step 7: restore full diagram ink + labels (keep orange ▱DEBF + ∥ DB/EF arrows).
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, labels, _diagram = _add_base_diagram(self)
        v = _laid_out_vertices(lines)
        top_da = lines["top_DA"]
        bot_cf = lines["bottom_CF"]
        cg = lines["seg_CG"]
        de_p1, de_p2 = _laid_out_subsegment(top_da, D, E, D, A)
        bf_p1, bf_p2 = _laid_out_subsegment(bot_cf, B, F, C, F)
        h_pt = _line_intersection(
            lines["diag_DB"].get_start(), lines["diag_DB"].get_end(),
            cg.get_start(), cg.get_end(),
        )
        hg_p1, hg_p2 = _laid_out_subsegment(cg, h_pt, v["G"], C, G)
        hc_p1, hc_p2 = _laid_out_subsegment(cg, v["C"], h_pt, C, G)

        self.play(Wait(0.01), run_time=0.01)
        self.next_slide()

        # ── STEP 1 — Parallel arrows on DE and BF ─────────────────────────────
        arr_de = _parallel_arrow_mark(de_p1, de_p2, ink=DRAW_INK)
        arr_bf = _parallel_arrow_mark(bf_p1, bf_p2, ink=DRAW_INK)
        arr_de.set_z_index(2)
        arr_bf.set_z_index(2)
        self.play(Create(arr_de), Create(arr_bf), run_time=0.75)
        self.next_slide()

        # ── STEP 2 — Highlight DE (yellow) + label 5k above ─────────────────
        hi_de = _highlight_seg(de_p1, de_p2, COL_DE)
        hi_de.set_z_index(2)
        lbl_de = _length_label(r"5k", de_p1, de_p2, UP, ink=COL_DE)
        lbl_de.set_z_index(3)
        self.play(Create(hi_de), run_time=0.65)
        self.play(FadeIn(lbl_de, scale=0.95), run_time=0.5)
        self.next_slide()

        # ── STEP 3 — Highlight BF (yellow) + label 5k below ─────────────────
        hi_bf = _highlight_seg(bf_p1, bf_p2, COL_BF)
        hi_bf.set_z_index(2)
        lbl_bf = _length_label(r"5k", bf_p1, bf_p2, DOWN, ink=COL_BF)
        lbl_bf.set_z_index(3)
        self.play(Create(hi_bf), run_time=0.65)
        self.play(FadeIn(lbl_bf, scale=0.95), run_time=0.5)
        self.next_slide()

        # ── STEP 4 — Shade ▱DEBF orange ─────────────────────────────────────
        quad_debf = _filled_quad(v["D"], v["E"], v["F"], v["B"], COL_DEBF)
        self.add(quad_debf)
        self.bring_to_back(quad_debf)
        self.play(FadeIn(quad_debf), run_time=0.75)
        self.next_slide()

        # ── STEP 5 — Remove segments (one mob each) ─────────────────────────
        rt = 0.28
        self.remove(cg)
        seg_hc = Line(hc_p1, hc_p2, color=DRAW_INK, stroke_width=STROKE)
        seg_hg = Line(hg_p1, hg_p2, color=DRAW_INK, stroke_width=STROKE)
        self.add(seg_hc, seg_hg)
        # Remove: segment HG (H → G on CG)
        _remove(self, seg_hg)
        _remove(self, labels["H"])
        # Remove: segment EA (E → A on top parallel)
        _remove(self, lines["top_DA"])
        _remove(self, labels["A"])
        # Remove: segment AG (A → G on AB)
        _remove(self, lines["right_AB"])
        _remove(self, labels["G"])
        # Remove: line DC (C → D)
        _remove(self, lines["left_DC"])
        # Remove: segment HC (H → C on CG)
        _remove(self, seg_hc)
        # Remove: segment BC (B → C on bottom parallel)
        _remove(self, lines["bottom_CF"])
        _remove(self, labels["C"])
        self.next_slide()

        # ── STEP 6 — Double // arrows on DB (tip → D) and EF (tip → E) ──────
        db = lines["diag_DB"]
        ef = lines["seg_EF"]
        db_d, db_b = db.get_start(), db.get_end()
        ef_e, ef_f = ef.get_start(), ef.get_end()
        arr_db = _double_parallel_arrow_mark(db_d, db_b)
        arr_ef = _double_parallel_arrow_mark(ef_e, ef_f)
        arr_db.set_z_index(2)
        arr_ef.set_z_index(2)
        self.play(Create(arr_db), Create(arr_ef), run_time=0.75)
        self.next_slide()

        # ── STEP 7 — Restore diagram ink + labels (keep orange + ∥ arrows) ──
        self.play(Create(lines["bottom_CF"]), run_time=rt)
        self.play(FadeIn(labels["C"], scale=0.95), run_time=rt)
        self.add(cg)
        self.play(Create(cg), run_time=rt)
        self.play(Create(lines["left_DC"]), run_time=rt)
        self.play(Create(lines["right_AB"]), run_time=rt)
        self.play(FadeIn(labels["G"], scale=0.95), run_time=rt)
        self.play(Create(lines["top_DA"]), run_time=rt)
        self.play(FadeIn(labels["A"], scale=0.95), run_time=rt)
        self.play(FadeIn(labels["H"], scale=0.95), run_time=rt)
        self.next_slide()


class ParallelLinesCgbAngleMarksDraw(Slide):
    """Continuation from `ParallelLinesDeBfParallelDraw` step 7 end frame.

    Step 0: copy of DeBf end (full ink, orange ▱DEBF, ∥ DB/EF, yellow 5k).
    Step 1: fade orange ▱**DEBF**.
    Step 2: move double // arrows from **DB** down to **HB** (tips → **H**).
    Step 3: remove yellow **DE**/**BF** + 5k labels; trim to △CHB/△CGF ink only.
    Step 4: purple ∠**CGF** + ∠**CHB**.
    Step 5: blue ∠**CFG** + ∠**CBH**.
    Step 6: green ∠**GCB**.
    Step 7: remove // marks on **HB** and **GF**.
    Step 8: duplicate △**CHB** (+ labels **C,H,B** + arcs) → shift up.
    Step 9: on original — remove **HB**, label **H**, arcs **CHB** + **CBH** (keep **B**).
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, labels, _diagram = _add_base_diagram(self)
        frame = _de_bf_parallel_end_frame(self, lines, labels)
        v = frame["v"]
        h_pt = frame["h_pt"]
        quad_debf = frame["quad_debf"]
        arr_db = frame["arr_db"]
        arr_de = frame["arr_de"]
        arr_bf = frame["arr_bf"]
        arr_ef = frame["arr_ef"]
        hi_de = frame["hi_de"]
        lbl_de = frame["lbl_de"]
        hi_bf = frame["hi_bf"]
        lbl_bf = frame["lbl_bf"]
        rt = 0.28
        ang_r = CGB_ANGLE_RADIUS

        self.play(Wait(0.01), run_time=0.01)
        self.next_slide()

        # ── STEP 1 — Remove orange ▱DEBF ────────────────────────────────────
        _remove(self, quad_debf)
        self.next_slide()

        # ── STEP 2 — Double // arrows: DB → HB (tips toward H) ──────────────
        arr_hb = _double_parallel_arrow_mark(h_pt, v["B"])
        arr_hb.set_z_index(2)
        _remove(self, arr_db)
        self.play(Create(arr_hb), run_time=0.5)
        self.next_slide()

        # ── STEP 3 — Remove DE/BF highlights; isolate △CHB + △CGF ink ─────
        _remove(self, hi_de)
        _remove(self, lbl_de)
        _remove(self, hi_bf)
        _remove(self, lbl_bf)
        _remove(self, arr_de)
        _remove(self, arr_bf)
        _cgb_isolate_chb_cgf_ink(self, lines, labels, v, h_pt, rt)
        self.next_slide()

        # ── STEP 4 — Purple ∠CGF and ∠CHB ───────────────────────────────────
        arcs = _build_cgb_angle_arcs(v, h_pt, ang_r)
        ang_cgf, ang_chb = arcs["cgf"], arcs["chb"]
        for mob in (*ang_cgf, *ang_chb):
            mob.set_z_index(2)
        self.play(
            *[FadeIn(m) for m in ang_cgf],
            *[FadeIn(m) for m in ang_chb],
            run_time=0.75,
        )
        self.next_slide()

        # ── STEP 5 — Blue ∠CFG and ∠CBH ─────────────────────────────────────
        ang_cfg, ang_cbh = arcs["cfg"], arcs["cbh"]
        for mob in (*ang_cfg, *ang_cbh):
            mob.set_z_index(2)
        self.play(
            *[FadeIn(m) for m in ang_cfg],
            *[FadeIn(m) for m in ang_cbh],
            run_time=0.75,
        )
        self.next_slide()

        # ── STEP 6 — Green ∠GCB ─────────────────────────────────────────────
        ang_gcb = arcs["gcb"]
        for mob in ang_gcb:
            mob.set_z_index(2)
        self.play(*[FadeIn(m) for m in ang_gcb], run_time=0.75)
        self.next_slide()

        # ── STEP 7 — Remove // marks on HB and GF ───────────────────────────
        for arrow in (arr_hb, arr_ef):
            _remove(self, arrow)
        self.next_slide()

        # ── STEP 8 — Duplicate △CHB and lift vertically ───────────────────
        ang_chb, ang_cbh = arcs["chb"], arcs["cbh"]
        chb_dup = _chb_triangle_copy(labels, v, h_pt)
        self.add(chb_dup)
        lift = _chb_lift_amount(chb_dup, v, h_pt)
        self.play(chb_dup.animate.shift(UP * lift), run_time=0.75)
        self.next_slide()

        # ── STEP 9 — Trim original: HB, H, ∠CHB, ∠CBH (keep label B) ──────
        _remove(self, lines["diag_DB"])
        _remove(self, labels["H"])
        for mob in ang_chb:
            _remove(self, mob)
        for mob in ang_cbh:
            _remove(self, mob)
        self.next_slide()


class ParallelLinesChbLiftDraw(Slide):
    """Continuation from `ParallelLinesCgbAngleMarksDraw` step 7 end frame.

    Step 0: copy of CgbAngleMarks step-7 end.
    Step 1: duplicate △**CHB** (+ labels **C,H,B** + arcs **GCB,CHB,CBH**) → shift up.
    Step 2: on original — remove **HB**, label **H**, arcs **CHB** + **CBH** (keep label **B**).
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, labels, _diagram = _add_base_diagram(self)
        frame = _cgb_angle_marks_end_frame(self, lines, labels)
        v = frame["v"]
        h_pt = frame["h_pt"]
        ang_gcb = frame["gcb"]
        ang_chb = frame["chb"]
        ang_cbh = frame["cbh"]
        rt = 0.28

        self.play(Wait(0.01), run_time=0.01)
        self.next_slide()

        # ── STEP 1 — Duplicate △CHB and lift vertically ─────────────────────
        chb_dup = _chb_triangle_copy(labels, v, h_pt)
        self.add(chb_dup)
        lift = _chb_lift_amount(chb_dup, v, h_pt)
        self.play(chb_dup.animate.shift(UP * lift), run_time=0.75)
        self.next_slide()

        # ── STEP 2 — Trim original: HB, H, ∠CHB, ∠CBH (keep label B) ───
        _remove(self, lines["diag_DB"])
        _remove(self, labels["H"])
        for mob in ang_chb:
            _remove(self, mob)
        for mob in ang_cbh:
            _remove(self, mob)
        self.next_slide()


class ParallelLinesChbRegionsDraw(Slide):
    """Continuation from `ParallelLinesChbLiftDraw` step 2 end frame.

    Step 0: ChbLift end (lifted △**HCB**, trimmed original **HB** / **H**).
    Step 1: blue **CB** + **7k** on lower **CB** and lifted **CB**.
    Step 2: yellow **BF** + **5k**.
    Step 3: fill △**GCB** (blue) + △**GBF** (green) + lifted △**HCB** (orange);
            area labels **420**, **300**, **245 cm²**.

  Full animation map: `docs/CHB_REGIONS.md` (search `# ── STEP` below).
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, labels, _diagram = _add_base_diagram(self)
        frame = _chb_lift_end_frame(self, lines, labels)
        v = frame["v"]
        seg_cb_dup: Line = frame["seg_cb_dup"]  # type: ignore[assignment]
        h_pt_lift = frame["h_pt_lift"]
        rt_k = 0.55
        rt_lbl = 0.45
        rt_bf = 0.65
        rt_fill = 0.8
        rt_area = 0.45

        # ── STEP 0 — Static ChbLift step-2 end ──────────────────────────────
        # On screen: white ink **C,G,B,F** + **CG,GB,GF,CB/BF**; lifted △**HCB**
        # (duplicate **C,H,B** + arcs **GCB,CHB,CBH**); original ∠**GCB** at **C**;
        # original **HB** / label **H** / ∠**CHB** / ∠**CBH** removed; label **B** kept.
        # | Animation | Mobject | Code |
        # | `Wait(0.01)` | (hold) | `_chb_lift_end_frame(self, lines, labels)` |
        self.play(Wait(0.01), run_time=0.01)
        self.next_slide()

        k_mobs = _build_chb_regions_k_highlights(v, seg_cb_dup)

        # ── STEP 1 — Both **CB** segments: blue highlight + 7k below ────────
        # Lower **CB**: `v["C"]` → `v["B"]` on bottom parallel.
        # Lifted **CB**: `seg_cb_dup` (duplicate △**HCB** base, already shifted up).
        # | # | Animation | Mobject | Colour / text |
        # | 1 | `Create` | `hi_cb_low` | blue overlay on lower **CB** |
        # | 2 | `FadeIn` | `lbl_7k_low` | blue **7k** below lower **CB** |
        # | 3 | `Create` | `hi_cb_lift` | blue overlay on lifted **CB** |
        # | 4 | `FadeIn` | `lbl_7k_lift` | blue **7k** below lifted **CB** |
        self.play(Create(k_mobs["hi_cb_low"]), run_time=rt_k)
        self.play(FadeIn(k_mobs["lbl_7k_low"], scale=0.95), run_time=rt_lbl)
        self.play(Create(k_mobs["hi_cb_lift"]), run_time=rt_k)
        self.play(FadeIn(k_mobs["lbl_7k_lift"], scale=0.95), run_time=rt_lbl)
        self.next_slide()

        # ── STEP 2 — **BF** yellow highlight + 5k below ─────────────────────
        # Segment: `v["B"]` → `v["F"]` on bottom parallel.
        # | # | Animation | Mobject | Colour / text |
        # | 1 | `Create` | `hi_bf` | yellow overlay on **BF** |
        # | 2 | `FadeIn` | `lbl_5k_bf` | yellow **5k** below **BF** |
        self.play(Create(k_mobs["hi_bf"]), run_time=rt_bf)
        self.play(FadeIn(k_mobs["lbl_5k_bf"], scale=0.95), run_time=rt_lbl)
        self.next_slide()

        # ── STEP 3 — △fills + area labels (420, 300, 245 cm²) ───────────────
        # Fills behind ink: blue △**GCB** (`G,C,B`), green △**GBF** (`G,B,F`),
        # orange lifted △**HCB** (`H_lift,C_lift,B_lift`).
        # Area labels: **300 cm²** in △**GBF**; **420 cm²** in △**GCB** (matched
        # height, same y as 300); **245 cm²** inside lifted △**HCB** (matched height,
        # local y via `AREA_HCB_Y_FRAC`, x via `AREA_HCB_X_FRAC`).
        # | # | Animation | Mobject |
        # | 1 | `FadeIn` × 3 | `tri_gcb`, `tri_gbf`, `tri_hcb` |
        # | 2 | `FadeIn` | `area_gbf` → **300 cm²** |
        # | 3 | `FadeIn` | `area_gcb` → **420 cm²** |
        # | 4 | `FadeIn` | `area_hcb` → **245 cm²** |
        fill_mobs = _build_chb_regions_fills_and_areas(
            v, h_pt_lift, k_mobs["cb_lift_p1"], k_mobs["cb_lift_p2"],
        )
        self.add(
            fill_mobs["tri_gcb"],
            fill_mobs["tri_gbf"],
            fill_mobs["tri_hcb"],
        )
        self.bring_to_back(
            fill_mobs["tri_gcb"],
            fill_mobs["tri_gbf"],
            fill_mobs["tri_hcb"],
        )
        self.play(
            FadeIn(fill_mobs["tri_gcb"]),
            FadeIn(fill_mobs["tri_gbf"]),
            FadeIn(fill_mobs["tri_hcb"]),
            run_time=rt_fill,
        )
        self.play(FadeIn(fill_mobs["area_gbf"]), run_time=rt_area)
        self.play(FadeIn(fill_mobs["area_gcb"]), run_time=rt_area)
        self.play(FadeIn(fill_mobs["area_hcb"]), run_time=rt_area)
        self.next_slide()


class ParallelLinesChbRegionsContDraw(Slide):
    """Continuation from `ParallelLinesChbRegionsDraw` step 3 end frame.

    Step 0: ChbRegions step-3 end.
    Step 1: remove ∠**CGF**, ∠**CFG**, duplicate ∠**CHB**/**CBH**; keep ∠**GCB**.
    Step 2: (hold) keep **F**, **GF**, **BF**/**5k** ink + green △**GBF**.
    Step 3: remove green △**GBF** + **300 cm²** (keep **245 cm²** on lifted △**HCB**).
    Step 4: shift lifted △**HCB** down until both **CB** segments coincide (**245** moves with it).
    Step 5: orange △**HCB** → red △**HBG** + **175 cm²**; remove **420 cm²** + blue △**GCB** fill.

  Full map: `docs/CHB_REGIONS_CONT.md` (search `# ── STEP` below).
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, labels, _diagram = _add_base_diagram(self)
        frame = _chb_regions_end_frame(self, lines, labels)
        v = frame["v"]
        h_pt = frame["h_pt"]
        lift = float(frame["lift"])
        chb_dup = frame["chb_dup"]
        rt = 0.28

        # ── STEP 0 — Static ChbRegions step-3 end ───────────────────────────
        # | Animation | Code |
        # | `Wait(0.01)` | `_chb_regions_end_frame(self, lines, labels)` |
        self.play(Wait(0.01), run_time=0.01)
        self.next_slide()

        # ── STEP 1 — Remove ∠CGF, ∠CFG, duplicate ∠CHB/∠CBH; keep ∠GCB ──
        # **Keep:** green ∠**GCB** at **C** (`ang_gcb` + duplicate at **C**).
        # **Remove:** purple ∠**CGF** at **G**; blue ∠**CFG** at **F**; duplicate
        # ∠**CHB** at **H** and ∠**CBH** at **B** on lifted copy.
        # | # | Animation | Mobject |
        # | 1…2 | `FadeOut` | each mob in `ang_cgf` (∠**CGF** / **BGF** at **G**) |
        # | 3…4 | `FadeOut` | each mob in `ang_cfg` (∠**CFG** at **F**) |
        # | 5…8 | `FadeOut` | `_chb_dup_angle_mobs(chb_dup, include_gcb=False)` |
        for mob in _angle_group_mobs(frame["ang_cgf"]):  # type: ignore[arg-type]
            _remove(self, mob)
        for mob in _angle_group_mobs(frame["ang_cfg"]):  # type: ignore[arg-type]
            _remove(self, mob)
        for mob in _chb_dup_angle_mobs(chb_dup, include_gcb=False):
            _remove(self, mob)
        self.next_slide()

        # ── STEP 2 — Keep **F**, **GF**, **BF**/**5k** (no ink removal) ───────
        self.play(Wait(0.01), run_time=0.01)
        self.next_slide()

        # ── STEP 3 — Remove green △**GBF** + **300 cm²** (keep **245**) ───────
        _remove(self, frame["tri_gbf"])
        _remove(self, frame["area_gbf"])
        self.next_slide()

        # ── STEP 4 — Lower lifted △**HCB** until both **CB** coincide ───────
        merge_shift = VGroup(
            chb_dup,
            frame["hi_cb_lift"],
            frame["lbl_7k_lift"],
            frame["tri_hcb"],
            frame["area_hcb"],
        )
        self.play(merge_shift.animate.shift(DOWN * lift), run_time=0.75)
        _remove(self, frame["hi_cb_lift"], frame["lbl_7k_lift"])
        self.next_slide()

        # ── STEP 5 — Red △**HBG** + **175 cm²**; drop **420** + blue △**GCB** ─
        hbg = _build_chb_hbg_final_mobs(v, h_pt)
        tri_hbg = hbg["tri_hbg"]
        area_hbg = hbg["area_hbg"]
        self.add(tri_hbg)
        self.bring_to_back(tri_hbg)
        _remove(self, frame["tri_hcb"], frame["area_hcb"], frame["tri_gcb"], frame["area_gcb"])
        self.play(FadeIn(tri_hbg), run_time=0.8)
        self.play(FadeIn(area_hbg), run_time=0.45)
        self.next_slide()


class ParallelLinesChbHbgRestoreDraw(Slide):
    """Continuation from `ParallelLinesChbRegionsContDraw` step 5 end frame.

    Step 0: ChbRegionsCont step-5 end (red △**HBG** + **175 cm²** only).
    Step 1: remove all remaining angle arcs (∠**GCB** at **C**).
    Step 2: restore full graph ink + labels **D,E,A,F,H**; drop duplicate △**HCB** ink.
    Step 3: `Create` // marks on **DE**/**BF** and **DB**/**EF**.

  Full map: `docs/CHB_HBG_RESTORE.md` (search `# ── STEP` below).
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, labels, _diagram = _add_base_diagram(self)
        frame = _chb_regions_cont_end_frame(self, lines, labels)
        v = frame["v"]
        chb_dup = frame["chb_dup"]
        tri_hbg = frame["tri_hbg"]
        area_hbg = frame["area_hbg"]
        rt = 0.28

        # ── STEP 0 — Static ChbRegionsCont step-5 end ───────────────────────
        # On screen: merged △**HCB** (`chb_dup`), red △**HBG** + **175 cm²**,
        # **C,G,B** + duplicate **H**, **CB**/**7k**, **CG**/**GB**; trimmed **CB**
        # only; ∠**GCB** at **C**; no **F**/**GF**/**BF**.
        # | Animation | Code |
        # | `Wait(0.01)` | `_chb_regions_cont_end_frame(self, lines, labels)` |
        self.play(Wait(0.01), run_time=0.01)
        self.next_slide()

        # ── STEP 1 — Remove all angle arcs ──────────────────────────────────
        # **Remove:** green ∠**GCB** at **C** (original + duplicate on `chb_dup`).
        # **Keep:** red △**HBG**, **175 cm²**, △**HCB** ink.
        # | # | Animation | Mobject |
        # | 1…2 | `FadeOut` | each mob in `ang_gcb` |
        # | 3…4 | `FadeOut` | duplicate ∠**GCB** on `chb_dup` |
        for mob in _angle_group_mobs(frame["ang_gcb"]):  # type: ignore[arg-type]
            _remove(self, mob)
        for mob in _chb_dup_angle_mobs(chb_dup, include_gcb=True):
            _remove(self, mob)
        self.next_slide()

        # ── STEP 2 — Restore full parallel-lines graph ────────────────────────
        # **Restore:** **DC**, **DA**, **AB**, **DB**, **EF**, **CG**, **CF** + labels
        # **D,E,A,F,H**. **Drop:** duplicate △**HCB** ink (now covered by full lines).
        # **Keep:** red △**HBG** (`tri_hbg`), **175 cm²**, **CB**/**7k**, **C,G,B** labels.
        # | # | Animation | Mobject |
        # | 1 | `FadeIn` | `labels["D"]`, `labels["E"]`, `labels["A"]` |
        # | 2 | `Create` | `left_DC`, `top_DA` |
        # | 3 | `Create` | `diag_DB`, `seg_EF`, `right_AB`, `bottom_CF`, `seg_CG` |
        # | 4 | `FadeIn` | `labels["F"]`, `labels["H"]` |
        # | 5 | `FadeOut` | `chb_dup` lines + duplicate **C,H,B** labels |
        _restore_full_parallel_graph_ink(lines, labels, v)
        self.play(
            FadeIn(labels["D"], scale=0.95),
            FadeIn(labels["E"], scale=0.95),
            FadeIn(labels["A"], scale=0.95),
            run_time=0.5,
        )
        self.play(
            Create(lines["left_DC"]),
            Create(lines["top_DA"]),
            run_time=0.65,
        )
        self.play(
            Create(lines["diag_DB"]),
            Create(lines["right_AB"]),
            Create(lines["seg_CG"]),
            run_time=0.75,
        )
        self.play(
            FadeIn(labels["H"], scale=0.95),
            run_time=0.45,
        )
        dup_lines = VGroup(
            chb_dup[CHB_DUP_SEG_CH],
            chb_dup[CHB_DUP_SEG_HB],
            chb_dup[CHB_DUP_SEG_CB],
        )
        dup_lbls = VGroup(
            chb_dup[CHB_DUP_LBL_C],
            chb_dup[CHB_DUP_LBL_H],
            chb_dup[CHB_DUP_LBL_B],
        )
        _remove(self, dup_lines, dup_lbls)
        self.next_slide()

        # ── STEP 3 — Parallel marks on horizontals + slants ───────────────────
        # **DE** ∥ **BF** (single //); **DB** ∥ **EF** (double //).
        # | # | Animation | Mobject |
        # | 1 | `Create` × 4 | `arr_de`, `arr_bf`, `arr_db`, `arr_ef` |
        arrows = _build_parallel_graph_arrow_marks(lines, v)
        self.play(
            Create(arrows["arr_de"]),
            Create(arrows["arr_bf"]),
            run_time=0.55,
        )
        self.play(
            Create(arrows["arr_db"]),
            Create(arrows["arr_ef"]),
            run_time=0.55,
        )
        self.next_slide()


class ParallelLinesChbHbgMarksDraw(Slide):
    """Continuation from `ParallelLinesChbHbgRestoreDraw` step 3 end frame.

    Step 0: HbgRestore step-3 end (full graph, // **DE**/**BF**/**DB**/**EF**).
    Step 1: remove // on **BF**, **EF** (G–F slant), **DB**.
    Step 2: double // on **CD** and **AB** (matched, tips toward **D** / **A**).
    Step 3: teal fill △**CDH**.
    Steps 4–6: three angle-pair highlights (∠**CDB**/∠**GBH**, ∠**DCH**/∠**HGB**, ∠**DHC**/∠**GHB**).

    Full map: `docs/CHB_HBG_MARKS.md` (search `# ── STEP` below).
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, labels, _diagram = _add_base_diagram(self)
        frame = _chb_hbg_restore_end_frame(self, lines, labels)
        v = frame["v"]
        h_pt = frame["h_pt"]
        rt = 0.28

        # ── STEP 0 — Static HbgRestore step-3 end ─────────────────────────────
        # Full graph, red △**HBG** + **175 cm²**, **CB**/**7k** (removed step 1); // on **DE**/**BF**/**DB**/**EF**.
        # | Animation | Code |
        # | `Wait(0.01)` | `_chb_hbg_restore_end_frame(self, lines, labels)` |
        self.play(Wait(0.01), run_time=0.01)
        self.next_slide()

        # ── STEP 1 — Remove // on BF, EF, DB; drop CB / 7k ───────────────────
        # **Remove:** `arr_bf`, `arr_ef` (**EF** / G–F portion of parallel pair), `arr_db`,
        # blue **CB** highlight, **7k** label.
        # **Keep:** `arr_de`, red △**HBG**, **175 cm²**.
        # | Animation | Mobject |
        # | `FadeOut` × 5 | `arr_bf`, `arr_ef`, `arr_db`, `hi_cb_low`, `lbl_7k_low` |
        _remove(self, frame["arr_bf"], frame["arr_ef"], frame["arr_db"], frame["hi_cb_low"], frame["lbl_7k_low"])
        self.next_slide()

        # ── STEP 2 — Revised parallel marks ───────────────────────────────────
        # Matched double // on **CD** and **AB** (tips toward **D** / **A**); no // on **GB**.
        # | Animation | Mobject |
        # | `Create` × 2 | `arr_cd`, `arr_ab` |
        new_arrows = _build_chb_hbg_marks_arrow_marks(v)
        self.play(
            Create(new_arrows["arr_cd"]),
            Create(new_arrows["arr_ab"]),
            run_time=0.55,
        )
        self.next_slide()

        # ── STEP 3 — Teal △CDH ──────────────────────────────────────────────
        # | Animation | Mobject |
        # | `FadeIn` | `tri_cdh` (vertices **C**, **D**, **H**) |
        tri_cdh = _filled_triangle(v["C"], v["D"], h_pt, COL_TRI_CDH)
        self.add(tri_cdh)
        self.bring_to_back(tri_cdh)
        self.play(FadeIn(tri_cdh), run_time=0.5)
        self.next_slide()

        # ── STEP 4 — ∠CDB and ∠GBH (gold) ───────────────────────────────────
        arcs = _build_chb_hbg_marks_angle_arcs(v, h_pt)
        self.play(
            Create(arcs["ang_cdb"]),
            Create(arcs["ang_gbh"]),
            run_time=0.55,
        )
        self.next_slide()

        # ── STEP 5 — ∠DCH and ∠HGB (pink) ─────────────────────────────────────
        self.play(
            Create(arcs["ang_dch"]),
            Create(arcs["ang_hgb"]),
            run_time=0.55,
        )
        self.next_slide()

        # ── STEP 6 — ∠DHC and ∠GHB (maroon) ───────────────────────────────────
        self.play(
            Create(arcs["ang_dhc"]),
            Create(arcs["ang_ghb"]),
            run_time=0.55,
        )
        self.next_slide()


class ParallelLinesChbHbgKRegionsDraw(Slide):
    """Continuation from `ParallelLinesChbHbgMarksDraw` step 6 end frame.

    Step 0: ChbHbgMarks step-6 end (full graph + △**CDH** + angle pairs + △**HBG**).
    Step 1: pink △**EAG** and green △**GBF** fills.
    Step 2: green **EA**/**AG** + **2k** (above / right).
    Step 3: yellow **BF**/**BG** + **5k** (below / right).
    Step 4: blue **DC** + **7k** (left).

    Full map: `docs/CHB_HBG_K_REGIONS.md` (search `# ── STEP` below).
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, labels, _diagram = _add_base_diagram(self)
        frame = _chb_hbg_marks_end_frame(self, lines, labels)
        rt = 0.28

        # ── STEP 0 — Static ChbHbgMarks step-6 end ────────────────────────────
        # | Animation | Code |
        # | `Wait(0.01)` | `_chb_hbg_marks_end_frame(self, lines, labels)` |
        self.play(Wait(0.01), run_time=0.01)
        self.next_slide()

        v = frame["v"]
        k_mobs = _build_chb_hbg_k_region_mobs(v)  # type: ignore[arg-type]
        tri_eag = k_mobs["tri_eag"]
        tri_gbf = k_mobs["tri_gbf"]

        # ── STEP 1 — △EAG (pink) and △GBF (green) ─────────────────────────────
        # | Animation | Mobject |
        # | `FadeIn` × 2 | `tri_eag`, `tri_gbf` |
        self.add(tri_eag, tri_gbf)
        self.bring_to_back(tri_eag, tri_gbf)
        self.play(FadeIn(tri_eag), FadeIn(tri_gbf), run_time=0.55)
        self.next_slide()

        # ── STEP 2 — Green EA / AG + 2k ───────────────────────────────────────
        # | # | Animation | Mobject |
        # | 1 | `Create` | `hi_ea` |
        # | 2 | `FadeIn` | `lbl_2k_ea` above **EA** |
        # | 3 | `Create` | `hi_ag` |
        # | 4 | `FadeIn` | `lbl_2k_ag` right of **AG** |
        self.play(Create(k_mobs["hi_ea"]), run_time=rt)
        self.play(FadeIn(k_mobs["lbl_2k_ea"], scale=0.95), run_time=0.45)
        self.play(Create(k_mobs["hi_ag"]), run_time=rt)
        self.play(FadeIn(k_mobs["lbl_2k_ag"], scale=0.95), run_time=0.45)
        self.next_slide()

        # ── STEP 3 — Yellow BF / BG + 5k ──────────────────────────────────────
        # | # | Animation | Mobject |
        # | 1 | `Create` | `hi_bf` |
        # | 2 | `FadeIn` | `lbl_5k_bf` below **BF** |
        # | 3 | `Create` | `hi_bg` |
        # | 4 | `FadeIn` | `lbl_5k_bg` right of **BG** |
        self.play(Create(k_mobs["hi_bf"]), run_time=rt)
        self.play(FadeIn(k_mobs["lbl_5k_bf"], scale=0.95), run_time=0.45)
        self.play(Create(k_mobs["hi_bg"]), run_time=rt)
        self.play(FadeIn(k_mobs["lbl_5k_bg"], scale=0.95), run_time=0.45)
        self.next_slide()

        # ── STEP 4 — Blue DC + 7k (left) ──────────────────────────────────────
        # | # | Animation | Mobject |
        # | 1 | `Create` | `hi_dc` |
        # | 2 | `FadeIn` | `lbl_7k_dc` left of **DC** |
        self.play(Create(k_mobs["hi_dc"]), run_time=rt)
        self.play(FadeIn(k_mobs["lbl_7k_dc"], scale=0.95), run_time=0.45)
        self.next_slide()


class ParallelLinesChbHbgKTrimDraw(Slide):
    """Continuation from `ParallelLinesChbHbgKRegionsDraw` step 4 end frame.

    Step 0: ChbHbgKRegions step-4 end (all k labels + △fills from that deck).
    Step 1: remove pink △**EAG**, green **EA**/**2k**, yellow **BF**/**5k**, green △**GBF**.
    Step 2: **343 cm²** inside teal △**CDH**.
    Step 3: CDH-only frame — **D**, **H**, **C**, △**CDH**, **343 cm²**, white **DC**/**DH**/**HC**.

    Chain terminus. Next deck: step 0 via `_chb_hbg_k_cdh_only_end_frame()`.
    Full map: `docs/CHB_HBG_K_TRIM.md` · chain: `docs/CHB_DECK_CHAIN.md`
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, labels, _diagram = _add_base_diagram(self)
        frame = _chb_hbg_k_regions_end_frame(self, lines, labels)
        rt = 0.55

        # ── STEP 0 — Static ChbHbgKRegions step-4 end ───────────────────────
        # | Animation | Code |
        # | `Wait(0.01)` | `_chb_hbg_k_regions_end_frame(self, lines, labels)` |
        self.play(Wait(0.01), run_time=0.01)
        self.next_slide()

        # ── STEP 1 — Trim △EAG / △GBF and EA / BF ink ───────────────────────
        # **Remove:** pink △**EAG**, green **EA** + **2k**, yellow **BF** + **5k**, green △**GBF**.
        # **Keep:** green **AG** + **2k**, yellow **BG** + **5k**, blue **DC** + **7k**;
        # △**CDH**, angle pairs, red △**HBG** + **175 cm²**, // marks.
        # | Animation | Mobject |
        # | `FadeOut` × 6 | `tri_eag`, `hi_ea`, `lbl_2k_ea`, `hi_bf`, `lbl_5k_bf`, `tri_gbf` |
        _remove(self, frame["tri_eag"], frame["hi_ea"], frame["lbl_2k_ea"], frame["hi_bf"], frame["lbl_5k_bf"], frame["tri_gbf"])
        self.next_slide()

        # ── STEP 2 — 343 cm² inside △CDH ──────────────────────────────────────
        # | Animation | Mobject |
        # | `FadeIn` | `area_cdh` → **343 cm²** inside teal △**CDH** |
        tri_cdh = frame["tri_cdh"]
        area_cdh = _area_label_in_triangle(
            tri_cdh,  # type: ignore[arg-type]
            r"\mathbf{343\ \mathrm{cm}^{2}}",
            shift=RIGHT * AREA_CDH_H_SHIFT,
        )
        area_cdh.set_z_index(5)
        self.play(FadeIn(area_cdh), run_time=0.45)
        self.next_slide()

        # ── STEP 3 — CDH-only frame ───────────────────────────────────────────
        # **Keep:** labels **D**, **H**, **C**; teal △**CDH**; **343 cm²**; white **DC**/**DH**/**HC**.
        # **Remove:** other lines/labels, △**HBG**/**175 cm²**, k ink, // marks, angle arcs.
        # | # | Action | Mobject |
        # | 1 | trim | `left_DC`, `diag_DB`→**DH**, `seg_CG`→**HC** |
        # | 2 | `FadeOut` × N | `_chb_hbg_k_final_cleanup_mobs(...)` |
        _trim_cdh_triangle_ink(lines, frame["v"], frame["h_pt"])  # type: ignore[arg-type]
        cleanup = _chb_hbg_k_final_cleanup_mobs(frame, lines, labels)
        _remove(self, *cleanup)
        self.next_slide()


class ParallelLinesEagGbfAnglesDraw(Slide):
    """Isolated △EAG / △GBF through card 3 side-by-side area compare.

    Steps 0–3: card 2 — isolate, three AAA angle pairs.
    Steps 4–9: card 3 — pull △EAG, relabel, k marks, areas (lines stay).
    """

    def construct(self):
        self.camera.background_color = DRAW_BG
        lines, labels, _diagram = _add_base_diagram(self)
        v = _laid_out_vertices(lines)

        # Trim horizontals to **EA** and **BF** before the isolated reveal.
        lines["top_DA"].put_start_and_end_on(v["E"], v["A"])
        lines["bottom_CF"].put_start_and_end_on(v["B"], v["F"])
        ea_p1, ea_p2 = v["E"], v["A"]
        bf_p1, bf_p2 = v["B"], v["F"]

        tri_eag = _filled_triangle(v["E"], v["A"], v["G"], COL_TRI_EAG)
        tri_gbf = _filled_triangle(v["G"], v["B"], v["F"], COL_TRI_GBF)
        self.add(tri_eag, tri_gbf)
        self.bring_to_back(tri_eag, tri_gbf)

        hi_ea = _highlight_seg(ea_p1, ea_p2, COL_EA)
        lbl_ea = _length_label(r"2k", ea_p1, ea_p2, UP, ink=COL_EA)
        hi_bf = _highlight_seg(bf_p1, bf_p2, COL_BF)
        lbl_bf = _length_label(r"5k", bf_p1, bf_p2, DOWN, ink=COL_BF)
        arr_ea = _parallel_arrow_mark(v["E"], v["A"], ink=DRAW_INK)
        arr_bf = _parallel_arrow_mark(v["B"], v["F"], ink=DRAW_INK)

        # ── STEP 0 — Isolated △EAG + △GBF (matches main sim end state) ─────
        rt = 0.30
        self.play(
            FadeIn(tri_eag),
            FadeIn(tri_gbf),
            FadeIn(hi_ea),
            FadeIn(lbl_ea),
            FadeIn(hi_bf),
            FadeIn(lbl_bf),
            Create(arr_ea),
            Create(arr_bf),
            run_time=0.75,
        )
        _remove(self, lines["left_DC"])
        _remove(self, lines["diag_DB"])
        _remove(self, lines["seg_CG"])
        _remove(self, labels["D"])
        _remove(self, labels["C"])
        _remove(self, labels["H"])
        self.next_slide()

        angle_mobs = _eag_gbf_angle_pairs_steps(self, v)
        _area_compare_from_isolated_steps(
            self,
            lines,
            labels,
            v,
            tri_eag,
            tri_gbf,
            angle_mobs,
            arr_ea,
            arr_bf,
            hi_ea,
            lbl_ea,
            hi_bf,
            lbl_bf,
        )
