from manim import *


class TriangleArea(Scene):
    """Geometry animation — triangle area formula with labelled sides."""

    def construct(self):
        triangle = Polygon(
            ORIGIN, RIGHT * 3, RIGHT * 3 + UP * 2,
            color=BLUE,
            fill_opacity=0.3,
        )
        base_label = MathTex(r"b", font_size=36).next_to(triangle, DOWN)
        height_label = MathTex(r"h", font_size=36).next_to(triangle, RIGHT)

        formula = MathTex(r"A = \frac{1}{2} b h", font_size=48)
        formula.to_edge(UP)

        self.play(Create(triangle))
        self.play(Write(base_label), Write(height_label))
        self.play(Write(formula))
        self.wait(2)
