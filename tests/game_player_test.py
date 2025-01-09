import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from manim_chess.game_player import *

class TestBoard(unittest.TestCase):
	def test_king(self):
		expected_coordinates = ('e1', 'e2', '')
		actual_coordinates = king_algebraic_notation('ke2','rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_king_capture(self):
		expected_coordinates = ('f4', 'f5', '')
		actual_coordinates = king_algebraic_notation('kxf5','8/5k2/8/5r2/5K2/8/8/8 w - - 0 1')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_king_disovered_check(self):
		expected_coordinates = ('f4', 'e4', '')
		actual_coordinates = king_algebraic_notation('ke4+','8/5k2/8/r7/5K2/8/8/5R2 w - - 0 1')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_king_disovered_checkmate(self):
		expected_coordinates = ('h6', 'g6', '')
		actual_coordinates = king_algebraic_notation('kg6#','7k/r4P2/7K/8/8/8/8/6RR w - - 12 7')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_pawn(self):
		expected_coordinates = ('e2', 'e4', '')
		actual_coordinates = pawn_algebraic_notation('e4','rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_pawn_capture(self):
		expected_coordinates = ('e4', 'd5', '')
		actual_coordinates = pawn_algebraic_notation('exd5','rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 2')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_pawn_check(self):
		expected_coordinates = ('d6', 'd7', '')
		actual_coordinates = pawn_algebraic_notation('d7+','rnbqkbnr/ppp2ppp/3P4/4p3/8/8/PPPP1PPP/RNBQKBNR w KQkq - 0 4')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_pawn_promote(self):
		expected_coordinates = ('d7', 'd8', 'R')
		actual_coordinates = pawn_algebraic_notation('d8=R','rnb2bnr/pppP1ppp/4k3/4p1q1/8/3P1P2/PPP3PP/RNBQKBNR w KQ - 1 7')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_pawn_promote_check(self):
		expected_coordinates = ('d7', 'd8', 'N')
		actual_coordinates = pawn_algebraic_notation('d8=N','rnb2bnr/pppP1ppp/4k3/4p1q1/8/3P1P2/PPP3PP/RNBQKBNR w KQ - 1 7')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_pawn_capture_promote(self):
		expected_coordinates = ('d7', 'c8', 'Q')
		actual_coordinates = pawn_algebraic_notation('dxc8=Q','rnbq1bnr/pppPkppp/8/4p3/8/8/PPPP1PPP/RNBQKBNR w KQ - 1 5')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_pawn_capture_check(self):
		expected_coordinates = ('d6', 'e7', '')
		actual_coordinates = pawn_algebraic_notation('dxe7+','rnbq1knr/ppp1bppp/3Pp3/8/8/5P2/PPPP2PP/RNBQKBNR w KQ - 1 5')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_pawn_promote_checkmate(self):
		expected_coordinates = ('d7', 'd8', 'Q')
		actual_coordinates = pawn_algebraic_notation('d8=Q#','rnb2bnr/1ppPkpp1/7p/3QpP2/4N3/p1KP4/PPP3PP/RN3B1R w - - 0 20')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_knight(self):
		expected_coordinates = ('g1', 'f3', '')
		actual_coordinates = knight_algebraic_notation('nf3','rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_knight_check(self):
		expected_coordinates = ('f5', 'g7', '')
		actual_coordinates = knight_algebraic_notation('ng7+','rnbqkbnr/pppp1p1p/6p1/4pN2/8/8/PPPPPPPP/RNBQKB1R w KQkq - 0 4')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_knight_capture(self):
		expected_coordinates = ('f3', 'e5', '')
		actual_coordinates = knight_algebraic_notation('nxe5','rnbqkbnr/pppp1ppp/8/4p3/8/5N2/PPPPPPPP/RNBQKB1R w KQkq e6 0 2')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_knight_capture_check(self):
		expected_coordinates = ('f5', 'g7', '')
		actual_coordinates = knight_algebraic_notation('nxg7+','rnbqkbnr/ppp2ppp/3p4/4pN2/8/8/PPPPPPPP/RNBQKB1R w KQkq - 0 4')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_knight_ambiguity_file(self):
		expected_coordinates = ('g4', 'e5', '')
		actual_coordinates = knight_algebraic_notation('nge5','rnbq1bnr/pp2kppp/2p5/3p4/4p1N1/5N2/PPPPPPPP/R1BQKB1R w KQ - 0 6')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_knight_ambiguity_rank_capture(self):
		expected_coordinates = ('g4', 'e5', '')
		actual_coordinates = knight_algebraic_notation('ngxe5','rnbq1bnr/p3kppp/1pp5/3pp3/6N1/5N2/PPPPPPPP/R1BQKB1R w KQ - 0 6')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_knight_ambiguity_file(self):
		expected_coordinates = ('g6', 'e5', '')
		actual_coordinates = knight_algebraic_notation('n6e5','rnbq1bnr/5ppp/1pp1k1N1/p2p4/6N1/8/PPPPPPPP/R1BQKB1R w KQ a6 0 8')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_knight_ambiguity_rank_and_file(self):
		expected_coordinates = ('d3', 'e5', '')
		actual_coordinates = knight_algebraic_notation('nd3e5','1nbqkbnr/3N1ppp/r5N1/pppp4/8/3N1N2/PPPPPPPP/R1BQKB1R w KQ - 0 14')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_bishop(self):
		expected_coordinates = ('f1', 'c4', '')
		actual_coordinates = bishop_algebraic_notation('bc4','rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_bishop_capture(self):
		expected_coordinates = ('f1', 'c4', '')
		actual_coordinates = bishop_algebraic_notation('bxc4','rnbqkbnr/pp1p1ppp/8/4p1N1/2p1P3/8/PPPP1PPP/RNBQKB1R w KQkq - 0 4')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_bishop_check(self):
		expected_coordinates = ('f1', 'b5', '')
		actual_coordinates = bishop_algebraic_notation('bb5+','rnbqkbnr/ppp2ppp/8/3pp3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq d6 0 3')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_bishop_capture_check(self):
		expected_coordinates = ('f1', 'b5', '')
		actual_coordinates = bishop_algebraic_notation('bxb5+','rnbqkbnr/p1p2ppp/8/1p1pp1N1/4P3/8/PPPP1PPP/RNBQKB1R w KQkq b6 0 4')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_bishop_capture_check_abiguity(self):
		expected_coordinates = ('f1', 'b5', '')
		actual_coordinates = bishop_algebraic_notation('bfxb5+','rnbqkbnr/p1p2ppp/B7/1p1pp1N1/4P3/8/PPPP1PPP/RNBQKB1R w KQkq b6 0 4')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_rook(self):
		expected_coordinates = ('h1', 'h3', '')
		actual_coordinates = rook_algebraic_notation('rh3','rnbqkbnr/ppppppp1/8/7p/7P/8/PPPPPPP1/RNBQKBNR w KQkq h6 0 2')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_rook_capture(self):
		expected_coordinates = ('e3', 'e5', '')
		actual_coordinates = rook_algebraic_notation('rxe5','rnbqk1nr/ppppbpp1/8/4p2p/7P/4R3/PPPPPPP1/RNBQKBN1 w Qkq - 2 4')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_rook_check(self):
		expected_coordinates = ('f5', 'e5', '')
		actual_coordinates = rook_algebraic_notation('re5+','rnbqkbnr/pppp1pp1/8/5R1p/7P/4p3/PPPPPPP1/RNBQKBN1 w Qkq - 0 5')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_rook_capture_check(self):
		expected_coordinates = ('e3', 'e4', '')
		actual_coordinates = rook_algebraic_notation('rxe4+','rnbqkbnr/pppp1pp1/8/7p/4p2P/4R3/PPPPPPP1/RNBQKBN1 w Qkq - 0 4')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_rook_ambiguity_file(self):
		expected_coordinates = ('a3', 'e3', '')
		actual_coordinates = rook_algebraic_notation('rae3','rnbqkbn1/pppp1pp1/7r/7p/P3p2P/R6R/1PPPPPP1/1NBQKBN1 w q - 0 5')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_rook_ambiguity_file_capture(self):
		expected_coordinates = ('g4', 'e4', '')
		actual_coordinates = rook_algebraic_notation('rgxe4','rnbqk1n1/1pppbpp1/7r/p6p/P3p1RP/4R3/1PPPPPP1/1NBQKBN1 w q - 0 8')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_rook_ambiguity_file_capture_check(self):
		expected_coordinates = ('g4', 'e4', '')
		actual_coordinates = rook_algebraic_notation('rgxe4+','rnbqk1n1/1ppp1pp1/p6r/6bp/P3p1RP/4R3/1PPPPPP1/1NBQKBN1 w q - 2 8')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_queen(self):
		expected_coordinates = ('d1', 'g4', '')
		actual_coordinates = queen_algebraic_notation('qg4','rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_queen_ambiguity(self):
		expected_coordinates = ('g4', 'g6', '')
		actual_coordinates = queen_algebraic_notation('qgg6','rnbqkbnr/ppppppp1/8/8/4Q1Q1/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_pawn_black(self):
		expected_coordinates = ('h7', 'h5', '')
		actual_coordinates = pawn_algebraic_notation('h5','rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_king_black(self):
		expected_coordinates = ('e8', 'e7', '')
		actual_coordinates = king_algebraic_notation('ke7','rnbqkbnr/pppp1pp1/4p3/7p/4PPP1/8/PPPP3P/RNBQKBNR b KQkq g3 0 3')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_knight_black(self):
		expected_coordinates = ('g8', 'f6', '')
		actual_coordinates = knight_algebraic_notation('nf6','rnbq1bnr/ppppkpp1/4p3/7p/3PPPP1/8/PPP4P/RNBQKBNR b KQ d3 0 4')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_bishop_black(self):
		expected_coordinates = ('f8', 'h6', '')
		actual_coordinates = bishop_algebraic_notation('bh6','rnbq1b1r/ppppkp2/4pn2/6pp/1PPPPPP1/8/P6P/RNBQKBNR b KQ b3 0 6')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_rook_black(self):
		expected_coordinates = ('h8', 'g8', '')
		actual_coordinates = rook_algebraic_notation('rg8','rnbq3r/ppppkp2/4pn1b/6pp/1PPPPPP1/5N2/P6P/RNBQKB1R b KQ - 2 7')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_queen_black(self):
		expected_coordinates = ('d8', 'f8', '')
		actual_coordinates = queen_algebraic_notation('Qf8','rnbq2r1/ppppkp2/4pn1b/6pp/1PPPPPP1/5N2/P3K2P/RNBQ1B1R b - - 4 8')
		self.assertEqual(expected_coordinates, actual_coordinates)

	def test_convert_from_PGN(self):
		expected_output = [('e2', 'e4', ''), ('e7', 'e5', ''), ('g1', 'f3', ''), ('d8', 'f6', '')]

		# This looks ugly but I am just copy pasting from chess.com, I figure that is what most people would do
		actual_output = convert_from_PGN("""[Event "?"]
[Site "?"]
[Date "????.??.??"]
[Round "?"]
[White "?"]
[Black "?"]
[Result "*"]
[Link "https://www.chess.com/analysis?tab=analysis"]

1. e4 e5 2. Nf3 Qf6 *""")
		self.assertEqual(expected_output, actual_output)

	def test_convert_from_PGN_side_lines(self):
		expected_output = [('e2', 'e4', ''), ('e7', 'e5', ''), ('g1', 'f3', ''), ('d8', 'f6', ''), ('d2', 'd4', ''), ('d7', 'd5', '')]

		# This looks ugly but I am just copy pasting from chess.com, I figure that is what most people would do
		actual_output = convert_from_PGN("""[Event "?"]
[Site "?"]
[Date "????.??.??"]
[Round "?"]
[White "?"]
[Black "?"]
[Result "*"]
[Link "https://www.chess.com/analysis?tab=analysis"]

1. e4 e5 2. Nf3 Qf6 3. d4 (3. Bc4 d5 4. Bxd5) 3... d5 *""")
		self.assertEqual(expected_output, actual_output)


if __name__ == '__main__':
	unittest.main()