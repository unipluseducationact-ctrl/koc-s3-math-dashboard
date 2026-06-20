"""Geometric (area-model) proofs of the three factorization identities.

Scenes (each a Manim-Slides deck)
---------------------------------
  PerfectSquareSum     (a+b)^2 = a^2 + 2ab + b^2   — square dissection
  PerfectSquareDiff    (a-b)^2 = a^2 - 2ab + b^2   — over-subtraction model
  DifferenceOfSquares  a^2 - b^2 = (a+b)(a-b)      — L-shape (gnomon) rearrange

Consistent symbol <-> colour mapping lives in ``shared/styles.py``:
  a -> blue   b -> amber   ab -> green   removed -> red.

Visual side lengths are proportional to a and b (a drawn longer than b) so the
drawn areas genuinely correspond to the quantities.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from manim import *
from manim_slides import Slide

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.styles import (  # noqa: E402
    AREA_FONT,
    BG,
    COL_A,
    COL_AB,
    COL_B,
    COL_REMOVE,
    FILL_OPACITY,
    INK,
    LABEL_FONT,
    STROKE,
    THIN_STROKE,
)

# Visual lengths (manim units). a is drawn longer than b.
A_LEN = 3.1
B_LEN = 1.7

TCM = {"a": COL_A, "b": COL_B}  # tex_to_color_map: a always blue, b always amber


# ── small helpers ────────────────────────────────────────────────────────────
def filled_rect(bl, w, h, color, opacity=FILL_OPACITY, stroke=THIN_STROKE):
    """Axis-aligned rectangle with bottom-left corner at ``bl``."""
    r = Rectangle(
        width=w,
        height=h,
        stroke_color=color,
        stroke_width=stroke,
        fill_color=color,
        fill_opacity=opacity,
    )
    r.move_to(np.array(bl, dtype=float) + np.array([w / 2.0, h / 2.0, 0.0]))
    return r


def dim_brace(p_start, p_end, direction, tex, color, buff=0.12):
    """A brace spanning p_start->p_end with a coloured LaTeX label at its tip."""
    line = Line(np.array(p_start, dtype=float), np.array(p_end, dtype=float))
    br = Brace(line, direction=direction, buff=buff, color=INK)
    lab = br.get_tex(tex)
    lab.set_color(color)
    lab.scale(0.85)
    return VGroup(br, lab)


def area_label(tex, color, center, scale=1.0):
    m = MathTex(tex, color=color).scale(scale)
    m.move_to(np.array(center, dtype=float))
    return m


class _FactorScene(Slide):
    """Shared setup: dark background + a colour-coded title banner."""

    title_tex = ""

    def setup_scene(self):
        self.camera.background_color = BG
        title = MathTex(self.title_tex, tex_to_color_map=TCM).scale(1.0)
        title.to_edge(UP, buff=0.45)
        return title


# ══════════════════════════════════════════════════════════════════════════════
# 1)  (a+b)^2 = a^2 + 2ab + b^2
# ══════════════════════════════════════════════════════════════════════════════
class PerfectSquareSum(_FactorScene):
    title_tex = r"(a+b)^2 = a^2 + 2ab + b^2"

    def construct(self):
        a, b = A_LEN, B_LEN
        s = a + b
        title = self.setup_scene()
        bl = np.array([-5.8, -2.7, 0.0])  # bottom-left of the big square

        # Regions (origin bottom-left, x right, y up)
        a2 = filled_rect(bl, a, a, COL_A)
        ab_r = filled_rect(bl + np.array([a, 0, 0]), b, a, COL_AB)
        ab_t = filled_rect(bl + np.array([0, a, 0]), a, b, COL_AB)
        b2 = filled_rect(bl + np.array([a, a, 0]), b, b, COL_B)

        outline = Square(side_length=s, stroke_color=INK, stroke_width=STROKE)
        outline.move_to(bl + np.array([s / 2, s / 2, 0]))

        # Side braces: bottom = a then b, left = a then b
        br_a_bot = dim_brace(bl, bl + np.array([a, 0, 0]), DOWN, "a", COL_A)
        br_b_bot = dim_brace(bl + np.array([a, 0, 0]), bl + np.array([s, 0, 0]), DOWN, "b", COL_B)
        br_a_left = dim_brace(bl + np.array([0, a, 0]), bl, LEFT, "a", COL_A)
        br_b_left = dim_brace(bl + np.array([0, s, 0]), bl + np.array([0, a, 0]), LEFT, "b", COL_B)

        # Interior labels
        lab_a2 = area_label("a^2", COL_A, bl + np.array([a / 2, a / 2, 0]), 1.1)
        lab_ab_r = area_label("ab", COL_AB, bl + np.array([a + b / 2, a / 2, 0]), 0.85)
        lab_ab_t = area_label("ab", COL_AB, bl + np.array([a / 2, a + b / 2, 0]), 0.85)
        lab_b2 = area_label("b^2", COL_B, bl + np.array([a + b / 2, a + b / 2, 0]), 0.85)

        # Right-side building equation (single MathTex => baselines align perfectly)
        eq = MathTex("(a+b)^2", "=", "a^2", "+", "2ab", "+", "b^2").scale(0.95)
        eq.move_to(np.array([3.35, 0.3, 0]))
        eq[0][1].set_color(COL_A)   # a in (a+b)^2
        eq[0][3].set_color(COL_B)   # b in (a+b)^2
        eq[2].set_color(COL_A)      # a^2
        eq[4].set_color(COL_AB)     # 2ab
        eq[6].set_color(COL_B)      # b^2
        lhs = VGroup(eq[0], eq[1])
        t_a2, p1, t_2ab, p2, t_b2 = eq[2], eq[3], eq[4], eq[5], eq[6]

        # ── STEP: title ──────────────────────────────────────────────────────
        self.play(Write(title))
        self.wait(0.3)
        self.next_slide()

        # ── STEP: square outline + side = a + b ──────────────────────────────
        self.play(Create(outline))
        self.play(
            GrowFromCenter(br_a_bot), GrowFromCenter(br_b_bot),
            GrowFromCenter(br_a_left), GrowFromCenter(br_b_left),
        )
        self.play(FadeIn(lhs, shift=0.3 * UP))
        self.next_slide()

        # ── STEP: cut into four regions ──────────────────────────────────────
        vline = Line(bl + np.array([a, 0, 0]), bl + np.array([a, s, 0]), color=INK, stroke_width=THIN_STROKE)
        hline = Line(bl + np.array([0, a, 0]), bl + np.array([s, a, 0]), color=INK, stroke_width=THIN_STROKE)
        self.play(Create(vline), Create(hline))
        self.next_slide()

        # ── STEP: a^2 ────────────────────────────────────────────────────────
        self.play(FadeIn(a2), Write(lab_a2))
        self.play(FadeIn(t_a2, shift=0.2 * UP))
        self.next_slide()

        # ── STEP: 2ab ────────────────────────────────────────────────────────
        self.play(FadeIn(ab_r), FadeIn(ab_t), Write(lab_ab_r), Write(lab_ab_t))
        self.play(FadeIn(p1), FadeIn(t_2ab, shift=0.2 * UP))
        self.next_slide()

        # ── STEP: b^2 ────────────────────────────────────────────────────────
        self.play(FadeIn(b2), Write(lab_b2))
        self.play(FadeIn(p2), FadeIn(t_b2, shift=0.2 * UP))
        self.next_slide()

        # ── STEP: conclude ───────────────────────────────────────────────────
        box = SurroundingRectangle(eq, color=COL_AB, buff=0.25)
        self.play(Create(box))
        self.wait(0.4)
        self.next_slide()

        # ── STEP: numeric instance a=3, b=2 ──────────────────────────────────
        sub = MathTex("a = ", "3", r",\quad b = ", "2").scale(0.8)
        sub[0].set_color(COL_A)
        sub[1].set_color(COL_A)
        sub[2].set_color(COL_B)
        sub[3].set_color(COL_B)
        line_a = MathTex(
            r"(", "3", "+", "2", ")^2", "=", "3^2", "+", "2(3)(2)", "+", "2^2",
        ).scale(0.72)
        line_b = MathTex("=", "9", "+", "12", "+", "4", "=", "25").scale(0.72)
        line_a[1].set_color(COL_A)
        line_a[3].set_color(COL_B)
        line_a[6].set_color(COL_A)
        line_a[8].set_color(COL_AB)
        line_a[10].set_color(COL_B)
        line_b[1].set_color(COL_A)
        line_b[3].set_color(COL_AB)
        line_b[5].set_color(COL_B)
        numeric = VGroup(sub, line_a, line_b).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        numeric.next_to(box, DOWN, buff=0.6)
        self.play(FadeIn(sub, shift=0.3 * UP))
        self.play(FadeIn(line_a, shift=0.2 * UP))
        self.play(FadeIn(line_b, shift=0.2 * UP))
        self.wait(0.5)
        self.next_slide()


# ══════════════════════════════════════════════════════════════════════════════
# 2)  (a-b)^2 = a^2 - 2ab + b^2   (over-subtraction / inclusion-exclusion)
# ══════════════════════════════════════════════════════════════════════════════
class PerfectSquareDiff(_FactorScene):
    title_tex = r"(a-b)^2 = a^2 - 2ab + b^2"

    def construct(self):
        a = 4.2          # full square side = a
        b = 1.7          # strip width = b
        inner = a - b    # inner square side
        title = self.setup_scene()
        bl = np.array([-5.9, -2.8, 0.0])

        # base square (area a^2)
        base = filled_rect(bl, a, a, COL_A, opacity=0.18)
        outline = Square(side_length=a, stroke_color=INK, stroke_width=STROKE)
        outline.move_to(bl + np.array([a / 2, a / 2, 0]))

        # side braces showing a, and the a-b / b split on bottom + right
        br_a_top = dim_brace(bl + np.array([0, a, 0]), bl + np.array([a, a, 0]), UP, "a", COL_A)
        br_ab_bot = dim_brace(bl, bl + np.array([inner, 0, 0]), DOWN, "a-b", COL_A)
        br_b_bot = dim_brace(bl + np.array([inner, 0, 0]), bl + np.array([a, 0, 0]), DOWN, "b", COL_B)
        # right side splits into the tall red rectangle (height a-b) and the corner (height b)
        br_ab_right = dim_brace(bl + np.array([a, a, 0]), bl + np.array([a, b, 0]), RIGHT, "a-b", COL_A)
        br_b_right = dim_brace(bl + np.array([a, b, 0]), bl + np.array([a, 0, 0]), RIGHT, "b", COL_B)

        # the two ab strips (right + bottom) and the shared b^2 corner
        strip_r = filled_rect(bl + np.array([inner, 0, 0]), b, a, COL_AB, opacity=0.55)
        strip_b = filled_rect(bl, a, b, COL_AB, opacity=0.55)
        corner = filled_rect(bl + np.array([inner, 0, 0]), b, b, COL_B, opacity=0.9)
        inner_sq = filled_rect(bl + np.array([0, b, 0]), inner, inner, COL_A, opacity=0.85)

        lab_ab_r = area_label("ab", INK, bl + np.array([inner + b / 2, (b + a) / 2, 0]), 0.8)
        lab_ab_b = area_label("ab", INK, bl + np.array([inner / 2, b / 2, 0]), 0.8)
        lab_b2 = area_label("b^2", BG, bl + np.array([inner + b / 2, b / 2, 0]), 0.7)
        lab_inner = area_label("(a-b)^2", INK, bl + np.array([inner / 2, b + inner / 2, 0]), 0.78)

        # right-side building equation (single MathTex => baselines align perfectly)
        eq = MathTex("(a-b)^2", "=", "a^2", "-", "2ab", "+", "b^2").scale(0.92)
        eq.move_to(np.array([3.4, 1.8, 0]))
        eq[0][1].set_color(COL_A)
        eq[0][3].set_color(COL_B)
        eq[2].set_color(COL_A)       # a^2
        eq[3].set_color(COL_REMOVE)  # -
        eq[4].set_color(COL_AB)      # 2ab
        eq[6].set_color(COL_B)       # b^2
        lhs = VGroup(eq[0], eq[1])
        t_a2, m1, t_2ab, p1, t_b2 = eq[2], eq[3], eq[4], eq[5], eq[6]
        # intermediate "ab" (after one strip) that morphs into "2ab" (after two)
        t_ab = MathTex("ab", color=COL_AB)
        t_ab.scale_to_fit_height(t_2ab.height).move_to(t_2ab)

        note = Text("the corner is removed twice", font_size=24, color=COL_REMOVE)
        note.next_to(eq, DOWN, buff=0.7)

        # ── STEP: title ──
        self.play(Write(title))
        self.wait(0.2)
        self.next_slide()

        # ── STEP: square of side a, area a^2 ──
        self.play(Create(outline), FadeIn(base))
        self.play(GrowFromCenter(br_a_top))
        self.play(FadeIn(lhs, shift=0.3 * UP), FadeIn(t_a2, shift=0.2 * UP))
        self.next_slide()

        # ── STEP: split side into (a-b) and b ──
        self.play(
            GrowFromCenter(br_ab_bot), GrowFromCenter(br_b_bot),
            GrowFromCenter(br_ab_right), GrowFromCenter(br_b_right),
        )
        self.next_slide()

        # ── STEP: remove right strip (- ab) ──
        self.play(FadeIn(strip_r), Write(lab_ab_r))
        self.play(strip_r.animate.set_fill(COL_REMOVE, opacity=0.5).set_stroke(COL_REMOVE))
        self.play(FadeIn(m1), FadeIn(t_ab, shift=0.2 * UP))
        self.next_slide()

        # ── STEP: remove bottom strip (- ab) -> -2ab, corner removed twice ──
        self.play(FadeIn(strip_b), Write(lab_ab_b))
        self.play(strip_b.animate.set_fill(COL_REMOVE, opacity=0.5).set_stroke(COL_REMOVE))
        self.play(ReplacementTransform(t_ab, t_2ab))
        self.play(Indicate(corner, color=COL_REMOVE, scale_factor=1.15), FadeIn(corner))
        self.play(FadeIn(note))
        self.next_slide()

        # ── STEP: add the corner b^2 back ──
        self.play(corner.animate.set_fill(COL_B, opacity=0.85).set_stroke(COL_B), Write(lab_b2))
        self.play(FadeIn(p1), FadeIn(t_b2, shift=0.2 * UP), FadeOut(note))
        self.next_slide()

        # ── STEP: remaining inner square = (a-b)^2 ──
        self.play(FadeIn(inner_sq), Write(lab_inner))
        box = SurroundingRectangle(eq, color=COL_A, buff=0.25)
        self.play(Create(box))
        self.wait(0.5)
        self.next_slide()

        # ── STEP: numeric instance a=5, b=2 ──────────────────────────────────
        sub = MathTex("a = ", "5", r",\quad b = ", "2").scale(0.78)
        sub[0].set_color(COL_A)
        sub[1].set_color(COL_A)
        sub[2].set_color(COL_B)
        sub[3].set_color(COL_B)
        line_a = MathTex("(", "5", "-", "2", ")^2", "=", "5^2", "-", "2(5)(2)", "+", "2^2").scale(0.7)
        line_b = MathTex("=", "25", "-", "20", "+", "4", "=", "9").scale(0.7)
        line_a[1].set_color(COL_A)
        line_a[3].set_color(COL_B)
        line_a[6].set_color(COL_A)
        line_a[7].set_color(COL_REMOVE)
        line_a[8].set_color(COL_AB)
        line_a[10].set_color(COL_B)
        line_b[1].set_color(COL_A)
        line_b[2].set_color(COL_REMOVE)
        line_b[3].set_color(COL_AB)
        line_b[5].set_color(COL_B)
        numeric = VGroup(sub, line_a, line_b).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        numeric.next_to(box, DOWN, buff=0.55)
        self.play(FadeIn(sub, shift=0.3 * UP))
        self.play(FadeIn(line_a, shift=0.2 * UP))
        self.play(FadeIn(line_b, shift=0.2 * UP))
        self.wait(0.5)
        self.next_slide()


# ══════════════════════════════════════════════════════════════════════════════
# 3)  a^2 - b^2 = (a+b)(a-b)   (L-shape / gnomon rearrangement)
# ══════════════════════════════════════════════════════════════════════════════
class DifferenceOfSquares(_FactorScene):
    title_tex = r"a^2 - b^2 = (a+b)(a-b)"

    def construct(self):
        a = 4.0
        b = 1.6
        inner = a - b
        title = self.setup_scene()
        bl = np.array([-5.0, -2.6, 0.0])

        big = filled_rect(bl, a, a, COL_A, opacity=0.40)
        big_outline = Square(side_length=a, stroke_color=INK, stroke_width=STROKE)
        big_outline.move_to(bl + np.array([a / 2, a / 2, 0]))

        br_a_top = dim_brace(bl + np.array([0, a, 0]), bl + np.array([a, a, 0]), UP, "a", COL_A)
        br_a_left = dim_brace(bl + np.array([0, a, 0]), bl, LEFT, "a", COL_A)

        # b^2 corner to remove (bottom-right)
        corner = filled_rect(bl + np.array([inner, 0, 0]), b, b, COL_B, opacity=0.85)
        lab_corner = area_label("b^2", COL_B, bl + np.array([inner + b / 2, b / 2, 0]), 0.75)

        # The two pieces of the L-shape
        top_piece = filled_rect(bl + np.array([0, b, 0]), a, inner, COL_A, opacity=0.55)
        bot_piece = filled_rect(bl, inner, b, COL_A, opacity=0.55)

        lab_l = area_label("a^2 - b^2", COL_A, bl + np.array([inner / 2, b + inner / 2, 0]), 0.8)

        # right-side equation (single MathTex => baselines align perfectly)
        eq = MathTex("a^2", "-", "b^2", "=", "(a+b)(a-b)").scale(0.95)
        eq.move_to(np.array([3.6, 2.0, 0]))
        eq[0].set_color(COL_A)       # a^2
        eq[1].set_color(COL_REMOVE)  # -
        eq[2].set_color(COL_B)       # b^2
        eq[4][1].set_color(COL_A)    # a in (a+b)
        eq[4][3].set_color(COL_B)    # b in (a+b)
        eq[4][6].set_color(COL_A)    # a in (a-b)
        eq[4][8].set_color(COL_B)    # b in (a-b)
        lhs = VGroup(eq[0], eq[1], eq[2], eq[3])
        rhs = eq[4]

        # ── STEP: title ──
        self.play(Write(title))
        self.wait(0.2)
        self.next_slide()

        # ── STEP: square a^2 ──
        self.play(Create(big_outline), FadeIn(big))
        self.play(GrowFromCenter(br_a_top), GrowFromCenter(br_a_left))
        self.play(FadeIn(lhs, shift=0.3 * UP))
        self.next_slide()

        # ── STEP: remove b^2 corner -> L-shape ──
        self.play(FadeIn(corner), Write(lab_corner))
        self.play(corner.animate.set_fill(COL_B, opacity=0.85).set_stroke(COL_B))
        self.remove(big)
        self.add(top_piece, bot_piece)
        self.play(FadeOut(corner), FadeOut(lab_corner), Write(lab_l))
        self.next_slide()

        # ── STEP: cut the L into two rectangles ──
        cut = Line(bl + np.array([inner, 0, 0]), bl + np.array([inner, b, 0]), color=INK, stroke_width=THIN_STROKE)
        self.play(Create(cut))
        self.play(
            top_piece.animate.set_stroke(INK, width=STROKE),
            bot_piece.animate.set_stroke(INK, width=STROKE),
        )
        self.next_slide()

        # ── STEP: rotate + slide the bottom piece to the right ──
        self.play(FadeOut(lab_l), FadeOut(cut), FadeOut(br_a_top), FadeOut(br_a_left), FadeOut(big_outline))
        self.play(
            bot_piece.animate.rotate(-PI / 2).next_to(top_piece, RIGHT, buff=0.0, aligned_edge=DOWN)
        )
        self.next_slide()

        # ── STEP: label the new rectangle (a+b) x (a-b) ──
        rect_group = VGroup(top_piece, bot_piece)
        new_outline = SurroundingRectangle(rect_group, color=INK, buff=0.0, stroke_width=STROKE)
        br_w = dim_brace(
            rect_group.get_corner(DOWN + LEFT), rect_group.get_corner(DOWN + RIGHT), DOWN, "a+b", INK
        )
        br_h = dim_brace(
            rect_group.get_corner(UP + LEFT), rect_group.get_corner(DOWN + LEFT), LEFT, "a-b", INK
        )
        self.play(Create(new_outline), GrowFromCenter(br_w), GrowFromCenter(br_h))
        self.play(FadeIn(rhs, shift=0.2 * UP))
        box = SurroundingRectangle(eq, color=COL_A, buff=0.25)
        self.play(Create(box))
        self.wait(0.5)
        self.next_slide()

        # ── STEP: numeric instance a=5, b=2 ──────────────────────────────────
        sub = MathTex("a = ", "5", r",\quad b = ", "2").scale(0.78)
        sub[0].set_color(COL_A)
        sub[1].set_color(COL_A)
        sub[2].set_color(COL_B)
        sub[3].set_color(COL_B)
        line_a = MathTex("5^2", "-", "2^2", "=", "(5+2)(5-2)").scale(0.7)
        line_a[0].set_color(COL_A)
        line_a[1].set_color(COL_REMOVE)
        line_a[2].set_color(COL_B)
        line_a[4][1].set_color(COL_A)
        line_a[4][3].set_color(COL_B)
        line_a[4][6].set_color(COL_A)
        line_a[4][8].set_color(COL_B)
        line_b = MathTex("=", "25", "-", "4", "=", "(7)(3)", "=", "21").scale(0.7)
        line_b[1].set_color(COL_A)
        line_b[2].set_color(COL_REMOVE)
        line_b[3].set_color(COL_B)
        numeric = VGroup(sub, line_a, line_b).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        numeric.next_to(box, DOWN, buff=0.55)
        self.play(FadeIn(sub, shift=0.3 * UP))
        self.play(FadeIn(line_a, shift=0.2 * UP))
        self.play(FadeIn(line_b, shift=0.2 * UP))
        self.wait(0.5)
        self.next_slide()
