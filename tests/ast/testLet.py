import unittest
from fern.ast.let import Let
from fern.ast.map import Map
from fern.ast.list import List
from fern.ast.kvpair import KVPair
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

class TestLetKVPairs(unittest.TestCase):
    def testKVPairs(self):
        self.let = Let()
        self.let.names['var'] = 3
        x = Map()
        x['bar'] = NameRef('var')
        self.let.put(KVPair('a', x))
        x = List()
        x.put(NameRef('var'))
        self.let.put(KVPair('b', x))
        root = Map()
        root.put(self.let)
        self.assertEqual(root.eval(), {'a':{'bar':3}, 'b':[3]})
