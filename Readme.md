# Manim Chess

This is a [Manim Community](https://www.manim.community/) plugin that allows you to generate a chess board/chess game easily.


## Installation

```bash
pip install manim-chess
```

## Features

- **Create Chessboard**: Allows you to create and display a chessboard.
- **Move Pieces**: Animate piece movement with PGN notation or the simplified notation in the package.
- **Special Moves**: Handle special chess moves like castling and en passant.
- **Load FEN Strings**: Load and display a board configuration from a FEN string.
- **Play PGN Files**: Load and animate moves from PGN files.
- **Evaluation Bar**: Allows the creation and ability to display an evaluation bar.
- **Update Evaluation Bar**: Can update the value in the evaluation bar with externally obtained evaulations.
- **Mark Squares**: Can mark and unmark squares to highlight them.
- **Draw Arrows**: Can draw/undraw arrows similar to chess.com

## Usage

In order to use this package you need to run the script using Manim. I have provided some examples on how to use it
below.


### Moving Pieces
This example initializes the chessboard and shows how you can move a piece.

![MovingPieces](https://github.com/codevardhan/manim-chess-plugin/blob/main/example/MovePieceExampleGif.gif?raw=true)


```python
import manim_chess

class MovingPieces(Scene):
    def construct(self):
        chess_board = manim_chess.board.Board()
        chess_board.set_board_from_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") # Also can set the default board with no arguments

        # Define the moves you want to be done with the default notation (starting_square, ending_square, promotion_piece)
        # Note that the promotion piece is blank unless a pawn is promoting
        moves = [('e2', 'e4', ''), ('e7', 'e5', ''), ('g1', 'f3', '')]

        self.add(chess_board)
        self.wait()
        manim_chess.game_player.play_game(scene=self, board=chess_board, moves=moves)
        self.wait()
```

### Using a PGN Notation
This example demonstrates playing moves from a PGN file on the chessboard. NOTE if you are starting from a different FEN than the standard start of a game, include FEN=your_fen_string

![PGNExample](https://github.com/codevardhan/manim-chess-plugin/blob/main/example/PlayPGNExample.gif?raw=true)


```python

class PGN_Example(MovingCameraScene):
    def construct(self):
        chess_board = manim_chess.board.Board()
        chess_board.set_board_from_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") # Also can set the default board with no arguments

        # You can paste a PGN straight from wherever you got your pgn. Just make it a multiline string with """PGN"""
        moves = manim_chess.game_player.convert_from_PGN("""[Event "It (cat.17)"]
[Site "Wijk aan Zee (Netherlands)"]
[Date "1999.??.??"]
[Round "4"]
[White "Kasparov Garry (RUS)"]
[Black "Topalov Veselin (BUL)"]
[Result "1-0"]
[ECO "B07"]
[WhiteElo "2851"]
[BlackElo "2690"]
[Annotator ""]
[Source ""]
[Remark "I"]
[WhiteUrl "https://images.chesscomfiles.com/uploads/v1/master_player/4fe1281a-a9df-11e8-8450-4ff4fd58ed06.bb91bfe2.50x50o.77b8f8a95e5e.jpeg"]
[WhiteCountry ""]
[WhiteTitle ""]
[BlackUrl "https://images.chesscomfiles.com/uploads/v1/master_player/e9640f50-c002-11e8-b93d-e56e1835faa8.4a751865.50x50o.dd0ca3584c8b.png"]
[BlackCountry ""]
[BlackTitle ""]
[Link "https://www.chess.com/analysis/game/master/969971?tab=analysis"]

1. e4 d6 2. d4 Nf6 3. Nc3 g6 4. Be3 Bg7 5. Qd2 c6 6. f3 b5 7. Nge2 Nbd7 8. Bh6
Bxh6 9. Qxh6 Bb7 10. a3 e5 11. O-O-O Qe7 12. Kb1 a6 13. Nc1 $6 O-O-O $2 14. Nb3 $6
exd4 15. Rxd4 c5 16. Rd1 Nb6 17. g3 $6 Kb8 $6 18. Na5 $6 Ba8 19. Bh3 d5 20. Qf4+
Ka7 21. Rhe1 d4 $1 22. Nd5 Nbxd5 23. exd5 Qd6 24. Rxd4 $1 cxd4 $2 25. Re7+ $3 Kb6 26.
Qxd4+ Kxa5 27. b4+ $1 Ka4 28. Qc3 $1 Qxd5 29. Ra7 $1 Bb7 30. Rxb7 Qc4 31. Qxf6 Kxa3 $2
32. Qxa6+ $1 Kxb4 33. c3+ $1 Kxc3 34. Qa1+ $1 Kd2 35. Qb2+ $1 Kd1 36. Bf1 $3 Rd2 37.
Rd7 $3 Rxd7 38. Bxc4 bxc4 39. Qxh8 Rd3 40. Qa8 c3 41. Qa4+ Ke1 42. f4 f5 43. Kc1
Rd2 44. Qa7 1-0""")

        self.add(chess_board)
        self.wait()
        manim_chess.game_player.play_game(scene=self, board=chess_board, moves=moves)
        self.wait()
```

### Evaluation Bar
This example shows how to add and adjust the values of the evaluation bar

![PGNExample](https://github.com/codevardhan/manim-chess-plugin/blob/main/example/PlayPGNExample.gif?raw=true)


```python

class EvalBarExample(MovingCameraScene):
    def construct(self):
        chess_board = manim_chess.board.Board()
        chess_board.set_board_from_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") # Also can set the default board with no arguments

        eval_bar = mc.evaluation_bar.EvaluationBar()
		eval_bar.move_to(chess_board.get_left()).shift(LEFT*0.5)

        self.add(chess_board, eval_bar)
        self.wait()
```

### Running the Examples
To run any of the examples, execute the script using Manim. For instance, here is an example on how to render the first example with low quality (if you want high quality replace -pql with -hql)

```sh
manim -pql examples.py MovingPieces
```

Replace `MovingPieces` with the class name of the example you want to run.

### License
This project is licensed under the MIT License. See the LICENSE file for more details.
