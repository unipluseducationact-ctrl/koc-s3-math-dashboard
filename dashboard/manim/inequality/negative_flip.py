"""Inequality - Deck 2 (Concept & Formula): the negative-coefficient rule.

    Slide 1   why it flips:  3 < 5  but  -3 > -5   (shown on a number line)
    Slide 2   the rule:      x or / by a negative  ->  reverse the sign
    Slide 3   Method 1:      divide by (-1) directly  ->  must remember to flip
    Slide 4   Method 2:      move the negative term across  ->  no negative
                             division, so nothing to forget (recommended)

Render:
    manim-slides render negative_flip.py NegativeCoefficient --quality h
    manim-slides convert NegativeCoefficient <out>/index.html --to html
"""
from __future__ import annotations

import sys
import pathlib

from manim import *

sys.path.append(str(pathlib.Path(__file__).resolve().parent))
from ineq_common import (  # noqa: E402
    IneqSlide, BG, INK, MUTED, GOLD, GREEN, AMBER, RED, SAFE,
    make_axis, closed_dot,
)

EQ_FS = 60
NOTE_FS = 30


def _place(eq, sign_x, y):
    """Position an equation at height ``y`` with its relation sign (index 1)
    snapped to ``sign_x`` so the signs line up vertically across rows."""
    eq.move_to([0, y, 0])
    eq.shift(RIGHT * (sign_x - eq[1].get_center()[0]))
    return eq


