import unittest
from engine import material
class Tests(unittest.TestCase):
 def test_empty(self): self.assertEqual(material('8/8/8/8/8/8/8/8 w - - 0 1'),0)
 def test_queen(self): self.assertEqual(material('8/8/8/8/8/8/8/Q7 w - - 0 1'),900)
 def test_bad(self):
  with self.assertRaises(ValueError): material('8/8')
