import unittest
from lyanna.tree import Node

class TestNode(unittest.TestCase):
    def setUp(self):
        self.n = Node()
    def testReparent(self):
        other = Node()
        self.n.reparent(other)
        self.failUnless(other.parent is self.n)
