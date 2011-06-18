import unittest
from lyanna.tree import Node

class MyNode(Node):
    def refresh_impl(self):
        self.value = 'ahh!'

class TestNode(unittest.TestCase):
    def setUp(self):
        self.n = MyNode()
    def testReparent(self):
        other = Node()
        self.n.reparent(other)
        self.failUnless(other.parent is self.n)
    def testInvalidateSetsModified(self):
        self.n.invalidate()
        self.assertTrue(self.n.modified)
    def testRefreshCallsRefreshImpl(self):
        self.n.refresh()
        self.assertEqual(self.n.value, 'ahh!')
    def testEval(self):
        self.n.invalidate()
        self.assertEqual(self.n.eval(), 'ahh!')