"""Regression: quiescence must not invent mate when check extension reaches its cap."""
import unittest
from engine import parse, search, moves, king, attacked

class CheckExtensionTests(unittest.TestCase):
    def test_check_at_extension_cap_is_not_mate(self):
        board, side, castle, ep = parse("4r2k/8/8/8/8/8/8/4K3 w - - 0 1")
        self.assertTrue(attacked(board, king(board, True), False))
        self.assertTrue(moves(board, True, castle, ep))
        score, _ = search(board, True, castle, ep, 0, q=6)
        self.assertGreater(score, -90000)

    def test_actual_checkmate_still_scores_as_mate(self):
        board, side, castle, ep = parse("7k/6Q1/5K2/8/8/8/8/8 b - - 0 1")
        self.assertFalse(moves(board, False, castle, ep))
        score, _ = search(board, False, castle, ep, 0, q=6)
        self.assertLess(score, -90000)

if __name__ == "__main__":
    unittest.main()
