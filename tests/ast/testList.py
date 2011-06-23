import unittest
from fern.primitives import Undefined
from fern.ast.list import List
from fern.ast.tools import ItemStream

class TestList(unittest.TestCase):
    def setUp(self):
        self.li = List()
    def testPutAndAccess(self):
        self.li.put(42)
        self.li.put('umm')
        self.assertEqual(self.li[0], 42)
        self.assertEqual(self.li[1], 'umm')
    def testPutStream(self):
        s = ItemStream([4, False, List()])
        self.li.put(s)
        self.assertEqual(self.li.eval(), [4, False, []])
    def testPutUndefinedHasNoEffect(self):
        self.li.put('gob')
        self.li.put(Undefined)
        self.li.put(13)
        self.assertEqual(self.li.eval(), ['gob', 13])