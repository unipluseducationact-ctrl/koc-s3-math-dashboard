"""Equal height / equal base triangle ratio lab — Manim Slides for Geometry Lab."""
from __future__ import annotations

import numpy as np
from manim import *
from manim_slides import Slide

DRAW_BG = BLACK
DRAW_INK = WHITE
COL_TRI_1 = BLUE
COL_TRI_2 = TEAL
STROKE = 2.8
FONT = 36


def _tri(points: list[np.ndarray], color: ManimColor, fill: float = 0.28) -> Polygon:
    return Polygon(*points, stroke_color=color, stroke_width=STROKE, fill_color=color, fill_opacity=fill)


def _height_seg(top: np.ndarray, foot: np.ndarray, color: ManimColor) -> DashedLine:
    return DashedLine(top, foot, color=color, stroke_width=2.2, dash_length=0.12)


def _bracket_label(p1: np.ndarray, p2: np.ndarray, tex: str, direction=DOWN, color=DRAW_INK) -> MathTex:
    mid = (p1 + p2) / 2
    return MathTex(tex, color=color, font_size=FONT).next_to(mid, direction, buff=0.22)


class EqualHeightTrianglesDraw(Slide):
    """Shared apex; bases on one line — area ratio = base ratio."""

    def construct(self):
        self.camera.background_color = DRAW_BG

        base_y = 0.0
        h = 2.0
        b1, b2, gap = 2.4, 1.8, 0.45
        span = b1 + gap + b2
        x0 = -span / 2
        apex = np.array([0.0, base_y + h, 0.0])
        b1a = np.array([x0, base_y, 0.0])
        b1b = np.array([x0 + b1, base_y, 0.0])
        b2a = np.array([x0 + b1 + gap, base_y, 0.0])
        b2b = np.array([x0 + b1 + gap + b2, base_y, 0.0])
        foot = np.array([apex[0], base_y, 0.0])

        base_line = Line(np.array([x0 - 0.6, base_y, 0.0]), np.array([x0 + span + 0.6, base_y, 0.0]), color=GRAY_B)
        tri1 = _tri([apex, b1a, b1b], COL_TRI_1)
        tri2 = _tri([apex, b2a, b2b], COL_TRI_2)
        height = _height_seg(apex, foot, COL_TRI_1)
        apex_dot = Dot(apex, color=COL_TRI_1, radius=0.06)

        lbl_apex = MathTex(r"A\ \text{(shared apex)}", color=DRAW_INK, font_size=32).next_to(apex, UP, buff=0.18)
        lbl_h = MathTex(r"h = 200", color=COL_TRI_1, font_size=FONT).next_to(height, RIGHT, buff=0.2)
        lbl_b1 = _bracket_label(b1a, b1b, r"b_1 = 120", DOWN, COL_TRI_1)
        lbl_b2 = _bracket_label(b2a, b2b, r"b_2 = 90", DOWN, COL_TRI_2)
        a1 = 0.5 * b1 * h * 100  # display units² (120*200/2)
        a2 = 0.5 * b2 * h * 100
        lbl_a1 = MathTex(rf"A_1 = {a1:.0f}", color=COL_TRI_1, font_size=32).move_to((apex + b1a + b1b) / 3 + LEFT * 0.35)
        lbl_a2 = MathTex(rf"A_2 = {a2:.0f}", color=COL_TRI_2, font_size=32).move_to((apex + b2a + b2b) / 3 + RIGHT * 0.35)
        ratio = MathTex(
            r"\dfrac{A_1}{A_2} = \dfrac{b_1}{b_2} = \dfrac{120}{90} = 4 : 3",
            color=DRAW_INK,
            font_size=38,
        ).to_edge(UP)

        self.play(FadeIn(base_line), run_time=0.4)
        self.next_slide()
        self.play(Create(tri1), Create(tri2), FadeIn(apex_dot), run_time=0.9)
        self.next_slide()
        self.play(Create(height), FadeIn(lbl_h), FadeIn(lbl_apex), run_time=0.7)
        self.next_slide()
        self.play(FadeIn(lbl_b1), FadeIn(lbl_b2), run_time=0.6)
        self.next_slide()
        self.play(FadeIn(lbl_a1), FadeIn(lbl_a2), run_time=0.6)
        self.next_slide()
        self.play(Write(ratio), run_time=0.8)
        self.next_slide()


