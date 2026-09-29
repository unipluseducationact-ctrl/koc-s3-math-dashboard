"""JM28 - Deck 2: the four centres of a triangle and where they lie.

    Slide 0   three lines of the same kind meet at one point
    Slide 1   centroid G      (medians; AG : GD = 2 : 1)
    Slide 2   orthocentre H   (altitudes)
    Slide 3   in-centre I     (angle bisectors; inscribed circle)
    Slide 4   circumcentre O  (perpendicular bisectors; circumscribed circle)
    Slide 5   right-angled triangle: H at the right angle, O at mid-point of hypotenuse
    Slide 6   obtuse-angled triangle: H and O outside
    Slide 7   summary table

Render (from a scratch folder, see README.md):
    manim-slides render centres.py TriangleCentres --quality h
    manim-slides convert TriangleCentres <out>/index.html --to html
"""
from __future__ import annotations

import sys
import pathlib

from manim import *

sys.path.append(str(pathlib.Path(__file__).resolve().parent))
from tc_common import (  # noqa: E402
    TCSlide, A0, B0, C0, BG, INK, MUTED, GOLD, MEDIAN, ALTITUDE, BISECTOR, PERP, TICK,
    unit, mid, foot, centroid, incentre, circumcentre, orthocentre, bisector_foot, on_segment,
    triangle, vertex_labels, point_label, dot, seg, dashed, dotted,
    ticks, right_mark, angle_arcs, perp_bisector, panel, heading, body, eq,
)

OUTSIDE = ManimColor("#F87171")


def centre_dot(p, color):
    return VGroup(Dot(p, radius=0.11, color=color), Dot(p, radius=0.05, color=BG))


def altitudes(A, B, C, H):
    """Altitude from each vertex, extended (dashed) to H and with dotted side
    extensions when the foot falls outside the opposite side."""
    lines, marks, extras = VGroup(), VGroup(), VGroup()
    for v, p, q in ((A, B, C), (B, C, A), (C, A, B)):
        f = foot(v, p, q)
        lines.add(seg(v, f, ALTITUDE))
        if not on_segment(f, p, q):
            near = p if np.linalg.norm(f - p) < np.linalg.norm(f - q) else q
            extras.add(dotted(near, f))
        if np.linalg.norm(f - v) > 1e-6 and not on_segment(H, v, f):
            end = v if np.linalg.norm(H - v) < np.linalg.norm(H - f) else f
            extras.add(dashed(end, H, ALTITUDE))
        other = q if np.linalg.norm(q - f) > 0.3 else p
        if np.linalg.norm(f - v) > 1e-6:
            marks.add(right_mark(f, other, v))
    return lines, marks, extras


def perp_bisectors(A, B, C, O):
    lines, marks = VGroup(), VGroup()
    for n, (p, q) in enumerate(((B, C), (C, A), (A, B)), start=1):
        m = mid(p, q)
        lines.add(perp_bisector(p, q, through=O))
        marks.add(ticks(p, m, n), ticks(m, q, n))
        if np.linalg.norm(O - m) > 0.3:
            marks.add(right_mark(m, q, O))
    return lines, marks


