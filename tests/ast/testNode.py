import unittest
from fern.ast import Node
from fern.ast import NameRef

class MyNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.children = []
    def refresh_impl(self):
        self.value = 'ahh!'
    def put(self, it):
        self.reparent(it)
        self.children.append(it)
    def get_children(self):
        return self.children

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
    def testVisit(self):
        self.counter = 0 # must be on self for visitor to close on it
        def visitor(n):
            self.counter += 1
        n2 = MyNode()
        n2.put(MyNode())
        n2.put(MyNode())
        self.n.put(n2)
        self.n.put(MyNode())
        # there are now 5 nodes
        self.n.visit(visitor)
        self.assertEqual(self.counter, 5)
