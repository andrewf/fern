import unittest
from fern.ast.let import Let
from fern.ast.map import Map
from fern.ast.list import List
from fern.ast.nameref import NameRef

class TestLetItem(unittest.TestCase):
    def setUp(self):
        self.m = Map()
        self.m['ref'] = NameRef('var')
        self.let = Let()
        self.let.put(self.m)
        self.let.names['var'] = 42
    def testMap(self):
        self.let.names['var'] = 42
        self.assertEqual(self.let.eval(), {'ref': 42})
    def testStream(self):
        self.let.names['var'] = True
        self.let.put(NameRef('var'))
        l = List()
        l.put(42)
        l.put(self.let)
        l.put('arg')
        self.assertEqual(l.eval(), [42, {'ref': True}, True, 'arg'])