class TriangleCentres(TCSlide):
    def construct(self):
        self.camera.background_color = BG
        self.title_bar(r"Centres of a triangle")

        A, B, C = A0, B0, C0
        tri = triangle(A, B, C)
        labs = vertex_labels([A, B, C], "ABC")
        self.play(Create(tri), run_time=1.0)
        self.play(FadeIn(labs))

        intro = panel([
            body(r"Draw \textbf{three} special lines of the", INK, 34),
            body(r"same kind --- they always meet at", INK, 34),
            body(r"\textbf{one point}: a \emph{centre} of the triangle.", INK, 34),
            Tex(r"medians $\to$ centroid $G$", color=MEDIAN, font_size=34),
            Tex(r"altitudes $\to$ orthocentre $H$", color=ALTITUDE, font_size=34),
            Tex(r"angle bisectors $\to$ in-centre $I$", color=BISECTOR, font_size=34),
            Tex(r"perp.\ bisectors $\to$ circumcentre $O$", color=PERP, font_size=34),
        ], y_top=2.0, buff=0.22)
        self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in intro], lag_ratio=0.2))
        self.next_slide()

        # ── 1. centroid ─────────────────────────────────────────────────
        G = centroid(A, B, C)
        D, E, F = mid(B, C), mid(C, A), mid(A, B)
        tk = VGroup(ticks(B, D, 1), ticks(D, C, 1), ticks(C, E, 2), ticks(E, A, 2),
                    ticks(A, F, 3), ticks(F, B, 3))
        meds = VGroup(seg(A, D, MEDIAN), seg(B, E, MEDIAN), seg(C, F, MEDIAN))
        mlabs = VGroup(point_label(D, "D", DOWN), point_label(E, "E", UP + RIGHT),
                       point_label(F, "F", UP + LEFT))
        txt = panel([
            heading(r"Centroid $G$", MEDIAN),
            body(r"The three \textbf{medians} meet at $G$."),
            body(r"$G$ always lies \textbf{inside} the triangle."),
        ])
        self.swap(intro, txt)
        for i in range(3):
            self.play(Create(tk[2 * i]), Create(tk[2 * i + 1]), FadeIn(mlabs[i]), run_time=0.5)
            self.play(Create(meds[i]), run_time=0.7)
        g = centre_dot(G, MEDIAN)
        g_lab = point_label(G, "G", RIGHT + DOWN * 0.9, MEDIAN, buff=0.4, backed=True)
        self.play(FadeIn(g, scale=0.5), Write(g_lab))
        self.next_slide()

        # G divides each median 2 : 1 from the vertex
        ag = seg(A, G, MEDIAN, w=8).set_opacity(0.55)
        gd = seg(G, D, TICK, w=8).set_opacity(0.55)
        two = MathTex("2", color=MEDIAN, font_size=34).next_to(mid(A, G), LEFT, buff=0.18)
        one = MathTex("1", color=TICK, font_size=34).next_to(mid(G, D), LEFT, buff=0.18)
        ratio = panel([eq(r"AG : GD = 2 : 1", INK, 40),
                       body(r"(true for every median)", MUTED, 28)], y_top=txt.get_bottom()[1] - 0.35)
        self.play(Create(ag), Write(two))
        self.play(Create(gd), Write(one))
        self.play(FadeIn(ratio, shift=UP * 0.15))
        cur = VGroup(tk, meds, mlabs, g, g_lab, ag, gd, two, one)
        self.next_slide()

        # ── 2. orthocentre ──────────────────────────────────────────────
        H = orthocentre(A, B, C)
        alts, rms, _ = altitudes(A, B, C, H)
        txt2 = panel([
            heading(r"Orthocentre $H$", ALTITUDE),
            body(r"The three \textbf{altitudes} meet at $H$."),
            body(r"Each altitude is $\perp$ to the opposite side."),
        ])
        self.play(FadeOut(cur), FadeOut(ratio), run_time=0.4)
        self.swap(txt, txt2)
        for i in range(3):
            self.play(Create(alts[i]), run_time=0.6)
            self.play(Create(rms[i]), run_time=0.3)
        h = centre_dot(H, ALTITUDE)
        h_lab = point_label(H, "H", RIGHT + UP * 0.9, ALTITUDE, buff=0.4, backed=True)
        self.play(FadeIn(h, scale=0.5), Write(h_lab))
        cur = VGroup(alts, rms, h, h_lab)
        self.next_slide()

        # ── 3. in-centre ────────────────────────────────────────────────
        I = incentre(A, B, C)
        bis, arcs = VGroup(), VGroup()
        for n, (v, p, q) in enumerate(((A, B, C), (B, C, A), (C, A, B)), start=1):
            f = bisector_foot(v, p, q)
            bis.add(seg(v, f, BISECTOR))
            arcs.add(VGroup(angle_arcs(v, p, f, n, r=0.45), angle_arcs(v, f, q, n, r=0.45)))
        r_in = np.linalg.norm(I - foot(I, B, C))
        incircle = Circle(radius=r_in, color=BISECTOR, stroke_width=3).move_to(I)
        txt3 = panel([
            heading(r"In-centre $I$", BISECTOR),
            body(r"The three \textbf{angle bisectors} meet at $I$."),
            body(r"$I$ always lies \textbf{inside} the triangle."),
        ])
        self.play(FadeOut(cur), run_time=0.4)
        self.swap(txt2, txt3)
        for i in range(3):
            self.play(Create(arcs[i]), run_time=0.4)
            self.play(Create(bis[i]), run_time=0.6)
        ic = centre_dot(I, BISECTOR)
        i_lab = point_label(I, "I", RIGHT + UP * 1.2, BISECTOR, buff=0.4, backed=True)
        self.play(FadeIn(ic, scale=0.5), Write(i_lab))
        self.next_slide()

        in_txt = panel([body(r"$I$ is the centre of the \textbf{inscribed circle}", BISECTOR, 30),
                        body(r"(it touches all three sides).", MUTED, 28)],
                       y_top=txt3.get_bottom()[1] - 0.35)
        self.play(FadeOut(bis), FadeOut(arcs), Create(incircle), FadeIn(in_txt), run_time=1.2)
        cur = VGroup(ic, i_lab, incircle)
        self.next_slide()

        # ── 4. circumcentre ─────────────────────────────────────────────
        O = circumcentre(A, B, C)
        pbs, pmarks = perp_bisectors(A, B, C, O)
        circ = Circle(radius=np.linalg.norm(A - O), color=PERP, stroke_width=3).move_to(O)
        txt4 = panel([
            heading(r"Circumcentre $O$", PERP),
            body(r"The three \textbf{perpendicular bisectors}"),
            body(r"of the sides meet at $O$."),
        ])
        self.play(FadeOut(cur), FadeOut(in_txt), run_time=0.4)
        self.swap(txt3, txt4)
        for i in range(3):
            self.play(Create(pmarks[3 * i]), Create(pmarks[3 * i + 1]), run_time=0.4)
            self.play(Create(pbs[i]), Create(pmarks[3 * i + 2]), run_time=0.6)
        oc = centre_dot(O, PERP)
        o_lab = point_label(O, "O", LEFT + DOWN * 0.9, PERP, buff=0.42, backed=True)
        self.play(FadeIn(oc, scale=0.5), Write(o_lab))
        self.next_slide()

        out_txt = panel([body(r"$O$ is the centre of the circle through", PERP, 30),
                         body(r"$A$, $B$ and $C$: $OA = OB = OC$.", PERP, 30)],
                        y_top=txt4.get_bottom()[1] - 0.35)
        radii = VGroup(*[dashed(O, P, PERP, w=2) for P in (A, B, C)])
        self.play(FadeOut(pbs), FadeOut(pmarks), Create(radii), Create(circ), FadeIn(out_txt),
                  run_time=1.4)
        self.next_slide()

        # ── 5. right-angled triangle ────────────────────────────────────
        self.play(FadeOut(VGroup(tri, labs, oc, o_lab, circ, radii, txt4, out_txt)))
        Ar, Br, Cr = np.array([-5.6, 1.4, 0]), np.array([-5.6, -2.0, 0]), np.array([-1.0, -2.0, 0])
        tri_r = triangle(Ar, Br, Cr)
        labs_r = vertex_labels([Ar, Br, Cr], "ABC")
        ra = right_mark(Br, Cr, Ar, s=0.3)
        txt5 = panel([
            heading(r"Right-angled triangle", GOLD, 42),
            body(r"$\angle ABC = 90^\circ$"),
        ])
        self.play(Create(tri_r), FadeIn(labs_r), Create(ra), FadeIn(txt5))
        self.next_slide()

        # altitudes: AB and CB are already altitudes, so they meet at B
        Fr = foot(Br, Ar, Cr)
        alt_b = seg(Br, Fr, ALTITUDE)
        rm_b = right_mark(Fr, Cr, Br)
        hr = centre_dot(Br, ALTITUDE)
        hr_lab = point_label(Br, "H", DOWN + RIGHT * 1.6, ALTITUDE, buff=0.62)
        h_rows = panel([
            body(r"$AB \perp BC$, so $AB$ and $CB$ are altitudes.", ALTITUDE, 30),
            body(r"Orthocentre $H$ = the right-angle vertex $B$.", ALTITUDE, 30),
        ], y_top=txt5.get_bottom()[1] - 0.3)
        side_ab = seg(Ar, Br, ALTITUDE, w=6)
        side_cb = seg(Cr, Br, ALTITUDE, w=6)
        self.play(Create(side_ab), Create(side_cb), FadeIn(h_rows[0]))
        self.play(Create(alt_b), Create(rm_b))
        self.play(FadeIn(hr, scale=0.5), Write(hr_lab), FadeIn(h_rows[1]))
        self.next_slide()

        # circumcentre: mid-point of hypotenuse AC
        Or = mid(Ar, Cr)
        pbs_r, pmarks_r = perp_bisectors(Ar, Br, Cr, Or)
        circ_r = Circle(radius=np.linalg.norm(Ar - Or), color=PERP, stroke_width=3).move_to(Or)
        orr = centre_dot(Or, PERP)
        or_lab = point_label(Or, "O", UP + RIGHT, PERP, buff=0.36)
        o_rows = panel([
            body(r"Circumcentre $O$ = mid-point of the", PERP, 30),
            body(r"hypotenuse $AC$ (it lies \textbf{on} the triangle).", PERP, 30),
        ], y_top=h_rows.get_bottom()[1] - 0.3)
        self.play(Create(pbs_r), Create(pmarks_r), run_time=1.2)
        self.play(FadeIn(orr, scale=0.5), Write(or_lab), FadeIn(o_rows))
        self.play(FadeOut(pbs_r), FadeOut(pmarks_r), Create(circ_r), run_time=1.0)
        self.next_slide()

        # ── 6. obtuse-angled triangle ───────────────────────────────────
        self.play(FadeOut(VGroup(tri_r, labs_r, ra, txt5, h_rows, o_rows, alt_b, rm_b, hr, hr_lab,
                                 side_ab, side_cb, orr, or_lab, circ_r)))
        Ao, Bo, Co = np.array([-4.4, 0.0, 0]), np.array([-6.0, -1.6, 0]), np.array([-0.6, -1.6, 0])
        tri_o = triangle(Ao, Bo, Co)
        labs_o = VGroup(point_label(Ao, "A", UP + RIGHT * 1.2, buff=0.36),
                        point_label(Bo, "B", LEFT + DOWN * 0.4),
                        point_label(Co, "C", RIGHT + DOWN * 0.4))
        obt = angle_arcs(Ao, Bo, Co, r=0.35)
        txt6 = panel([
            heading(r"Obtuse-angled triangle", GOLD, 42),
            body(r"$\angle BAC > 90^\circ$"),
        ])
        self.play(Create(tri_o), FadeIn(labs_o), Create(obt), FadeIn(txt6))
        self.next_slide()

        Ho = orthocentre(Ao, Bo, Co)
        alts_o, rms_o, ext_o = altitudes(Ao, Bo, Co, Ho)
        ho = centre_dot(Ho, ALTITUDE)
        ho_lab = point_label(Ho, "H", RIGHT, ALTITUDE, buff=0.34)
        h_rows = panel([
            body(r"Two altitudes meet the \textbf{extended} sides", ALTITUDE, 30),
            body(r"(dotted), so $H$ lies \textbf{outside}.", ALTITUDE, 30),
        ], y_top=txt6.get_bottom()[1] - 0.3)
        self.play(Create(alts_o), Create(rms_o), run_time=1.2)
        self.play(Create(ext_o), FadeIn(h_rows), run_time=1.2)
        self.play(FadeIn(ho, scale=0.5), Write(ho_lab))
        self.next_slide()

        Oo = circumcentre(Ao, Bo, Co)
        pbs_o, pmarks_o = perp_bisectors(Ao, Bo, Co, Oo)
        oo = centre_dot(Oo, PERP)
        oo_lab = point_label(Oo, "O", RIGHT, PERP, buff=0.34)
        o_rows = panel([
            body(r"The perpendicular bisectors meet", PERP, 30),
            body(r"\textbf{outside} too: $O$ is below $BC$.", PERP, 30),
            body(r"$G$ and $I$ are still inside.", MUTED, 30),
        ], y_top=h_rows.get_bottom()[1] - 0.3)
        self.play(VGroup(alts_o, rms_o, ext_o).animate.set_stroke(opacity=0.25), run_time=0.5)
        self.play(Create(pbs_o), Create(pmarks_o), run_time=1.2)
        self.play(FadeIn(oo, scale=0.5), Write(oo_lab), FadeIn(o_rows))
        self.next_slide()

        # ── 7. summary table ────────────────────────────────────────────
        self.play(FadeOut(VGroup(tri_o, labs_o, obt, txt6, alts_o, rms_o, ext_o, ho, ho_lab,
                                 h_rows, pbs_o, pmarks_o, oo, oo_lab, o_rows)))
        cols = [-4.6, -1.3, 1.9, 5.1]
        rows_y = [1.9, 0.9, 0.0, -0.9, -1.8]
        header = [r"", r"Acute", r"Right-angled", r"Obtuse"]
        data = [
            (r"Centroid $G$", MEDIAN, [r"inside", r"inside", r"inside"]),
            (r"In-centre $I$", BISECTOR, [r"inside", r"inside", r"inside"]),
            (r"Orthocentre $H$", ALTITUDE, [r"inside", r"right-angle vertex", r"outside"]),
            (r"Circumcentre $O$", PERP, [r"inside", r"mid-point of hypotenuse", r"outside"]),
        ]
        table = VGroup()
        hdr = VGroup(*[Tex(h, color=GOLD, font_size=34).move_to([x, rows_y[0], 0])
                       for x, h in zip(cols, header) if h])
        table.add(hdr)
        rule = Line([-6.6, 1.45, 0], [6.6, 1.45, 0], color=MUTED, stroke_width=2)
        body_rows = VGroup()
        for y, (name, col, vals) in zip(rows_y[1:], data):
            r = VGroup(Tex(name, color=col, font_size=32).move_to([cols[0], y, 0]))
            for x, v in zip(cols[1:], vals):
                c = OUTSIDE if v == "outside" else (INK if v == "inside" else col)
                r.add(Tex(v, color=c, font_size=30).move_to([x, y, 0]))
            body_rows.add(r)
        seps = VGroup(*[Line([-6.6, y - 0.45, 0], [6.6, y - 0.45, 0], color=MUTED,
                             stroke_width=1, stroke_opacity=0.4) for y in rows_y[1:-1]])
        self.play(FadeIn(hdr), Create(rule))
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in body_rows], lag_ratio=0.3),
                  Create(seps), run_time=1.6)
        note = Tex(r"$G$ and $I$ are \textbf{always} inside; $H$ and $O$ move with the shape.",
                   color=MUTED, font_size=30).move_to([0, -2.9, 0])
        self.play(FadeIn(note))
        self.wait(0.3)
        self.next_slide()
