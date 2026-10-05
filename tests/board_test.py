import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from manim_chess.board import Board

class TestBoard(unittest.TestCase):
	def test_reading_fen(self):
		test_board = Board()
		expected_FEN = 'rnbqkbnr/ppp1pppp/8/8/2PpP3/5P2/PP1P2PP/RNBQKBNR'
		actual_FEN = test_board.get_piece_info_from_FEN('rnbqkbnr/ppp1pppp/8/8/2PpP3/5P2/PP1P2PP/RNBQKBNR b KQkq c3 0 3')
		self.assertEqual(expected_FEN, actual_FEN)

	def test_get_coordinate_from_index_a8(self):
		test_board = Board()
		expected_coordinate = 'a8'
		actual_coordinate = test_board.get_coordinate_from_index(0)
		self.assertEqual(expected_coordinate, actual_coordinate)

	def test_get_coordinate_from_index_e4(self):
		test_board = Board()
		expected_coordinate = 'e4'
		actual_coordinate = test_board.get_coordinate_from_index(36)
		self.assertEqual(expected_coordinate, actual_coordinate)

class TestBoardLabels(unittest.TestCase):
	def labels(self, board, coordinate):
		return [(round(float(label.get_x()), 4), round(float(label.get_y()), 4), label[0].get_fill_color().to_hex())
				for label in board.squares[coordinate].submobjects]

	def play_moves(self, board):
		board.move_piece('g1', 'f3')  # highlights g1, which has a file label
		board.move_piece('g8', 'f6')  # unmarks g1
		board.move_piece('a2', 'a4')  # highlights a2 and a4, which have rank labels
		board.move_piece('b8', 'c6')  # unmarks a2 and a4

	def assert_labels_unchanged_by_moves(self, scale):
		test_board = Board()
		test_board.set_board_from_FEN()
		test_board.scale(scale)
		coordinates = ['a1', 'a2', 'a4', 'g1']
		expected_labels = {coordinate: self.labels(test_board, coordinate) for coordinate in coordinates}
		self.play_moves(test_board)
		actual_labels = {coordinate: self.labels(test_board, coordinate) for coordinate in coordinates}
		self.assertEqual(expected_labels, actual_labels)

	def test_labels_unchanged_by_moves(self):
		self.assert_labels_unchanged_by_moves(1)

	def test_labels_unchanged_by_moves_on_shrunk_board(self):
		self.assert_labels_unchanged_by_moves(0.75)

	def test_labels_unchanged_by_moves_on_enlarged_board(self):
		self.assert_labels_unchanged_by_moves(1.5)

	def test_label_stays_while_square_is_marked(self):
		test_board = Board()
		expected_labels = self.labels(test_board, 'a1')
		test_board.mark_square('a1')
		self.assertEqual(expected_labels, self.labels(test_board, 'a1'))

	def test_square_colors(self):
		test_board = Board()
		test_board.highlight_square('g1')
		self.assertEqual(test_board.color_highlight_dark, test_board.squares['g1'].get_fill_color())
		test_board.highlight_square('h1')
		self.assertEqual(test_board.color_highlight_light, test_board.squares['h1'].get_fill_color())
		test_board.mark_square('a1')
		self.assertEqual('#EC7D6A', test_board.squares['a1'].get_fill_color().to_hex())
		test_board.unmark_square('g1')
		self.assertEqual(test_board.color_dark, test_board.squares['g1'].get_fill_color())
		test_board.unmark_square('h1')
		self.assertEqual(test_board.color_light, test_board.squares['h1'].get_fill_color())

if __name__ == '__main__':
	unittest.main()