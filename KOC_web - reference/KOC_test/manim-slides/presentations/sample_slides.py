from manim import *
from manim_slides import Slide


class MathLessonSlides(Slide):
    """Sample Manim Slides presentation — press Space/Arrow to advance."""

    def construct(self):
        title = Text("DSE Mathematics", font_size=52)
        subtitle = Text("Interactive Lesson", font_size=32, color=GREY_B)
        subtitle.next_to(title, DOWN)

        self.play(Write(title), Write(subtitle))
        self.next_slide()

        eq = MathTex(r"\frac{a}{b} = \frac{c}{d}", font_size=64)
        self.play(Write(eq))
        self.next_slide()

        cross = MathTex(r"ad = bc", font_size=64, color=YELLOW)
        self.play(Transform(eq, cross))
        self.next_slide()

        thanks = Text("Thank you!", font_size=48)
        self.play(FadeOut(eq), FadeIn(thanks))
        self.next_slide()
