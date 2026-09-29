"""Shared palette, geometry and marking helpers for the JM28 Manim slides.

Colour convention (same line type = same colour in every deck and on the
dashboard's Interactive Tool):

    median                 -> amber   (meet at centroid G)
    altitude               -> blue    (meet at orthocentre H)
    angle bisector         -> green   (meet at in-centre I)
    perpendicular bisector -> pink    (meet at circumcentre O)
    equal-length ticks     -> red
    equal-angle arcs, right-angle marks -> white

Layout: figure on the left half of the frame, explanation panel on the right.
"""
from __future__ import annotations

import numpy as np
from manim import *
from manim_slides import Slide

# Canvas (matches the dashboard decks) -------------------------------------
BG = ManimColor("#0f172a")
INK = ManimColor("#F8FAFC")
MUTED = ManimColor("#94A3B8")
GOLD = ManimColor("#E6C260")

# Concept colours ----------------------------------------------------------
MEDIAN = ManimColor("#FFD54F")
ALTITUDE = ManimColor("#4FC3F7")
BISECTOR = ManimColor("#81C784")
PERP = ManimColor("#F06292")
TICK = ManimColor("#F87171")
MARK = INK

STROKE = 3.0
LINE_W = 3.5
LABEL_FS = 36

# Default acute scalene triangle (left half of the frame) -------------------
A0 = np.array([-3.9, 2.0, 0.0])
B0 = np.array([-5.6, -2.0, 0.0])
C0 = np.array([-0.6, -2.0, 0.0])


# ── geometry ────────────────────────────────────────────────────────────────
def unit(v):
    n = np.linalg.norm(v)
    return v / n if n else v


def mid(p, q):
    return (p + q) / 2


def foot(p, a, b):
    """Foot of the perpendicular from p to the (infinite) line ab."""
    d = b - a
    t = np.dot(p - a, d) / np.dot(d, d)
    return a + t * d


def centroid(a, b, c):
    return (a + b + c) / 3


def incentre(a, b, c):
    la, lb, lc = np.linalg.norm(b - c), np.linalg.norm(c - a), np.linalg.norm(a - b)
    return (la * a + lb * b + lc * c) / (la + lb + lc)


def circumcentre(a, b, c):
    ax, ay = a[:2]
    bx, by = b[:2]
    cx, cy = c[:2]
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    return np.array([ux, uy, 0.0])


def orthocentre(a, b, c):
    return a + b + c - 2 * circumcentre(a, b, c)


def bisector_foot(v, p, q):
    """Where the bisector of angle pvq meets side pq (angle bisector theorem)."""
    lp, lq = np.linalg.norm(p - v), np.linalg.norm(q - v)
    return p + (lp / (lp + lq)) * (q - p)


def on_segment(x, a, b, eps=1e-6):
    t = np.dot(x - a, b - a) / np.dot(b - a, b - a)
    return -eps <= t <= 1 + eps


# ── drawing ─────────────────────────────────────────────────────────────────
def triangle(a, b, c, color=INK):
    return Polygon(a, b, c, color=color, stroke_width=STROKE)


def vertex_labels(pts, names, fs=LABEL_FS, buff=0.34):
    g = centroid(*pts)
    return VGroup(*[
        MathTex(n, color=INK, font_size=fs).move_to(p + unit(p - g) * buff)
        for p, n in zip(pts, names)
    ])


def point_label(p, name, direction, color=INK, fs=LABEL_FS, buff=0.3, backed=False):
    lab = MathTex(name, color=color, font_size=fs).move_to(p + unit(direction) * buff)
    if backed:
        lab.add_background_rectangle(color=BG, opacity=0.85, buff=0.06)
    return lab


def dot(p, color=INK, r=0.07):
    return Dot(p, radius=r, color=color)


def seg(p, q, color, w=LINE_W):
    return Line(p, q, color=color, stroke_width=w)


def dashed(p, q, color, w=2.5, dash=0.12):
    return DashedLine(p, q, color=color, stroke_width=w, dash_length=dash)


def dotted(p, q, color=MUTED, w=2.5):
    return DashedLine(p, q, color=color, stroke_width=w, dash_length=0.04, dashed_ratio=0.45)


