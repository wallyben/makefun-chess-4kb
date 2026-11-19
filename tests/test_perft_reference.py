"""Independent perft smoke tests for legal move generation.

Run: python -m unittest discover -s tests -v
These tests exercise move state, not search evaluation.
"""
import unittest
from engine import START, parse, moves, apply, nm

def perft(board, white, rights, ep, depth):
    if depth == 0:
        return 1
    total = 0
    for move in moves(board, white, rights, ep):
        i, j, _ = move
        piece = board[i]
        next_rights = rights
        if piece.lower() == 'k':
            next_rights = next_rights.replace('K' if white else 'k', '').replace('Q' if white else 'q', '')
        for square, flag in ((63, 'K'), (56, 'Q'), (7, 'k'), (0, 'q')):
            if i == square or j == square:
                next_rights = next_rights.replace(flag, '')
        next_ep = nm((i + j) // 2) if piece.lower() == 'p' and abs(i - j) == 16 else '-'
        total += perft(apply(board, move, ep), not white, next_rights, next_ep, depth - 1)
    return total

class PerftTests(unittest.TestCase):
    def test_start_depth_2(self):
        b, _, c, e = parse(START)
        self.assertEqual(perft(b, True, c, e, 2), 400)

    def test_start_depth_3(self):
        b, _, c, e = parse(START)
        self.assertEqual(perft(b, True, c, e, 3), 8902)

    def test_kings_and_rooks_castling_depth_1(self):
        b, _, c, e = parse('r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1')
        self.assertEqual(perft(b, True, c, e, 1), 26)

if __name__ == '__main__':
    unittest.main()
