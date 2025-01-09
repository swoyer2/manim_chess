import os
from manim import *

class Pawn(Mobject):
    """
    A class to represent a Pawn chess piece using Manim for visualization.

    Attributes:
    ----------
    piece_size : float
        The size of the chess piece.
    is_white : bool
        A boolean indicating if the piece is white.

    Methods:
    -------
    create_svg():
        Creates and adds the SVG representation of the pawn to the Mobject.
    """
    def __init__(self, is_white: bool, piece_size=1.1) -> None:
        """
        Initializes the Pawn object with specified color and size.

        Parameters:
        ----------
        is_white : bool
            Indicates if the pawn is white.
        piece_size : float, optional
            The size of the pawn (default is 1.1).
        """
        super().__init__()
        self.piece_size = piece_size
        self.is_white = is_white
        self.create_svg()

    def create_svg(self) -> SVGMobject:
        """
        Creates the SVG representation of the pawn and adds it to the Mobject.
        """
        svg_path = os.path.join(os.path.dirname(__file__), 'piece_svgs', 'wP.svg' if self.is_white else 'bP.svg')
        self.add(SVGMobject(svg_path).scale(self.piece_size / 4))

class Knight(Mobject):
    """
    A class to represent a Knight chess piece using Manim for visualization.

    Attributes:
    ----------
    piece_size : float
        The size of the chess piece.

    Methods:
    -------
    create_svg(is_white):
        Creates and adds the SVG representation of the knight to the Mobject.
    """
    def __init__(self, is_white: bool, piece_size=1.1) -> None:
        """
        Initializes the Knight object with specified color and size.

        Parameters:
        ----------
        is_white : bool
            Indicates if the knight is white.
        piece_size : float, optional
            The size of the knight (default is 1.1).
        """
        super().__init__()
        self.piece_size = piece_size
        self.create_svg(is_white)

    def create_svg(self, is_white: bool) -> SVGMobject:
        """
        Creates the SVG representation of the knight and adds it to the Mobject.

        Parameters:
        ----------
        is_white : bool
            Indicates if the knight is white.
        """
        svg_path = os.path.join(os.path.dirname(__file__), 'piece_svgs', 'wN.svg' if is_white else 'bN.svg')
        self.add(SVGMobject(svg_path).scale(self.piece_size / 4))

class Bishop(Mobject):
    """
    A class to represent a Bishop chess piece using Manim for visualization.

    Attributes:
    ----------
    piece_size : float
        The size of the chess piece.

    Methods:
    -------
    create_svg(is_white):
        Creates and adds the SVG representation of the bishop to the Mobject.
    """
    def __init__(self, is_white: bool, piece_size=1.1) -> None:
        """
        Initializes the Bishop object with specified color and size.

        Parameters:
        ----------
        is_white : bool
            Indicates if the bishop is white.
        piece_size : float, optional
            The size of the bishop (default is 1.1).
        """
        super().__init__()
        self.piece_size = piece_size
        self.create_svg(is_white)

    def create_svg(self, is_white: bool) -> SVGMobject:
        """
        Creates the SVG representation of the bishop and adds it to the Mobject.

        Parameters:
        ----------
        is_white : bool
            Indicates if the bishop is white.
        """
        svg_path = os.path.join(os.path.dirname(__file__), 'piece_svgs', 'wB.svg' if is_white else 'bB.svg')
        self.add(SVGMobject(svg_path).scale(self.piece_size / 4))

class Rook(Mobject):
    """
    A class to represent a Rook chess piece using Manim for visualization.

    Attributes:
    ----------
    piece_size : float
        The size of the chess piece.

    Methods:
    -------
    create_svg(is_white):
        Creates and adds the SVG representation of the rook to the Mobject.
    """
    def __init__(self, is_white: bool, piece_size=1.1) -> None:
        """
        Initializes the Rook object with specified color and size.

        Parameters:
        ----------
        is_white : bool
            Indicates if the rook is white.
        piece_size : float, optional
            The size of the rook (default is 1.1).
        """
        super().__init__()
        self.piece_size = piece_size
        self.create_svg(is_white)

    def create_svg(self, is_white: bool) -> SVGMobject:
        """
        Creates the SVG representation of the rook and adds it to the Mobject.

        Parameters:
        ----------
        is_white : bool
            Indicates if the rook is white.
        """
        svg_path = os.path.join(os.path.dirname(__file__), 'piece_svgs', 'wR.svg' if is_white else 'bR.svg')
        self.add(SVGMobject(svg_path).scale(self.piece_size / 4))

class Queen(Mobject):
    """
    A class to represent a Queen chess piece using Manim for visualization.

    Attributes:
    ----------
    piece_size : float
        The size of the chess piece.

    Methods:
    -------
    create_svg(is_white):
        Creates and adds the SVG representation of the queen to the Mobject.
    """
    def __init__(self, is_white: bool, piece_size=1.1) -> None:
        """
        Initializes the Queen object with specified color and size.

        Parameters:
        ----------
        is_white : bool
            Indicates if the queen is white.
        piece_size : float, optional
            The size of the queen (default is 1.1).
        """
        super().__init__()
        self.piece_size = piece_size
        self.create_svg(is_white)

    def create_svg(self, is_white: bool) -> SVGMobject:
        """
        Creates the SVG representation of the queen and adds it to the Mobject.

        Parameters:
        ----------
        is_white : bool
            Indicates if the queen is white.
        """
        svg_path = os.path.join(os.path.dirname(__file__), 'piece_svgs', 'wQ.svg' if is_white else 'bQ.svg')
        self.add(SVGMobject(svg_path).scale(self.piece_size / 4))

class King(Mobject):
    """
    A class to represent a King chess piece using Manim for visualization.

    Attributes:
    ----------
    piece_size : float
        The size of the chess piece.

    Methods:
    -------
    create_svg(is_white):
        Creates and adds the SVG representation of the king to the Mobject.
    """
    def __init__(self, is_white: bool, piece_size=1.1) -> None:
        """
        Initializes the King object with specified color and size.

        Parameters:
        ----------
        is_white : bool
            Indicates if the king is white.
        piece_size : float, optional
            The size of the king (default is 1.1).
        """
        super().__init__()
        self.piece_size = piece_size
        self.create_svg(is_white)

    def create_svg(self, is_white: bool) -> SVGMobject:
        """
        Creates the SVG representation of the king and adds it to the Mobject.

        Parameters:
        ----------
        is_white : bool
            Indicates if the king is white.
        """
        svg_path = os.path.join(os.path.dirname(__file__), 'piece_svgs', 'wK.svg' if is_white else 'bK.svg')
        self.add(SVGMobject(svg_path).scale(self.piece_size / 4))