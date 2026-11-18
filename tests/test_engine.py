import unittest
from engine import START,parse,material,moves,apply,sq,nm,search
class EngineTests(unittest.TestCase):
 def test_start_material(self):self.assertEqual(material(START),0)
 def test_start_moves(self):
  b,w,c,e=parse(START)
  self.assertEqual(len(moves(b,True,c,e)),20)
 def test_bad_fen(self):
  with self.assertRaises(ValueError):material('8/8')
 def test_queen(self):self.assertEqual(material('8/8/8/8/8/8/8/Q7 w - - 0 1'),900)
 def test_square_roundtrip(self):
  for i in range(64):self.assertEqual(sq(nm(i)),i)
 def test_check_evasion(self):
  b,w,c,e=parse('4r2k/8/8/8/8/8/8/4K3 w - - 0 1')
  self.assertNotIn('e1e2',[nm(i)+nm(j) for i,j,_ in moves(b,True,c,e)])
 def test_castling(self):
  b,w,c,e=parse('r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1')
  u=[nm(i)+nm(j) for i,j,_ in moves(b,True,c,e)]
  self.assertIn('e1g1',u);self.assertIn('e1c1',u)
 def test_en_passant(self):
  b,w,c,e=parse('4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1')
  m=next(m for m in moves(b,True,c,e) if nm(m[0])+nm(m[1])=='e5d6')
  n=apply(b,m,e);self.assertEqual(n[sq('d5')],'.');self.assertEqual(n[sq('d6')],'P')
 def test_promotion(self):
  b,w,c,e=parse('4k3/P7/8/8/8/8/8/4K3 w - - 0 1')
  self.assertEqual(len([m for m in moves(b,True,c,e) if nm(m[0])+nm(m[1])=='a7a8']),4)
 def test_castling_rights_after_rook_capture(self):
  b,w,c,e=parse('r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1')
  # The search must not invent a rook when a castling rook has been captured.
  _,m=search(b,True,c,e,2)
  self.assertIn(m,moves(b,True,c,e))
 def test_en_passant_only_on_immediate_reply(self):
  b,w,c,e=parse('4k3/8/8/3p4/8/8/4P3/4K3 w - - 0 1')
  m=next(m for m in moves(b,True,c,e) if nm(m[0])+nm(m[1])=='e2e4')
  n=apply(b,m,e)
  self.assertIn('d5e4',[nm(i)+nm(j) for i,j,_ in moves(n,False,'-',nm((m[0]+m[1])//2))])
  self.assertNotIn('d5e4',[nm(i)+nm(j) for i,j,_ in moves(n,False,'-','-')])
 def test_search_legal(self):
  b,w,c,e=parse(START);_,m=search(b,True,c,e,2)
  self.assertIn(m,moves(b,True,c,e))
if __name__=='__main__':unittest.main()
