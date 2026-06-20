from manim import *


class QuadraticFormula(Scene):
    """Sample Manim scene — quadratic formula with step-by-step reveal."""

    def construct(self):
        title = Text("Quadratic Formula", font_size=48)
        title.to_edge(UP)

        formula = MathTex(
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            font_size=60,
        )
        formula.next_to(title, DOWN, buff=1.0)

        self.play(Write(title))
        self.play(Write(formula))
        self.wait(2)
