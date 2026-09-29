"""JM28 - Deck 1: the four special lines of a triangle.

    Slide 0   triangle ABC + the four names
    Slide 1   median                 (BD = DC)
    Slide 2   altitude               (AE perpendicular to BC)
    Slide 3   angle bisector         (angle BAF = angle CAF)
    Slide 4   perpendicular bisector (through the mid-point, at right angles)
    Slide 5   recap: all four side by side

Render (from a scratch folder, see README.md):
    manim-slides render special_lines.py TriangleSpecialLines --quality h
    manim-slides convert TriangleSpecialLines <out>/index.html --to html
"""
from __future__ import annotations

import sys
import pathlib

from manim import *

sys.path.append(str(pathlib.Path(__file__).resolve().parent))
from tc_common import (  # noqa: E402
    TCSlide, A0, B0, C0, BG, INK, MUTED, GOLD, MEDIAN, ALTITUDE, BISECTOR, PERP, TICK,
    mid, foot, bisector_foot, triangle, vertex_labels, point_label, dot, seg,
    ticks, right_mark, ticked_arc, panel, heading, body, eq,
)

NAMES = [
    ("Median", MEDIAN),
    ("Altitude", ALTITUDE),
    ("Angle bisector", BISECTOR),
    ("Perpendicular bisector", PERP),
]


def median_parts(A, B, C, s=1.0):
    D = mid(B, C)
    return D, VGroup(ticks(B, D, size=0.24 * s), ticks(D, C, size=0.24 * s)), seg(A, D, MEDIAN)


def altitude_parts(A, B, C, s=1.0):
    E = foot(A, B, C)
    return E, right_mark(E, C, A, s=0.22 * s), seg(A, E, ALTITUDE)


def bisector_parts(A, B, C, s=1.0):
    F = bisector_foot(A, B, C)
    arcs = VGroup(ticked_arc(A, B, F, r=0.62 * s, size=0.16 * s),
                  ticked_arc(A, F, C, r=0.62 * s, size=0.16 * s))
    return F, arcs, seg(A, F, BISECTOR)


def perp_parts(A, B, C, s=1.0, up=3.3):
    D = mid(B, C)
    top = D + UP * up * s
    line = seg(D + DOWN * 0.55 * s, top, PERP)
    marks = VGroup(ticks(B, D, size=0.24 * s), ticks(D, C, size=0.24 * s),
                   right_mark(D, C, top, s=0.22 * s))
    return D, marks, line


