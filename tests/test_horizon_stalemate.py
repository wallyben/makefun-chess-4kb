import unittest
from engine import parse,search,moves

class HorizonStalemate(unittest.TestCase):
 def test_stalemate_at_quiescence_cutoff(self):
  # Black has no legal move, is not in check, and White has a queen.
  b,w,c,e=parse('7k/5Q2/6K1/8/8/8/8/8 b - - 0 1')
  self.assertEqual(moves(b,False,c,e),[])
  for q in (0,4,6):
   self.assertEqual(search(b,False,c,e,0,q=q)[0],0)

if __name__=='__main__':unittest.main()
