"""Regression tests for the byte-limited HTTP competition entrypoint."""
import importlib.util
import os
import unittest
from unittest.mock import patch

with patch.dict(os.environ, {"MAKEFUN_ENV_URL": "http://127.0.0.1:9"}):
    spec = importlib.util.spec_from_file_location("tiny_entry", "main.py")
    entry = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(entry)


class EntrypointTests(unittest.TestCase):
    def test_board_start(self):
        b = entry.board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqual(len(b), 64)
        self.assertEqual((b[0], b[60], b[63]), ("r", "K", "R"))

    def test_castle_moves_rook(self):
        b = entry.board("4k3/8/8/8/8/8/8/R3K2R w KQ - 0 1")
        n = entry.move(b, "e1g1")
        self.assertEqual((n[entry.sq("g1")], n[entry.sq("f1")]), ("K", "R"))
        self.assertEqual(n[entry.sq("h1")], ".")

    def test_en_passant_removes_pawn(self):
        b = entry.board("4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1")
        n = entry.move(b, "e5d6")
        self.assertEqual(n[entry.sq("d6")], "P")
        self.assertEqual(n[entry.sq("d5")], ".")

    def test_promotion(self):
        b = entry.board("4k3/P7/8/8/8/8/8/4K3 w - - 0 1")
        self.assertEqual(entry.move(b, "a7a8q")[entry.sq("a8")], "Q")

    def test_king_attacks_do_not_slide(self):
        b = entry.board("8/8/8/8/8/8/8/4K3 w - - 0 1")
        self.assertEqual(len(entry.attacks(b, True)), 5)

    def test_byte_limit(self):
        self.assertLessEqual(os.path.getsize("main.py"), 4096)


if __name__ == "__main__":
    unittest.main()
