"""Shared Manim style helpers.

Required by `resource/parallel-lines-diagram/manim/diagram.py`
(`import manim_styles as s`), which expects this module on
`<repo-root>/manim/`.
"""
from __future__ import annotations

import numpy as np
from manim import WHITE, Arc, ManimColor

TWO_PI = 2.0 * np.pi


def _angle_of(vec: np.ndarray) -> float:
    """Polar angle of a 2D/3D vector in [0, 2*pi)."""
    return float(np.arctan2(vec[1], vec[0])) % TWO_PI


def interior_angle_arc(
    vertex: np.ndarray,
    p1: np.ndarray,
    p2: np.ndarray,
    inside_point: np.ndarray,
    radius: float = 0.3,
    color: ManimColor = WHITE,
    stroke_width: float = 2.5,
) -> Arc:
    """Arc at `vertex` between rays vertex->p1 and vertex->p2.

    Of the two candidate arcs, returns the one passing on the side of
    `inside_point` (so the mark always sits inside the intended region).
    """
    a1 = _angle_of(p1 - vertex)
    a2 = _angle_of(p2 - vertex)
    a_in = _angle_of(inside_point - vertex)
    sweep = (a2 - a1) % TWO_PI
    if (a_in - a1) % TWO_PI <= sweep:
        start, angle = a1, sweep
    else:
        start, angle = a2, TWO_PI - sweep
    return Arc(
        radius=radius,
        start_angle=start,
        angle=angle,
        arc_center=vertex,
        color=color,
        stroke_width=stroke_width,
    )
