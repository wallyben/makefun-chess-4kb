"""Deterministic move-generation benchmark positions (standard chess perft)."""
import unittest
from engine import parse,moves,apply,START,nm

def child_state(b,w,c,e,m):
 i,j,_=m
 piece=b[i]
 next_castle=c
 if piece.lower()=='k':
  next_castle=next_castle.replace('K' if w else 'k','').replace('Q' if w else 'q','')
 for square,right in ((63,'K'),(56,'Q'),(7,'k'),(0,'q')):
  if i==square or j==square:next_castle=next_castle.replace(right,'')
 next_ep=nm((i+j)//2) if piece.lower()=='p' and abs(i-j)==16 else '-'
 return apply(b,m,e),not w,next_castle,next_ep

def perft(b,w,c,e,depth):
 if depth==0:return 1
 return sum(perft(*child_state(b,w,c,e,m),depth-1) for m in moves(b,w,c,e))

class PerftTests(unittest.TestCase):
 def test_initial_position_depth_two(self):
  self.assertEqual(perft(*parse(START)[:1],True,'KQkq','-',2),400)
 def test_initial_position_depth_three(self):
  b,side,c,e=parse(START)
  self.assertEqual(perft(b,side=='w',c,e,3),8902)
 def test_kiwipete_depth_one(self):
  fen='r3k2r/p1ppqpb1/bn2pnp1/2pP4/1p2P3/2N2N2/PPQBBPPP/R3K2R w KQkq - 0 1'
  b,side,c,e=parse(fen)
  self.assertGreater(len(moves(b,side=='w',c,e)),35)

if __name__=='__main__':unittest.main()
