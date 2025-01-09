from .board import *
from .evaluation_bar import *

import time
import re
from typing import Tuple

DEFAULT_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

def play_game(scene, board: Board, moves: list[Tuple[str, str, str]], eval_bar: EvaluationBar = None, evals: list[float] = None) -> None:
    """
    Executes a series of chess moves on a given board and updates the evaluation bar if provided.

    Parameters:
    ----------
    scene : Scene
        The Manim scene where the game is being played.
    board : Board
        The chess board object on which the moves are executed.
    moves : list of Tuple[str, str]
        A list of moves, where each move is a tuple containing the starting and ending positions, 
        and optionally a promotion piece.
    eval_bar : EvaluationBar, optional
        An evaluation bar object to visualize the evaluation of the board state (default is None).
    evals : list of float, optional
        A list of evaluation scores corresponding to each move (default is None).

    Returns:
    -------
    None
    """
    # Resize the evals array if not enough
    if not evals:
        evals = []
    while len(evals) < len(moves):
        evals.append(0)

    for move, evaluation in zip(moves, evals):
        start_time = time.time()  # Start timing

        # Check for en passant, if True then remove the captured piece
        if __check_for_en_passant(board, move):
            direction = int(move[1][1]) - int(move[0][1])
            if direction == 1:
                board.remove_piece(f'{move[1][0]}{int(move[1][1])-1}')
            else:
                board.remove_piece(f'{move[1][0]}{int(move[1][1])+1}')
        
        # Check for castling, if True move the rook next to the king
        if __check_for_castle(board, move):
            letters_in_order = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
            direction = letters_in_order[move[1][0]] - letters_in_order[move[0][0]]
            if direction > 1:
                board.move_piece(f'h{move[0][1]}', f'f{move[0][1]}')
            else:
                board.move_piece(f'a{move[0][1]}', f'd{move[0][1]}')

        board.move_piece(move[0], move[1])
        if move[2]:
            board.promote_piece(move[1], move[2])

        if eval_bar:
            scene.play(eval_bar.set_evaluation(evaluation))
        
    
        end_time = time.time()  # End timing
        print(f"Took {end_time - start_time:.2f} seconds to execute.")  # Print the duration
        scene.wait()

def __check_for_en_passant(board: Board, move: Tuple[str, str, str]) -> bool:
    """
    Checks if a given move is an en passant capture.

    Parameters:
    ----------
    board : Board
        The chess board object.
    move : Tuple[str, str]
        A tuple representing the starting and ending positions of the move.

    Returns:
    -------
    bool
        True if the move is an en passant capture, False otherwise.
    """
    starting_square = move[0]
    ending_square = move[1]
    if type(board.get_piece_at_square(starting_square)).__name__ == "Pawn":  # Check if the moving piece is a pawn
        if not board.get_piece_at_square(ending_square):  # Check if the ending square is empty
            if starting_square[0] != ending_square[0]:  # Check if the pawn did not move straight
                return True
    return False

def __check_for_castle(board: Board, move: Tuple[str, str, str]) -> bool:
    """
    Checks if a given move is a castling move.

    Parameters:
    ----------
    board : Board
        The chess board object.
    move : Tuple[str, str]
        A tuple representing the starting and ending positions of the move.

    Returns:
    -------
    bool
        True if the move is a castling move, False otherwise.
    """
    letters_in_order = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
    starting_square = move[0]
    ending_square = move[1]
    if type(board.get_piece_at_square(starting_square)).__name__ == "King":  # Check if the moving piece is a king
        # Check if the king moved more than 1 square left or right
        distance = abs(letters_in_order[ending_square[0]] - letters_in_order[starting_square[0]])
        if distance > 1:
            return True
    return False

def __get_coordinate_from_index(index: int) -> str:
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

def __get_index_from_FEN(FEN: str, position_in_FEN: int) -> int:
    piece_info = FEN.split()[0][:position_in_FEN]
    current_index = 0
    for char in piece_info:
        if char in {'1', '2', '3', '4', '5', '6', '7', '8'}:
            current_index += int(char)
        elif char == '/':
            pass
        else:
            current_index += 1
    return current_index