class EqualBaseSameSideDraw(Slide):
    """Shared base; apexes on the same side — area ratio = height ratio."""

    def construct(self):
        self.camera.background_color = DRAW_BG

        base_y = 0.0
        b = 2.2
        h1, h2 = 1.3, 0.95
        bx1 = np.array([-b / 2, base_y, 0.0])
        bx2 = np.array([b / 2, base_y, 0.0])
        a1 = bx1 + LEFT * 0.65 + UP * h1
        a2 = bx2 + RIGHT * 0.65 + UP * h2
        foot1 = np.array([a1[0], base_y, 0.0])
        foot2 = np.array([a2[0], base_y, 0.0])

        base_line = Line(bx1 + LEFT * 0.5, bx2 + RIGHT * 0.5, color=GRAY_B)
        tri1 = _tri([a1, bx1, bx2], COL_TRI_1)
        tri2 = _tri([a2, bx1, bx2], COL_TRI_2)
        ht1 = _height_seg(a1, foot1, COL_TRI_1)
        ht2 = _height_seg(a2, foot2, COL_TRI_2)

        lbl_b = _bracket_label(bx1, bx2, r"b = 220\ \text{(shared)}", DOWN, DRAW_INK)
        lbl_h1 = MathTex(r"h_1 = 130", color=COL_TRI_1, font_size=FONT).next_to(ht1, LEFT, buff=0.18)
        lbl_h2 = MathTex(r"h_2 = 95", color=COL_TRI_2, font_size=FONT).next_to(ht2, RIGHT, buff=0.18)
        area1 = 0.5 * b * h1 * 100
        area2 = 0.5 * b * h2 * 100
        lbl_a1 = MathTex(rf"A_1 = {area1:.0f}", color=COL_TRI_1, font_size=32).move_to((a1 + bx1 + bx2) / 3 + LEFT * 0.55)
        lbl_a2 = MathTex(rf"A_2 = {area2:.0f}", color=COL_TRI_2, font_size=32).move_to((a2 + bx1 + bx2) / 3 + RIGHT * 0.55)
        ratio = MathTex(
            r"\dfrac{A_1}{A_2} = \dfrac{h_1}{h_2} = \dfrac{130}{95} = 26 : 19",
            color=DRAW_INK,
            font_size=38,
        ).to_edge(UP)

        self.play(FadeIn(base_line), run_time=0.4)
        self.next_slide()
        self.play(Create(tri1), Create(tri2), run_time=0.9)
        self.next_slide()
        self.play(Create(ht1), Create(ht2), FadeIn(lbl_h1), FadeIn(lbl_h2), run_time=0.75)
        self.next_slide()
        self.play(FadeIn(lbl_b), run_time=0.5)
        self.next_slide()
        self.play(FadeIn(lbl_a1), FadeIn(lbl_a2), run_time=0.6)
        self.next_slide()
        self.play(Write(ratio), run_time=0.8)
        self.next_slide()


class EqualBaseOppositeDraw(Slide):
    """Shared base; apexes on opposite sides — area ratio = height ratio."""

    def construct(self):
        self.camera.background_color = DRAW_BG

        base_y = 0.0
        b = 2.2
        h1, h2 = 1.3, 0.95
        bx1 = np.array([-b / 2, base_y, 0.0])
        bx2 = np.array([b / 2, base_y, 0.0])
        mid = (bx1 + bx2) / 2
        a1 = mid + UP * h1
        a2 = mid + DOWN * h2
        foot1 = mid.copy()
        foot2 = mid.copy()

        base_line = Line(bx1 + LEFT * 0.5, bx2 + RIGHT * 0.5, color=GRAY_B)
        tri1 = _tri([a1, bx1, bx2], COL_TRI_1)
        tri2 = _tri([a2, bx1, bx2], COL_TRI_2)
        ht1 = _height_seg(a1, foot1, COL_TRI_1)
        ht2 = _height_seg(a2, foot2, COL_TRI_2)

        lbl_b = _bracket_label(bx1, bx2, r"b = 220\ \text{(shared)}", UP, DRAW_INK)
        lbl_h1 = MathTex(r"h_1 = 130", color=COL_TRI_1, font_size=FONT).next_to(ht1, LEFT, buff=0.18)
        lbl_h2 = MathTex(r"h_2 = 95", color=COL_TRI_2, font_size=FONT).next_to(ht2, RIGHT, buff=0.18)
        lbl_a1 = MathTex(r"A_1\ \text{(above)}", color=COL_TRI_1, font_size=30).next_to(a1, UP, buff=0.12)
        lbl_a2 = MathTex(r"A_2\ \text{(below)}", color=COL_TRI_2, font_size=30).next_to(a2, DOWN, buff=0.12)
        area1 = 0.5 * b * h1 * 100
        area2 = 0.5 * b * h2 * 100
        lbl_areas = MathTex(
            rf"A_1 = {area1:.0f},\quad A_2 = {area2:.0f}",
            color=DRAW_INK,
            font_size=34,
        ).to_edge(DOWN)
        ratio = MathTex(
            r"\dfrac{A_1}{A_2} = \dfrac{h_1}{h_2}\ \text{(perpendicular heights)}",
            color=DRAW_INK,
            font_size=36,
        ).to_edge(UP)

        self.play(FadeIn(base_line), run_time=0.4)
        self.next_slide()
        self.play(Create(tri1), Create(tri2), run_time=0.9)
        self.next_slide()
        self.play(Create(ht1), Create(ht2), FadeIn(lbl_h1), FadeIn(lbl_h2), run_time=0.75)
        self.next_slide()
        self.play(FadeIn(lbl_b), FadeIn(lbl_a1), FadeIn(lbl_a2), run_time=0.6)
        self.next_slide()
        self.play(FadeIn(lbl_areas), run_time=0.55)
        self.next_slide()
        self.play(Write(ratio), run_time=0.8)
        self.next_slide()
