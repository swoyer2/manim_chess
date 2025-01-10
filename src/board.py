from manim import *
import math
from typing import Tuple
from .pieces import Pawn, Knight, Bishop, Rook, Queen, King

class Board(Mobject):
    """
    A class to represent a chess board using Manim for visualization.

    Attributes:
    ----------
    size_of_board : int
        The number of squares along one side of the board (default is 8 for a standard chess board).
    cell_size : float
        The length of each square on the board.
    squares : dict
        A dictionary mapping coordinates (e.g., 'a1') to their corresponding Square objects.
    pieces : dict
        A dictionary mapping coordinates to their corresponding chess piece objects.
    highlighted_squares : list
        A list of coordinates of squares that are currently highlighted.
    arrows : list
        A list of arrow objects currently drawn on the board.

    Methods:
    -------
    create_board():
        Initializes the board with squares and labels.
    add_number_label(square, number):
        Adds a number label to a square.
    add_letter_label(square, letter):
        Adds a letter label to a square.
    get_square(coordinate):
        Returns the Square object at the given coordinate.
    add_piece(piece_type, is_white, coordinate):
        Adds a chess piece to the board at the specified coordinate.
    get_piece_info_from_FEN(FEN):
        Extracts piece placement information from a FEN string.
    get_coordinate_from_index(index):
        Converts a linear index to a board coordinate.
    set_board_from_FEN(FEN):
        Sets up the board pieces according to a FEN string.
    is_light_square(coordinate):
        Determines if a square is a light-colored square.
    mark_square(coordinate):
        Marks a square with a specific color.
    unmark_square(coordinate):
        Resets a square to its original color.
    highlight_square(coordinate):
        Highlights a square with a specific color.
    get_arrow_buffer(end_position, tip_position):
        Calculates buffer positions for drawing arrows.
    draw_arrow(end_coordinate, tip_coordinate):
        Draws an arrow between two squares.
    remove_piece(coordinate):
        Removes a piece from the board.
    remove_arrows():
        Removes all arrows from the board.
    move_piece(starting_coordinate, ending_coordinate):
        Moves a piece from one square to another.
    promote_piece(coordinate, piece_type):
        Promotes a piece to another piece type.
    get_piece_at_square(coordinate):
        Returns the piece at a given coordinate, if any.
    """

    def __init__(self) -> None:
        """
        Initializes the Board object.
        """
        super().__init__()
        self.size_of_board = 8
        self.cell_size = 0.8  # Size of each square in the board
        self.squares = {}  # squares[coordinate] = square
        self.create_board()
        self.pieces = {}  # pieces[coordinate] = piece
        self.highlighted_squares = []
        self.arrows = []

    def create_board(self) -> None:
        """
        Creates the chess board with squares and labels.
        """
        total_size = self.size_of_board * self.cell_size  # Total size of the board
        offset = total_size / 2  # Offset to center of board

        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        for row in range(self.size_of_board):
            for col in range(self.size_of_board):
                CHESS_GREEN = ManimColor('#769656')
                CHESS_WHITE = ManimColor('#eeeed2')
                color = CHESS_WHITE if (row + col) % 2 else CHESS_GREEN
                # Create a square for each cell in the board
                square = Square(side_length=self.cell_size)
                square.set_fill(color, opacity=1)
                square.set_stroke(color, opacity=0)
                square.move_to(np.array([col * self.cell_size - offset, row * self.cell_size - offset, 0]))

                # Add number label if first col
                if col == 0:
                    self.add_number_label(square, row + 1)

                # Add letter label if first row
                if row == 0:
                    self.add_letter_label(square, letters[col])

                # Add square to dictionary so we can access it with key
                self.squares[f'{letters[col]}{row + 1}'] = square
                # Add square to self mobj
                self.add(square)

    def add_number_label(self, square: Square, number: str) -> None:
        """
        Adds a number label to a square.

        Parameters:
        ----------
        square : Square
            The square to which the number label is added.
        number : str
            The number to be displayed on the square.
        """
        CHESS_GREEN = ManimColor('#769656')
        CHESS_WHITE = ManimColor('#eeeed2')

        offset = np.array([self.cell_size / 8, -self.cell_size / 6, 0])

        number_color = CHESS_WHITE if square.fill_color == CHESS_GREEN else CHESS_GREEN
        number = Text(f'{number}', color=number_color, font_size=14 * self.cell_size, font="Arial")
        square_top_left = square.get_center() + np.array([-self.cell_size / 2, self.cell_size / 2, 0])
        number.move_to(square_top_left + offset)
        square.add(number)

    def add_letter_label(self, square: Square, letter: str) -> None:
        """
        Adds a letter label to a square.

        Parameters:
        ----------
        square : Square
            The square to which the letter label is added.
        letter : str
            The letter to be displayed on the square.
        """
        CHESS_GREEN = ManimColor('#769656')
        CHESS_WHITE = ManimColor('#eeeed2')

        offset = np.array([-self.cell_size / 8, self.cell_size / 6, 0])

        letter_color = CHESS_WHITE if square.fill_color == CHESS_GREEN else CHESS_GREEN
        letter = Text(f'{letter}', color=letter_color, font_size=14 * self.cell_size, font="Arial")
        square_bot_right = square.get_center() + np.array([self.cell_size / 2, -self.cell_size / 2, 0])
        letter.move_to(square_bot_right + offset)
        square.add(letter)

    def get_square(self, coordinate: str) -> Square:
        """
        Returns the Square object at the given coordinate.

        Parameters:
        ----------
        coordinate : str
            The coordinate of the square (e.g., 'a1').

        Returns:
        -------
        Square
            The Square object at the specified coordinate.
        """
        return self.squares[coordinate]

    def add_piece(self, piece_type: str, is_white: bool, coordinate: str) -> None:
        """
        Adds a chess piece to the board at the specified coordinate.

        Parameters:
        ----------
        piece_type : str
            The type of the piece (e.g., 'P' for Pawn).
        is_white : bool
            True if the piece is white, False if black.
        coordinate : str
            The coordinate where the piece is to be placed.
        """
        piece_classes = {
            'P': Pawn,
            'N': Knight,
            'B': Bishop,
            'R': Rook,
            'Q': Queen,
            'K': King,
        }

        piece_class = piece_classes.get(piece_type)
        if piece_class:
            piece = piece_class(is_white=is_white).move_to(self.squares[coordinate].get_center())
            self.pieces[coordinate] = piece
            self.add(piece)
        else:
            raise ValueError(f"Unknown piece type: {piece_type}")

    def get_piece_info_from_FEN(self, FEN: str) -> str:
        """
        Extracts piece placement information from a FEN string.

        Parameters:
        ----------
        FEN : str
            The FEN string representing the board state.

        Returns:
        -------
        str
            The piece placement part of the FEN string.
        """
        return FEN.split()[0]

    def get_coordinate_from_index(self, index: int) -> str:
        """
        Converts a linear index to a board coordinate.

        Parameters:
        ----------
        index : int
            The linear index of a square.

        Returns:
        -------
        str
            The board coordinate corresponding to the index.
        """
        number_to_letter = {
            0: 'a',
            1: 'b',
            2: 'c',
            3: 'd',
            4: 'e',
            5: 'f',
            6: 'g',
            7: 'h'
        }
        coordinate = f'{number_to_letter[index % 8]}{8 - math.floor(index / 8)}'
        return coordinate

    def set_board_from_FEN(self, FEN: str="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> None:
        """
        Sets up the board pieces according to a FEN string. Default FEN is the standard start of game.

        Parameters:
        ----------
        FEN : str
            The FEN string representing the board state.
        """
        piece_info = self.get_piece_info_from_FEN(FEN)
        current_index = 0
        for char in piece_info:
            if char in {'1', '2', '3', '4', '5', '6', '7', '8'}:
                current_index += int(char)
            elif char == '/':
                pass
            else:
                coordinate = self.get_coordinate_from_index(current_index)
                self.add_piece(char.upper(), char.isupper(), coordinate)
                current_index += 1

    def is_light_square(self, coordinate: str) -> bool:
        """
        Determines if a square is a light-colored square.

        Parameters:
        ----------
        coordinate : str
            The coordinate of the square.

        Returns:
        -------
        bool
            True if the square is light-colored, False otherwise.
        """
        if coordinate[0] in {'a', 'c', 'e', 'g'}:
            if coordinate[1] in {'1', '3', '5', '7'}:
                return False
            else:
                return True
        else:
            if coordinate[1] in {'1', '3', '5', '7'}:
                return True
            else:
                return False

    def mark_square(self, coordinate: str) -> None:
        """
        Marks a square with a specific color.

        Parameters:
        ----------
        coordinate : str
            The coordinate of the square to be marked.
        """
        MARK_COLOR = ManimColor('#EC7D6A')
        self.squares[coordinate].set_fill(MARK_COLOR)

        # Add back text on square if needed
        if coordinate[1] == '1':
            self.add_letter_label(self.squares[coordinate], coordinate[0])
        if coordinate[0] == 'a':
            self.add_number_label(self.squares[coordinate], coordinate[1])

    def unmark_square(self, coordinate: str) -> None:
        """
        Resets a square to its original color.

        Parameters:
        ----------
        coordinate : str
            The coordinate of the square to be unmarked.
        """
        CHESS_GREEN = ManimColor('#769656')
        CHESS_WHITE = ManimColor('#eeeed2')

        if self.is_light_square(coordinate):
            self.squares[coordinate].set_fill(CHESS_WHITE)
        else:
            self.squares[coordinate].set_fill(CHESS_GREEN)

        # Add back text on square if needed
        if coordinate[1] == '1':
            self.add_letter_label(self.squares[coordinate], coordinate[0])
        if coordinate[0] == 'a':
            self.add_number_label(self.squares[coordinate], coordinate[1])

    def highlight_square(self, coordinate: str) -> None:
        """
        Highlights a square with a specific color.

        Parameters:
        ----------
        coordinate : str
            The coordinate of the square to be highlighted.
        """
        LIGHT_HIGHLIGHT_COLOR = ManimColor('#F7F769')
        DARK_HIGHLIGHT_COLOR = ManimColor('#BBCB2B')

        if self.is_light_square(coordinate):
            self.squares[coordinate].set_fill(LIGHT_HIGHLIGHT_COLOR)
        else:
            self.squares[coordinate].set_fill(DARK_HIGHLIGHT_COLOR)

        # Add back text on square if needed
        if coordinate[1] == '1':
            self.add_letter_label(self.squares[coordinate], coordinate[0])
        if coordinate[0] == 'a':
            self.add_number_label(self.squares[coordinate], coordinate[1])

    def get_arrow_buffer(self, end_position: np.array, tip_position: np.array) -> Tuple[np.array]:
        """
        Calculates buffer positions for drawing arrows.

        Parameters:
        ----------
        end_position : np.array
            The end position of the arrow.
        tip_position : np.array
            The tip position of the arrow.

        Returns:
        -------
        Tuple[np.array]
            The buffered end and tip positions.
        """
        # Calculate the direction vector
        subtracted_position_vectors = end_position - tip_position
        buffer = 0.25

        # Calculate the normalized direction vector
        direction_vector = subtracted_position_vectors / np.linalg.norm(subtracted_position_vectors)

        end_position_buffer = direction_vector * buffer
        tip_position_buffer = -direction_vector * buffer

        return end_position_buffer, tip_position_buffer

    def draw_arrow(self, end_coordinate: str, tip_coordinate: str) -> None:
        """
        Draws an arrow between two squares.

        Parameters:
        ----------
        end_coordinate : str
            The coordinate of the square where the arrow ends.
        tip_coordinate : str
            The coordinate of the square where the arrow starts.
        """
        ARROW_COLOR = ManimColor('#E09651')
        end_square = self.squares[end_coordinate]
        tip_square = self.squares[tip_coordinate]

        end_position = end_square.get_center()
        tip_position = tip_square.get_center()

        end_position_buffer, tip_position_buffer = self.get_arrow_buffer(end_position, tip_position)

        # Check if horizontal or vertical line or perfect diagonal like bishop
        subtracted_position_vectors = end_position - tip_position
        dir_x = subtracted_position_vectors[0]
        dir_y = subtracted_position_vectors[1]
        if dir_x == 0 or dir_y == 0 or abs(dir_x) == abs(dir_y):
            arrow = Line(stroke_width=15, stroke_opacity=.8, fill_color=ARROW_COLOR, stroke_color=ARROW_COLOR)
            arrow.reset_endpoints_based_on_tip = lambda *args: None
            arrow.set_points_as_corners([end_position - end_position_buffer, tip_position - tip_position_buffer])
            tip = arrow.create_tip()
            tip.move_to(tip_position - tip_position_buffer)
            finished_arrow = VGroup(arrow, tip)
            self.add(finished_arrow)
        else:
            arrow0 = Line(stroke_width=15, stroke_opacity=.8, fill_color=ARROW_COLOR, stroke_color=ARROW_COLOR)
            arrow0.reset_endpoints_based_on_tip = lambda *args: None
            arrow1 = Line(stroke_width=15, stroke_opacity=.8, fill_color=ARROW_COLOR, stroke_color=ARROW_COLOR)
            arrow1.reset_endpoints_based_on_tip = lambda *args: None

            if dir_y > 0:
                buffer_y = np.array([0, 0.25, 0])
            else:
                buffer_y = np.array([0, -0.25, 0])

            if dir_x > 0:
                buffer_x = np.array([0.25, 0, 0])
            else:
                buffer_x = np.array([-0.25, 0, 0])

            tip_buffer = -0.07 if dir_x > 0 else 0.07

            if abs(dir_y) > abs(dir_x):
                arrow0.set_points_as_corners([end_position - buffer_y, np.array([end_position[0], tip_position[1], 0])])
                arrow1.set_points_as_corners([np.array([end_position[0]-tip_buffer, tip_position[1], 0]), tip_position + buffer_x])
                tip = arrow1.create_tip()
                tip.move_to(tip_position + buffer_x)
            else:
                arrow0.set_points_as_corners([end_position - buffer_x, np.array([tip_position[0], end_position[1], 0])])
                arrow1.set_points_as_corners([np.array([tip_position[0]-tip_buffer, end_position[1], 0]), tip_position + buffer_y])
                tip = arrow1.create_tip()
                tip.move_to(tip_position + buffer_y)

            finished_arrow = VGroup(arrow0, arrow1, tip)
            self.add(finished_arrow)
        self.arrows.append(finished_arrow)

    def remove_piece(self, coordinate: str) -> None:
        """
        Removes a piece from the board.

        Parameters:
        ----------
        coordinate : str
            The coordinate of the piece to be removed.
        """
        piece_to_remove = self.pieces[coordinate]
        self.remove(piece_to_remove)
        del piece_to_remove
        del self.pieces[coordinate]

    def remove_arrows(self) -> None:
        """
        Removes all arrows from the board.
        """
        for arrow in self.arrows:
            self.remove(arrow)

    def move_piece(self, starting_coordinate: str, ending_coordinate: str) -> None:
        """
        Moves a piece from one square to another.

        Parameters:
        ----------
        starting_coordinate : str
            The coordinate of the square where the piece is currently located.
        ending_coordinate : str
            The coordinate of the square where the piece is to be moved.
        """
        if ending_coordinate in self.pieces.keys():
            self.remove_piece(ending_coordinate)
        try:
            piece_to_move = self.pieces[starting_coordinate]
            self.pieces[ending_coordinate] = piece_to_move
            del self.pieces[starting_coordinate]

            for coordinate in self.highlighted_squares:
                self.unmark_square(coordinate)
            self.highlighted_squares = []

            piece_to_move.move_to(self.squares[ending_coordinate].get_center())
            self.highlight_square(starting_coordinate)
            self.highlight_square(ending_coordinate)
            self.highlighted_squares.append(starting_coordinate)
            self.highlighted_squares.append(ending_coordinate)
        except Exception as e:
            print(f'{e} has no piece associated')

    def promote_piece(self, coordinate: str, piece_type: str) -> None:
        """
        Promotes a piece to another piece type.

        Parameters:
        ----------
        coordinate : str
            The coordinate of the piece to be promoted.
        piece_type : str
            The type of piece to which the piece is promoted (e.g., 'Q' for Queen).
        """
        piece_color = self.pieces[coordinate].is_white
        self.remove_piece(coordinate)
        self.add_piece(piece_type.upper(), piece_color, coordinate)

    def get_piece_at_square(self, coordinate: str):
        """
        Returns the piece at a given coordinate, if any.

        Parameters:
        ----------
        coordinate : str
            The coordinate of the square to check for a piece.

        Returns:
        -------
        object or None
            The piece object at the specified coordinate, or None if no piece is present.
        """
        if coordinate in self.pieces:
            return self.pieces[coordinate]
        else:
            return None  # No piece at the given coordinate
