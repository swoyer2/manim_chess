import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from board import Board

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

if __name__ == '__main__':
	unittest.main()