def ticks(p, q, n=1, color=TICK, size=0.24, gap=0.09):
    """n short tick marks across the mid-point of segment pq."""
    m, d = mid(p, q), unit(q - p)
    nrm = np.array([-d[1], d[0], 0.0])
    offs = (np.arange(n) - (n - 1) / 2) * gap
    return VGroup(*[
        Line(m + d * o - nrm * size / 2, m + d * o + nrm * size / 2, color=color, stroke_width=3)
        for o in offs
    ])


def right_mark(at, toward1, toward2, s=0.22, color=MARK):
    u, w = unit(toward1 - at), unit(toward2 - at)
    return VMobject(color=color, stroke_width=2.5).set_points_as_corners(
        [at + u * s, at + u * s + w * s, at + w * s]
    )


def angle_arcs(v, p, q, n=1, r=0.42, gap=0.09, color=MARK):
    """n concentric arcs marking the (smaller) angle pvq."""
    a1 = np.arctan2(*(p - v)[1::-1])
    a2 = np.arctan2(*(q - v)[1::-1])
    delta = (a2 - a1 + np.pi) % (2 * np.pi) - np.pi
    return VGroup(*[
        Arc(radius=r + i * gap, start_angle=a1, angle=delta, arc_center=v,
            color=color, stroke_width=2.5)
        for i in range(n)
    ])


def ticked_arc(v, p, q, r=0.55, color=MARK, size=0.16):
    """Single arc for angle pvq with a small tick across its middle; two
    ticked arcs of the same radius mark two equal angles."""
    arc = angle_arcs(v, p, q, 1, r=r, color=color)[0]
    a1 = np.arctan2(*(p - v)[1::-1])
    a2 = np.arctan2(*(q - v)[1::-1])
    am = a1 + ((a2 - a1 + np.pi) % (2 * np.pi) - np.pi) / 2
    d = np.array([np.cos(am), np.sin(am), 0.0])
    tick = Line(v + d * (r - size / 2), v + d * (r + size / 2), color=color, stroke_width=2.5)
    return VGroup(arc, tick)


def perp_bisector(p, q, through=None, over=0.6, color=PERP):
    """Perpendicular bisector of pq. If `through` is given, the line runs from
    just behind the mid-point to just past that point; else a fixed length."""
    m, d = mid(p, q), unit(q - p)
    nrm = np.array([-d[1], d[0], 0.0])
    if through is not None and np.linalg.norm(through - m) > 1e-6:
        u = unit(through - m)
        return seg(m - u * over, through + u * over, color)
    return seg(m - nrm * 2.2, m + nrm * 2.2, color)


# ── text panel ──────────────────────────────────────────────────────────────
def panel(rows, x_left=0.7, y_top=2.2, buff=0.26):
    """Stack rows (Mobjects) left-aligned in the right half of the frame."""
    g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=buff)
    g.move_to([x_left + g.width / 2, y_top - g.height / 2, 0])
    return g


def heading(text, color, fs=46):
    return Tex(text, color=color, font_size=fs)


def body(text, color=INK, fs=32):
    return Tex(text, color=color, font_size=fs)


def eq(tex, color=INK, fs=38):
    return MathTex(tex, color=color, font_size=fs)


class TCSlide(Slide):
    """Base slide with the gold-accented title bar used by the other decks."""

    def title_bar(self, text: str) -> VGroup:
        title = Tex(text, font_size=48, color=INK).to_edge(UP, buff=0.4)
        accent = Line(LEFT, RIGHT, color=GOLD, stroke_width=3)
        accent.set_width(title.width + 0.6).next_to(title, DOWN, buff=0.12)
        self.play(Write(title), GrowFromCenter(accent))
        return VGroup(title, accent)

    def swap(self, old, new, run_time=0.6):
        """Fade out `old` (Mobject or None) and fade in `new`."""
        anims = []
        if old is not None:
            anims.append(FadeOut(old))
        if new is not None:
            anims.append(FadeIn(new, shift=LEFT * 0.2))
        if anims:
            self.play(*anims, run_time=run_time)
