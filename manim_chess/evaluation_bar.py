from manim import *
from typing import Tuple

class EvaluationBar(Mobject):
    """
    A class to represent an evaluation bar using Manim for visualization.

    Attributes:
    ----------
    evaluation : float
        The current evaluation value, default is 0.0.
    BLACK : ManimColor
        The color used for the black portion of the bar.
    WHITE : ManimColor
        The color used for the white portion of the bar.
    black_rectangle : Rectangle
        The rectangle representing the black portion of the evaluation bar.
    white_rectangle : Rectangle
        The rectangle representing the white portion of the evaluation bar.
    bot_text : Text
        The text object displaying the evaluation at the bottom of the bar.
    top_text : Text
        The text object displaying the evaluation at the top of the bar.
    """

    def __init__(self, evaluation=0.0) -> None:
        """
        Initializes the EvaluationBar object with default or specified evaluation.

        Parameters:
        ----------
        evaluation : float, optional
            The initial evaluation value (default is 0.0).
        """
        super().__init__()
        self.evaluation = evaluation
        self.BLACK = ManimColor("#403D39")
        self.WHITE = ManimColor("#ffffff")
        self.black_rectangle = Rectangle(width=0.25, height=6.4, stroke_color=self.BLACK, fill_opacity=1).set_fill(self.BLACK)
        self.white_rectangle = Rectangle(width=0.25, height=3.2, stroke_color=self.WHITE, fill_opacity=1).set_fill(self.WHITE)
        self.bot_text = Text('0.0', font="Arial").move_to(self.black_rectangle.get_bottom() + np.array([0, 0.2, 0])).set_fill(self.BLACK).scale(0.2)
        self.top_text = Text('0.0', font="Arial").move_to(self.black_rectangle.get_top() + np.array([0, -0.2, 0])).set_fill(self.WHITE).scale(0.2)
        self.__add_rectangles()

    def set_evaluation(self, evaluation: float):
        """
        Updates the evaluation value and adjusts the visual representation accordingly.

        Parameters:
        ----------
        evaluation : float
            The new evaluation value to be set.
        
        Returns:
        -------
        list
            A list of Transform animations to update the evaluation bar.
        """
        self.evaluation = evaluation
        text_transformation = None
        if self.evaluation > 0:
            text_transformation = Transform(
                self.bot_text, 
                Text(f'{self.evaluation:.1f}', font="Arial").move_to(self.black_rectangle.get_bottom() + np.array([0, 0.2, 0])).set_fill(self.BLACK).scale(0.2)
            )
        else:
            text_transformation = Transform(
                self.bot_text,
                Text(f'{self.evaluation:.1f}', font="Arial").move_to(self.black_rectangle.get_top() + np.array([0, -0.2, 0])).set_fill(self.WHITE).scale(0.2)
            )

        height_from_evaluation = 0.737063 * self.evaluation + 3.2
        rect_height = min(max(0.32, height_from_evaluation), 6.18)
        pos = self.black_rectangle.get_bottom() + np.array([0, rect_height / 2, 0])
        new_rect = Rectangle(width=0.25, height=rect_height, stroke_color=self.WHITE, fill_opacity=1).set_fill(self.WHITE).move_to(pos)
        return [Transform(self.white_rectangle, new_rect), text_transformation]

    def __add_rectangles(self) -> None:
        """
        Adds the rectangles and text to the evaluation bar.
        """
        self.add(self.black_rectangle)
        self.add(self.white_rectangle.shift(DOWN * 1.6))
        self.add(self.bot_text)