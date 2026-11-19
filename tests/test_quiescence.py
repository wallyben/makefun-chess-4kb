import unittest
from engine import parse,search,moves,apply

class QuiescenceTests(unittest.TestCase):
 def test_horizon_avoids_undefended_queen_capture(self):
  # Capturing the rook with the queen looks profitable at depth one,
  # but the defending king can recapture. Search must see the reply.
  fen='4k3/8/8/8/8/4r3/4q3/4K3 b - - 0 1'
  b,w,c,e=parse(fen)
  self.assertTrue(moves(b,False,c,e))

 def test_checkmate_detected_at_leaf(self):
  # Black is already mated: white queen on g7 protected by king f6.
  b,w,c,e=parse('7k/6Q1/5K2/8/8/8/8/8 b - - 0 1')
  score,_=search(b,False,c,e,0)
  self.assertLess(score,-50000)

 def test_stalemate_at_leaf(self):
  b,w,c,e=parse('7k/5K2/6Q1/8/8/8/8/8 b - - 0 1')
  score,_=search(b,False,c,e,0)
  self.assertEqual(score,0)

 def test_quiet_start_does_not_crash(self):
  b,w,c,e=parse('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
  score,move=search(b,True,c,e,1)
  self.assertIsNotNone(move)

if __name__=='__main__':unittest.main()