def __find_all_pieces(FEN: str) -> list[str]:
    """
    Returns all coordiantes that contain a piece.

    Parameters:
    ----------
    FEN: str
        The FEN string of the current board position.
    """
    coordinates = []
    for i, char in enumerate(FEN.split()[0]):
        if char not in {'/', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            index = __get_index_from_FEN(FEN, i)
            coordinate = __get_coordinate_from_index(index)
            coordinates.append(coordinate)
    return coordinates

def __find_piece(FEN: str, piece_type: str) -> list[str]:
    """
    Returns all coordiantes the piece type was found at.

    Parameters:
    ----------
    FEN: str
        The FEN string of the current board position.
    piece_type: str
        The type of piece you would like to find. Case sensitive, lowercase for white
        upper case for black.

    """
    coordinates = []
    for i, char in enumerate(FEN.split()[0]):
        if char == piece_type:
            index = __get_index_from_FEN(FEN, i)
            coordinate = __get_coordinate_from_index(index)
            coordinates.append(coordinate)
    return coordinates

def __castling_notation(algebraic_notation, FEN) -> Tuple[str, str, str]:
    turn = FEN.split()[1] # w or b
    castling_king_side = True if algebraic_notation == 'O-O' else False

    if turn == 'w': # If player is white
        move = ('e1', 'g1', "") if castling_king_side else ('e1', 'c1', "") # King side castling or queen side castling
    else: # If player is black
       move = ('e8', 'g8', "") if castling_king_side else ('e8', 'c8', "") # King side castling or queen side castling
    return move

def pawn_algebraic_notation(algebraic_notation, FEN) -> Tuple[str, str, str]:
    # If the piece is a pawn than the starting square can be determined by seeing which pawn can go to the ending square
    # 
    # NOTE ascending means +1 rank and descending means -1 rank
    #
    # This can be done by:
    # 1. If not capturing, check the square descending from the ending square (or ascending if black) if a pawn 
    #    is there than that is the starting square, else it is the square descending from that square (or ascending if black)
    # 2. If capturing than the file is specified as first char on algebraic notation. Then the only needed information is the rank
    #    which can be determined by the turn (w or b) since white can only move ascending with pawns and black can only move descending 
    #    with pawns.
    # 3. If promoting than promotion piece is specified, make sure to check if the checking or checkmating since that moves the promotion
    #    piece to the second to last char
    turn = FEN.split()[1]
    capturing = True if 'x' in algebraic_notation else False
    promoting = True if '=' in algebraic_notation else False
    checkmate = True if '#' in algebraic_notation else False
    check = True if '+' in algebraic_notation else False

    ending_square_index = promoting * 2 + checkmate or check # this shifts the index over depending on if it has the + # or =piece_type

    ending_square_file = algebraic_notation[-(2+ending_square_index)]
    ending_square_rank = int(algebraic_notation[-(1+ending_square_index)])

    all_piece_coordiantes = __find_all_pieces(FEN)

    if not capturing:  
        starting_square_file = ending_square_file
        if turn == 'w':
            if f'{ending_square_file}{ending_square_rank-1}' in all_piece_coordiantes:
                starting_square_rank = ending_square_rank-1
            else:
                starting_square_rank = ending_square_rank-2
        else:
            if f'{ending_square_file}{ending_square_rank+1}' in all_piece_coordiantes:
                starting_square_rank = ending_square_rank+1
            else:
                starting_square_rank = ending_square_rank+2

    else:
        starting_square_file = algebraic_notation[0]
        starting_square_rank = f'{ending_square_rank-1}' if turn == 'w' else f'{ending_square_rank+1}'
    
    if promoting:
        promotion_piece = algebraic_notation[-2] if check or checkmate else algebraic_notation[-1]
        move = (f'{starting_square_file}{starting_square_rank}', f'{ending_square_file}{ending_square_rank}', promotion_piece)
    else:
        move = (f'{starting_square_file}{starting_square_rank}', f'{ending_square_file}{ending_square_rank}', '')

    return move

def knight_algebraic_notation(algebraic_notation, FEN) -> Tuple[str, str, str]:
    # If the piece is a knight than the starting square can be determined by seeing which knight can go to the ending square,
    # if the case where 2+ knights can go to the starting square the algebraic notation will give enough information to determine the
    # correct knight
    #
    # This can be done by:
    # 1. Check all squares around the ending square with a knight's movement, if the correct color knight is found (based on turn)
    #    and it is the only knight that is found, the position that knight is at is the starting square.
    # 2. If ambiguous check third char of algebraic notation if it is a letter (x or file specification) than the correct knight 
    #    has the second char in it's coordinate
    # 3. If ambiguous and the third char is not a letter than the correct knight is given by the coordinate secondchar + thirdchar
    #    of the algebraic notation
    turn = FEN.split()[1]
    knight_movements = [(-2, -1), (-1, -2), (2, 1), (1, 2), (-2, 1), (1, -2), (2, -1), (-1, 2)] # (x, y)

    checkmate = True if '#' in algebraic_notation else False
    check = True if '+' in algebraic_notation else False

    ending_square_index = checkmate or check # this shifts the index over depending on if it has the + #

    ending_square_file = algebraic_notation[-(2+ending_square_index)]
    ending_square_rank = int(algebraic_notation[-(1+ending_square_index)])

    piece_type = 'N' if turn == 'w' else 'n'
    knight_coordinates = __find_piece(FEN, piece_type)

    coordinates_that_passed = [] # A list of all the knight coordinates that could have moved to the ending square

    # Gives the letters that are to the right and to the left with the order of [current_postion, right_one, right_two, left_two, left_one]
    x_coordinate_to_letter = {
        'a': ['a', 'b', 'c', None, None],
        'b': ['b', 'c', 'd', None, 'a' ],
        'c': ['c', 'd', 'e', 'a', 'b'  ],
        'd': ['d', 'e', 'f', 'b', 'c'  ],
        'e': ['e', 'f', 'g', 'c', 'd'  ],
        'f': ['f', 'g', 'h', 'd', 'e'  ],
        'g': ['g', 'h', None, 'e', 'f' ],
        'h': ['h', None, None, 'f', 'g']
    }
    for movement in knight_movements:
        file_to_check = x_coordinate_to_letter[ending_square_file][movement[0]]
        rank_to_check = int(ending_square_rank)+movement[1]
        if f'{file_to_check}{rank_to_check}' in knight_coordinates:
            coordinates_that_passed.append(f'{file_to_check}{rank_to_check}')

    if len(coordinates_that_passed) == 1:
        return (coordinates_that_passed[0], f'{ending_square_file}{ending_square_rank}', '')

    else: # Ambiguous
        if algebraic_notation[2] in {'x', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}:
            for knight_coordinate in coordinates_that_passed:
                if algebraic_notation[1] in knight_coordinate:
                    return (knight_coordinate, f'{ending_square_file}{ending_square_rank}', '')
        else:
            return (algebraic_notation[1:3], f'{ending_square_file}{ending_square_rank}', '')

def bishop_algebraic_notation(algebraic_notation, FEN) -> Tuple[str, str, str]:
    # If the piece is a bishop than the starting square can be determined by seeing which bishop can go to the ending square,
    # if the case where 2+ bishops can go to the starting square the algebraic notation will give enough information to determine the
    # correct bishop
    #
    # This can be done by:
    # 1. Check each square diagnol one square at a time. Like this:
    #    2###2
    #    #1#1#
    #    ##O##
    #    #1#1#
    #    2###2
    #    If the search runs into a piece and it's a bishop goto 2.) if not ambiguous than return the coordinate of that bishop
    #    If the search runs into a piece that is not a bishop than stop searching in that direction 
    # 2. Check if ambiguous by seeing the length of the algebraic notation.
    #    a.) If checkmate or check, length can be +1
    #    b.) If capturing, length can be +1
    #    c.) Check if length is 2 greater than 3+(1 if check or checkmate)+(1 if capturing) if so it is ambiguous and the starting coordinate
    #        is algebraic_notation[1:2]
    #    d.) Check if length is 1 greater than 3+(1 if check or checkmate)+(1 if capturing) if so it is ambiguous and the specifier is
    #        algebraic_notation[1], so if the bishop that was found has that specifier in the coordinate than it is the correct bishop
    #    e.) else not ambiguous
    turn = FEN.split()[1]
    bishop_direction = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    checkmate = True if '#' in algebraic_notation else False
    check = True if '+' in algebraic_notation else False

    capturing = True if 'x' in algebraic_notation else False

    ending_square_index = checkmate or check # this shifts the index over depending on if it has the + #

    ending_square_file = algebraic_notation[-(2+ending_square_index)]
    ending_square_rank = int(algebraic_notation[-(1+ending_square_index)])

    piece_type = 'B' if turn == 'w' else 'b'
    bishop_coordiantes = __find_piece(FEN, piece_type)
    all_pieces = __find_all_pieces(FEN)

    # Gives the letters that are to the right and to the left with the order of [current_positon, right_one, left_one]
    x_coordinate_to_letter = {
        'a': ['a', 'b', None],
        'b': ['b', 'c', 'a' ],
        'c': ['c', 'd', 'b' ],
        'd': ['d', 'e', 'c' ],
        'e': ['e', 'f', 'd' ],
        'f': ['f', 'g', 'e' ],
        'g': ['g', 'h', 'f' ],
        'h': ['h', None, 'g']
    }
    for direction in bishop_direction:
        current_search_coordinate = f'{ending_square_file}{ending_square_rank}'
        hit_piece = False
        new_file = x_coordinate_to_letter[current_search_coordinate[0]][direction[0]]
        new_rank = int(current_search_coordinate[1]) + direction[1]
        while not hit_piece:
            if not new_file or new_rank < 1 or new_rank > 8:
                hit_piece = True
            else:
                if f'{new_file}{new_rank}' in bishop_coordiantes:
                    non_ambiguous_length = 3
                    if checkmate or check:
                        non_ambiguous_length += 1
                    if capturing:
                        non_ambiguous_length += 1
                    if len(algebraic_notation) == 2 + non_ambiguous_length:
                        return (algebraic_notation[1:2], f'{ending_square_file}{ending_square_rank}', '')
                    if len(algebraic_notation) == 1 + non_ambiguous_length:
                        if algebraic_notation[1] in f'{new_file}{new_rank}':
                            return (f'{new_file}{new_rank}', f'{ending_square_file}{ending_square_rank}', '')
                        else:
                            hit_piece = True
                    if len(algebraic_notation) == non_ambiguous_length:
                        return (f'{new_file}{new_rank}', f'{ending_square_file}{ending_square_rank}', '')
                elif f'{new_file}{new_rank}' in all_pieces:
                    hit_piece = True
                else:
                    new_file = x_coordinate_to_letter[new_file][direction[0]]
                    new_rank = int(new_rank) + direction[1]


def rook_algebraic_notation(algebraic_notation, FEN) -> Tuple[str, str, str]:
    # Works almost the same as bishop just with horizontal and vertical movement
    turn = FEN.split()[1]
    rook_direction = [(-1, 0), (0, 1), (0, -1), (1, 0)]

    checkmate = True if '#' in algebraic_notation else False
    check = True if '+' in algebraic_notation else False

    capturing = True if 'x' in algebraic_notation else False

    ending_square_index = checkmate or check # this shifts the index over depending on if it has the + #

    ending_square_file = algebraic_notation[-(2+ending_square_index)]
    ending_square_rank = int(algebraic_notation[-(1+ending_square_index)])

    piece_type = 'R' if turn == 'w' else 'r'
    rook_coordiantes = __find_piece(FEN, piece_type)
    all_pieces = __find_all_pieces(FEN)

    # Gives the letters that are to the right and to the left with the order of [current_position, right_one, left_one]
    x_coordinate_to_letter = {
        'a': ['a', 'b', None],
        'b': ['b', 'c', 'a' ],
        'c': ['c', 'd', 'b' ],
        'd': ['d', 'e', 'c' ],
        'e': ['e', 'f', 'd' ],
        'f': ['f', 'g', 'e' ],
        'g': ['g', 'h', 'f' ],
        'h': ['h', None, 'g']
    }
    for direction in rook_direction:
        current_search_coordinate = f'{ending_square_file}{ending_square_rank}'
        hit_piece = False
        new_file = x_coordinate_to_letter[current_search_coordinate[0]][direction[0]]
        new_rank = int(current_search_coordinate[1]) + direction[1]
        while not hit_piece:
            if not new_file or new_rank < 1 or new_rank > 8:
                hit_piece = True
            else:
                if f'{new_file}{new_rank}' in rook_coordiantes:
                    non_ambiguous_length = 3
                    if checkmate or check:
                        non_ambiguous_length += 1
                    if capturing:
                        non_ambiguous_length += 1
                    if len(algebraic_notation) == 2 + non_ambiguous_length:
                        return (algebraic_notation[1:2], f'{ending_square_file}{ending_square_rank}', '')
                    if len(algebraic_notation) == 1 + non_ambiguous_length:
                        if algebraic_notation[1] in f'{new_file}{new_rank}':
                            return (f'{new_file}{new_rank}', f'{ending_square_file}{ending_square_rank}', '')
                        else:
                            hit_piece = True
                    if len(algebraic_notation) == non_ambiguous_length:
                        return (f'{new_file}{new_rank}', f'{ending_square_file}{ending_square_rank}', '')
                elif f'{new_file}{new_rank}' in all_pieces:
                    hit_piece = True
                else:
                    new_file = x_coordinate_to_letter[new_file][direction[0]]
                    new_rank = int(new_rank) + direction[1]

def queen_algebraic_notation(algebraic_notation, FEN) -> Tuple[str, str, str]:
    # Works like bishop + rook
    turn = FEN.split()[1]
    queen_direction = [(-1, 0), (0, 1), (0, -1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    checkmate = True if '#' in algebraic_notation else False
    check = True if '+' in algebraic_notation else False

    capturing = True if 'x' in algebraic_notation else False

    ending_square_index = checkmate or check # this shifts the index over depending on if it has the + #

    ending_square_file = algebraic_notation[-(2+ending_square_index)]
    ending_square_rank = int(algebraic_notation[-(1+ending_square_index)])

    piece_type = 'Q' if turn == 'w' else 'q'
    queen_coordiantes = __find_piece(FEN, piece_type)
    all_pieces = __find_all_pieces(FEN)

    # Gives the letters that are to the right and to the left with the order of [current_position, right_one, left_one]
    x_coordinate_to_letter = {
        'a': ['a', 'b', None],
        'b': ['b', 'c', 'a' ],
        'c': ['c', 'd', 'b' ],
        'd': ['d', 'e', 'c' ],
        'e': ['e', 'f', 'd' ],
        'f': ['f', 'g', 'e' ],
        'g': ['g', 'h', 'f' ],
        'h': ['h', None, 'g']
    }
    for direction in queen_direction:
        current_search_coordinate = f'{ending_square_file}{ending_square_rank}'
        hit_piece = False
        new_file = x_coordinate_to_letter[current_search_coordinate[0]][direction[0]]
        new_rank = int(current_search_coordinate[1]) + direction[1]
        while not hit_piece:
            if not new_file or new_rank < 1 or new_rank > 8:
                hit_piece = True
            else:
                if f'{new_file}{new_rank}' in queen_coordiantes:
                    non_ambiguous_length = 3
                    if checkmate or check:
                        non_ambiguous_length += 1
                    if capturing:
                        non_ambiguous_length += 1
                    if len(algebraic_notation) == 2 + non_ambiguous_length:
                        return (algebraic_notation[1:2], f'{ending_square_file}{ending_square_rank}', '')
                    if len(algebraic_notation) == 1 + non_ambiguous_length:
                        if algebraic_notation[1] in f'{new_file}{new_rank}':
                            return (f'{new_file}{new_rank}', f'{ending_square_file}{ending_square_rank}', '')
                        else:
                            hit_piece = True
                    if len(algebraic_notation) == non_ambiguous_length:
                        return (f'{new_file}{new_rank}', f'{ending_square_file}{ending_square_rank}', '')
                elif f'{new_file}{new_rank}' in all_pieces:
                    hit_piece = True
                else:
                    new_file = x_coordinate_to_letter[new_file][direction[0]]
                    new_rank = int(new_rank) + direction[1]

def king_algebraic_notation(algebraic_notation, FEN) -> Tuple[str, str, str]:
    # If the piece is a king than the starting square can be determined by seeing where the king is
    turn = FEN.split()[1]

    checkmate = True if '#' in algebraic_notation else False
    check = True if '+' in algebraic_notation else False

    ending_square_index = checkmate or check # this shifts the index over depending on if it has the + #

    ending_square_file = algebraic_notation[-(2+ending_square_index)]
    ending_square_rank = int(algebraic_notation[-(1+ending_square_index)])

    piece_type = 'K' if turn == 'w' else 'k'
    king_coordinate = __find_piece(FEN, piece_type)[0]

    return (king_coordinate, f'{ending_square_file}{ending_square_rank}', '')

def convert_from_algebraic_notation(algebraic_notation: str, FEN: str) -> Tuple[str, str, str]:
    """
    Converts a move from algebraic notation to a tuple representing the starting and ending squares. Use this for
    single moves.

    Parameters:
    ----------
    algebraic_notation : str
    The move in algebraic notation, e.g., 'e2e4', 'Nf3', 'O-O', etc.
    board : Board
    The chess board object to interpret the move in context.

    Returns:
    -------
    Tuple[str, str]
    A tuple representing the starting and ending positions of the move in the format (starting_square, ending_square).
    """
    board = FEN.split()[0] # ex: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR

    castling = True if 'O' in algebraic_notation else False
    if castling: # Castling
        return __castling_notation(algebraic_notation, FEN)    

    else: # Not castling
        piece_being_moved = algebraic_notation[0] if algebraic_notation[0] in {'K', 'Q', 'R', 'N', 'B'} else 'P'

        match piece_being_moved:
            case 'K':
                return king_algebraic_notation(algebraic_notation, FEN)
            case 'Q':
                return queen_algebraic_notation(algebraic_notation, FEN)
            case 'R':
                return rook_algebraic_notation(algebraic_notation, FEN)
            case 'N':
                return knight_algebraic_notation(algebraic_notation, FEN)
            case 'B':
                return bishop_algebraic_notation(algebraic_notation, FEN)
            case 'P':
                return pawn_algebraic_notation(algebraic_notation, FEN)

def __apply_move_to_FEN(move: str, fen: str) -> str:
    # Parse the FEN components
    board, turn = fen.split()[:2]
    
    # Initialize the board (8x8 grid)
    rows = board.split('/')
    board_matrix = []
    
    # Convert each row in FEN into a list of characters, replacing numbers with '1'
    for row in rows:
        board_row = []
        for char in row:
            if char.isdigit():  # If the character is a number, replace it with '1's
                board_row.extend(['1'] * int(char))
            else:
                board_row.append(char)
        board_matrix.append(board_row)
    
    # Extract the move components
    starting_square, ending_square, promotion_piece = move
    
    # Convert squares from algebraic notation to matrix indices
    start_row, start_col = 8 - int(starting_square[1]), ord(starting_square[0]) - ord('a')
    end_row, end_col = 8 - int(ending_square[1]), ord(ending_square[0]) - ord('a')
    
    # Get the piece being moved
    piece = board_matrix[start_row][start_col]
    
    # Check if this move is castling
    if piece.lower() == 'k' and abs(start_col - end_col) == 2:
        # Castling logic for the King (moving two squares)
        # Determine the rook's position
        if end_col > start_col:  # Kingside castling
            rook_col = 7
            new_rook_col = 5
        else:  # Queenside castling
            rook_col = 0
            new_rook_col = 3
        
        # Get the rook piece
        rook_piece = board_matrix[start_row][rook_col]
        
        # Move the king
        board_matrix[end_row][end_col] = 'k' if piece.islower() else 'K'
        board_matrix[start_row][start_col] = '1'  # Empty the starting square
        
        # Move the rook
        board_matrix[start_row][new_rook_col] = rook_piece
        board_matrix[start_row][rook_col] = '1'  # Empty the rook's original position
    else:
        # Regular move (non-castling)
        # Update the board matrix: move the piece
        board_matrix[end_row][end_col] = piece
        board_matrix[start_row][start_col] = '1'  # Empty the starting square
        
        # Handle promotion
        if promotion_piece:
            board_matrix[end_row][end_col] = promotion_piece.lower()  # Use lowercase for black pieces
    
    # Convert the board back into FEN format
    updated_board = []
    for row in board_matrix:
        # Join the row and collapse consecutive '1's into numbers
        row_str = ''.join(row)
        collapsed_row = re.sub(r'1+', lambda m: str(len(m.group(0))), row_str)
        updated_board.append(collapsed_row)
    
    # Join all rows with '/'
    updated_board_str = '/'.join(updated_board)
    
    # Rebuild the FEN string
    updated_fen = f"{updated_board_str} {' w' if turn == 'b' else ' b'}"
    
    return updated_fen

def process_move(move: str, FEN: str) -> Tuple[Tuple[str, str, str], str]:
    """
    Processes a single move in algebraic notation, converting it to coordinate notation and updating the FEN string.

    Parameters:
    ----------
    move : str
        The move in algebraic notation.
    FEN : str
        The current FEN string representing the board state.

    Returns:
    -------
    Tuple[Tuple[str, str, str], str]
        A tuple containing the move in coordinate notation and the updated FEN string.
        If the move is invalid, returns (None, FEN).
    """
    coordinates = convert_from_algebraic_notation(move, FEN)
    if coordinates is None:
        print("Invalid notation/ impossible move")
        return None, FEN
    FEN = __apply_move_to_FEN(coordinates, FEN)
    return coordinates, FEN

def convert_from_PGN(PGN: list[str], FEN: str = DEFAULT_FEN) -> list[Tuple[str, str]]:
    """
    Converts a list of moves in PGN (Portable Game Notation) format to a list of tuples representing the starting and ending squares.
    Use this for entire game.

    Parameters:
    ----------
    PGN : list[str]
        A list of moves in PGN format, e.g., ['e4', 'Nf3', 'O-O', etc.].
    board : Board
        The chess board object to interpret the moves in context.

    Returns:
    -------
    list[Tuple[str, str]]
        A list of tuples, each representing the starting and ending positions of the moves in the format (starting_square, ending_square).
    """

    # I will find the start of the game by reversing the PGN string, using find() to find the first instance of ']' and then that is the start.
    # However this will give the index of the reverse string, I can get the actual index with len(FEN) - index_of_reverse.
    start_index = len(PGN) - PGN[::-1].find(']')

    movetext = PGN[start_index:].split()

    # this removes the 1. and other nonmoves NOTE all lowercase so do .lower
    allowed_start_of_moves = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'o', 'k', 'n', 'q', 'r'}

    filtered_movetext = []
    in_alternate_line = False
    for string in movetext:
        if string[0] == '(':
            in_alternate_line = True
        elif string[-1] == ')': # removes the end of the (    ) for other lines looked at in pgn
            in_alternate_line = False
        elif string[0].lower() in allowed_start_of_moves and not in_alternate_line:
            filtered_movetext.append(string)

    game_in_coordinate_notation = []
    print(filtered_movetext)
    for move in filtered_movetext:
        coordinates, FEN = process_move(move, FEN)
        if coordinates == None:
            break
        game_in_coordinate_notation.append(coordinates)

    return game_in_coordinate_notation