class TriangleSpecialLines(TCSlide):
    def construct(self):
        self.camera.background_color = BG
        self.title_bar(r"Special lines in a triangle")

        A, B, C = A0, B0, C0
        tri = triangle(A, B, C)
        labs = vertex_labels([A, B, C], "ABC")
        self.play(Create(tri), run_time=1.0)
        self.play(FadeIn(labs))

        intro = panel([
            body(r"A triangle has four special lines:", INK, 34),
            *[Tex(r"\textbullet\ " + n, color=c, font_size=36) for n, c in NAMES],
            body(r"Each is drawn by a rule --- the", MUTED, 30),
            body(r"markings on the figure show the rule.", MUTED, 30),
        ], y_top=1.9)
        self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in intro], lag_ratio=0.25))
        self.next_slide()

        # ── 1. median ────────────────────────────────────────────────────
        D, tk, med = median_parts(A, B, C)
        d_dot, d_lab = dot(D), point_label(D, "D", DOWN)
        txt = panel([
            heading(r"Median", MEDIAN),
            body(r"joins a vertex to the"),
            body(r"\textbf{mid-point} of the opposite side."),
            eq(r"BD = DC", TICK),
            body(r"(equal tick marks = equal lengths)", MUTED, 28),
        ])
        self.swap(intro, txt)
        self.play(FadeIn(d_dot), Write(d_lab))
        self.play(Create(tk))
        self.play(Create(med), run_time=0.9)
        cur = VGroup(d_dot, d_lab, tk, med)
        self.next_slide()

        # ── 2. altitude ──────────────────────────────────────────────────
        E, rm, alt = altitude_parts(A, B, C)
        e_dot, e_lab = dot(E), point_label(E, "E", DOWN)
        txt2 = panel([
            heading(r"Altitude", ALTITUDE),
            body(r"from a vertex, \textbf{perpendicular}"),
            body(r"to the opposite side."),
            eq(r"AE \perp BC", ALTITUDE),
            body(r"Also called the \emph{height} on base $BC$.", MUTED, 28),
        ])
        self.play(FadeOut(cur), run_time=0.4)
        self.swap(txt, txt2)
        self.play(Create(alt), run_time=0.9)
        self.play(FadeIn(e_dot), Write(e_lab), Create(rm))
        cur = VGroup(e_dot, e_lab, rm, alt)
        self.next_slide()

        # ── 3. angle bisector ────────────────────────────────────────────
        F, arcs, bis = bisector_parts(A, B, C)
        f_dot, f_lab = dot(F), point_label(F, "F", DOWN)
        txt3 = panel([
            heading(r"Angle bisector", BISECTOR),
            body(r"divides an angle into"),
            body(r"\textbf{two equal angles}."),
            eq(r"\angle BAF = \angle CAF", BISECTOR),
            body(r"(matching arcs = equal angles)", MUTED, 28),
        ])
        self.play(FadeOut(cur), run_time=0.4)
        self.swap(txt2, txt3)
        self.play(Create(bis), run_time=0.9)
        self.play(FadeIn(f_dot), Write(f_lab))
        self.play(Create(arcs[0]), Create(arcs[1]))
        cur = VGroup(f_dot, f_lab, arcs, bis)
        self.next_slide()

        # ── 4. perpendicular bisector ────────────────────────────────────
        D, marks, pb = perp_parts(A, B, C)
        m_dot, m_lab = dot(D), point_label(D, "M", DOWN + LEFT * 0.8, buff=0.4)
        txt4 = panel([
            heading(r"Perpendicular bisector", PERP),
            body(r"passes through the \textbf{mid-point}"),
            body(r"of a side and is \textbf{perpendicular} to it."),
            eq(r"BM = MC,\quad \text{line} \perp BC", PERP),
            body(r"It need not pass through a vertex.", MUTED, 28),
        ])
        self.play(FadeOut(cur), run_time=0.4)
        self.swap(txt3, txt4)
        self.play(FadeIn(m_dot), Write(m_lab), Create(marks[:2]))
        self.play(Create(pb), run_time=0.9)
        self.play(Create(marks[2]))
        cur = VGroup(m_dot, m_lab, marks, pb)
        self.next_slide()

        # ── 5. recap: four mini triangles ────────────────────────────────
        self.play(FadeOut(cur), FadeOut(txt4), FadeOut(tri), FadeOut(labs))
        s = 0.44
        g0 = (A + B + C) / 3
        builders = [median_parts, altitude_parts, bisector_parts, perp_parts]
        rules = [
            r"vertex $\to$ mid-point",
            r"vertex, $\perp$ opposite side",
            r"splits an angle equally",
            r"through mid-point, $\perp$ side",
        ]
        cells = VGroup()
        for i, (build, (name, col), rule) in enumerate(zip(builders, NAMES, rules)):
            cx = -5.25 + i * 3.5
            shift = np.array([cx, 0.35, 0]) - g0 * s
            a, b, c = A * s + shift, B * s + shift, C * s + shift
            _, marks_i, line_i = build(a, b, c, s=s)
            t = triangle(a, b, c)
            nm = Tex(name, color=col, font_size=30).move_to([cx, -1.45, 0])
            rl = Tex(rule, color=MUTED, font_size=24).next_to(nm, DOWN, buff=0.16)
            cells.add(VGroup(t, marks_i, line_i, nm, rl))
        self.play(LaggedStart(*[FadeIn(cell, shift=UP * 0.2) for cell in cells], lag_ratio=0.3),
                  run_time=2.0)
        foot_note = Tex(r"Next deck: three lines of the same kind meet at a \emph{centre}.",
                        color=GOLD, font_size=30).move_to([0, -2.9, 0])
        self.play(FadeIn(foot_note))
        self.wait(0.3)
        self.next_slide()