class NegativeCoefficient(IneqSlide):
    def construct(self):
        self.camera.background_color = BG
        self.title_bar(r"Multiply or Divide by a Negative")
        self.next_slide()

        prev = self._motivation()
        self.next_slide()
        self.play(FadeOut(prev))

        prev = self._rule()
        self.next_slide()
        self.play(FadeOut(prev))

        prev = self._method1()
        self.next_slide()
        self.play(FadeOut(prev))

        prev = self._method2()
        self.next_slide()

    # ----------------------------------------------------------------------
    def _motivation(self):
        true_stmt = MathTex("3", "<", "5", font_size=72, color=INK)
        true_stmt[1].set_color(AMBER)
        true_stmt.move_to([0, 1.85, 0])
        check = Tex(r"true", font_size=32, color=SAFE).next_to(true_stmt, RIGHT, buff=0.5)

        op = Tex(r"multiply both sides by $-1$", font_size=34, color=GOLD)
        op.move_to([0, 0.95, 0])

        flipped = MathTex("-3", r"\;\;?\;\;", "-5", font_size=72, color=INK)
        flipped.move_to([0, 0.1, 0])

        self.play(Write(true_stmt))
        self.play(FadeIn(check, shift=LEFT * 0.2))
        self.play(FadeIn(op, shift=DOWN * 0.2))
        self.play(TransformFromCopy(true_stmt[0], flipped[0]),
                  TransformFromCopy(true_stmt[2], flipped[2]),
                  Write(flipped[1]))

        nl = make_axis([-5, -3, 0, 3, 5], -6, 6, length=9.0, y=-1.9)
        dn5 = closed_dot(nl, -5, INK)
        dn3 = closed_dot(nl, -3, INK)
        l5 = MathTex("-5", font_size=30, color=MUTED).next_to(dn5, UP, buff=0.28)
        l3 = MathTex("-3", font_size=30, color=MUTED).next_to(dn3, UP, buff=0.28)
        self.play(Create(nl))
        self.play(GrowFromCenter(dn5), GrowFromCenter(dn3), FadeIn(l5), FadeIn(l3))

        bigger = Tex(r"$-3$ lies to the \emph{right} of $-5$, so $-3$ is larger",
                     font_size=30, color=MUTED).next_to(nl, DOWN, buff=0.45)
        self.play(FadeIn(bigger))

        gt = MathTex(">", font_size=72, color=GREEN).move_to(flipped[1])
        self.play(Transform(flipped[1], gt))
        conclusion = Tex(r"the sign \textbf{reversed}", font_size=32, color=GREEN)
        conclusion.next_to(flipped, RIGHT, buff=0.5)
        self.play(FadeIn(conclusion, shift=LEFT * 0.2))

        return VGroup(true_stmt, check, op, flipped, nl, dn5, dn3, l5, l3,
                      bigger, conclusion)

    def _rule(self):
        box = RoundedRectangle(corner_radius=0.2, width=10.6, height=2.4,
                               stroke_color=GOLD, stroke_width=2.5,
                               fill_color=GOLD, fill_opacity=0.07)
        box.move_to([0, 0.9, 0])
        line1 = Tex(r"Multiplying or dividing \emph{both sides} by a",
                    font_size=40, color=INK)
        neg = Tex(r"negative number", font_size=40, color=RED)
        top = VGroup(line1, neg).arrange(RIGHT, buff=0.22)
        line2 = Tex(r"reverses the inequality sign.", font_size=40, color=INK)
        text = VGroup(top, line2).arrange(DOWN, buff=0.28).move_to(box.get_center())

        self.play(GrowFromCenter(box), FadeIn(text))

        # visual: >  flips to  <
        demo = VGroup(
            MathTex(">", font_size=88, color=GREEN),
            MathTex(r"\longrightarrow", font_size=60, color=MUTED),
            MathTex("<", font_size=88, color=AMBER),
        ).arrange(RIGHT, buff=0.6).move_to([0, -1.7, 0])
        arc = CurvedArrow(demo[0].get_top() + UP * 0.1,
                          demo[2].get_top() + UP * 0.1,
                          color=RED, stroke_width=4, angle=-TAU / 4)
        self.play(Write(demo[0]))
        self.play(Write(demo[1]), Write(demo[2]))
        self.play(Create(arc))
        return VGroup(box, text, demo, arc)

    def _method1(self):
        head = self._method_header(r"Method 1: divide by the negative", RED)

        SIGN_X = -0.8
        e0 = MathTex(r"-\tfrac{x}{4}", r"\ge", "2", font_size=EQ_FS, color=INK)
        e1 = MathTex("-x", r"\ge", "8", font_size=EQ_FS, color=INK)
        e2 = MathTex("x", r"\le", "-8", font_size=EQ_FS, color=INK)
        _place(e0, SIGN_X, 1.35)
        _place(e1, SIGN_X, 0.15)
        _place(e2, SIGN_X, -1.05)

        n1 = Tex(r"$\times\,4$", font_size=NOTE_FS, color=MUTED).next_to(e1, RIGHT, buff=1.3)
        n2 = Tex(r"$\div\,(-1)$", font_size=NOTE_FS, color=RED).next_to(e2, RIGHT, buff=1.3)
        flip = Tex(r"sign \textbf{flips}", font_size=26, color=RED).next_to(n2, DOWN, buff=0.14)

        self.play(Write(e0))
        self.play(TransformFromCopy(e0, e1), FadeIn(n1, shift=LEFT * 0.2))
        self.play(TransformFromCopy(e1, e2), FadeIn(n2, shift=LEFT * 0.2))
        e2[1].set_color(RED)
        self.play(Indicate(e2[1], color=RED, scale_factor=1.4),
                  FadeIn(flip, shift=UP * 0.1))
        warn = Tex(r"easy to forget the flip!", font_size=30, color=RED)
        warn.move_to([0, -2.45, 0])
        self.play(FadeIn(warn))
        return VGroup(head, e0, e1, e2, n1, n2, flip, warn)

    def _method2(self):
        head = self._method_header(r"Method 2: move the negative term across", SAFE)

        SIGN_X = -0.9
        e0 = MathTex(r"-\tfrac{x}{4}", r"\ge", "2", font_size=EQ_FS, color=INK)
        e1 = MathTex("-x", r"\ge", "8", font_size=EQ_FS, color=INK)
        _place(e0, SIGN_X, 1.35)
        _place(e1, SIGN_X, 0.35)
        n1 = Tex(r"$\times\,4$", font_size=NOTE_FS, color=MUTED).next_to(e1, RIGHT, buff=1.4)

        self.play(Write(e0))
        self.play(TransformFromCopy(e0, e1), FadeIn(n1, shift=LEFT * 0.2))

        # move -x to the right (becomes +x) and 8 to the left (becomes -8)
        e2 = MathTex("-8", r"\ge", "x", font_size=EQ_FS, color=INK)
        _place(e2, SIGN_X, -1.15)
        cross = Tex(r"add $x$, subtract $8$", font_size=26, color=SAFE)
        cross.next_to(e1, RIGHT, buff=1.4).shift(DOWN * 0.72)
        a1 = CurvedArrow(e1[0].get_bottom() + DOWN * 0.18, e2[2].get_top() + UP * 0.18,
                         color=SAFE, stroke_width=3.5, angle=-TAU / 7)
        a2 = CurvedArrow(e1[2].get_bottom() + DOWN * 0.18, e2[0].get_top() + UP * 0.18,
                         color=SAFE, stroke_width=3.5, angle=TAU / 7)
        self.play(Create(a1), Create(a2), FadeIn(cross))
        self.play(TransformFromCopy(e1[0], e2[2]),
                  TransformFromCopy(e1[2], e2[0]),
                  TransformFromCopy(e1[1], e2[1]))

        # swap sides into standard form
        e3 = MathTex("x", r"\le", "-8", font_size=EQ_FS, color=INK)
        e3[1].set_color(SAFE)
        _place(e3, SIGN_X, -2.0)
        swap = Tex(r"swap sides to read it normally", font_size=26, color=SAFE)
        swap.next_to(e3, RIGHT, buff=1.4)
        self.play(TransformFromCopy(e2[2], e3[0]),
                  TransformFromCopy(e2[0], e3[2]),
                  Write(e3[1]), FadeIn(swap))

        good = Tex(r"only $+$ and $-$ used \;--\; no flip to forget",
                   font_size=28, color=SAFE).move_to([0, -3.05, 0])
        self.play(FadeIn(good))
        return VGroup(head, e0, e1, n1, e2, cross, a1, a2, e3, swap, good)

    # ----------------------------------------------------------------------
    def _method_header(self, text, color):
        head = Tex(text, font_size=38, color=color).move_to([0, 2.45, 0])
        underline = Line(LEFT, RIGHT, color=color, stroke_width=2.5)
        underline.set_width(head.width + 0.4).next_to(head, DOWN, buff=0.14)
        grp = VGroup(head, underline)
        self.play(FadeIn(head, shift=DOWN * 0.15), GrowFromCenter(underline))
        return grp
