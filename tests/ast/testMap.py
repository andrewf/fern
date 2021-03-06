import unittest

import fern
from fern.ast.node import Node
from fern.ast.map import Map, KVPair
from fern.ast.nameref import NameRef
from fern.ast.tools import ItemStream
from fern.ast.list import List

class TestMap(unittest.TestCase):
    def setUp(self):
        self.m = Map()
    def testOnePair(self):
        self.m.put(KVPair('key', 'value'))
        self.assertEqual(self.m['key'], 'value')
    def testTwoPairs(self):
        self.m.put(KVPair(13, 'value'))
        self.m.put(KVPair('key', 42))
        self.assertEqual(self.m[13], 'value')
        self.assertEqual(self.m['key'], 42)
    def testAssign(self):
        self.m['key'] = 34
        self.assertEqual(self.m['key'], 34)
    def testLaterKeySupersedes(self):
        self.m.put(KVPair('key', 4))
        self.m['key'] = 45
        self.m.put(KVPair('key', 13))
        self.assertEqual(self.m['key'], 13)
    def testMissingKeyisUndefined(self):
        self.assertEqual(self.m['I do not exist'], fern.primitives.Undefined)
    def testUndefinedValueDeletesKey(self):
        self.m['foo'] = 17
        self.m['foo'] = fern.primitives.Undefined
        self.failIf('foo' in self.m)
    def testSetKeyDoesNotAddChildren(self):
        # we need to have a nice interface for changing keys by
        # mutating KVPairs
        self.m.put(KVPair('foo', 42))
        self.m.put(KVPair('bar', 17))
        self.m.put(KVPair('ggg', 'umm'))
        self.assertEqual(self.m['bar'], 17)
        self.assertEqual(len(self.m.children), 3)
        # now the good part
        self.m.set_key('bar', 13)
        self.assertEqual(self.m['bar'], 13)
        self.assertEqual(len(self.m.children), 3)
        
class ItemStreamCompatibility(unittest.TestCase):
    def setUp(self):
        self.stream = ItemStream([
            KVPair(42, 'foo'),
            KVPair('foo', 17),
            KVPair('umm', List()),
        ])
        self.m = Map()
    def testPut(self):
        self.m.put(self.stream)
        self.assertEqual(self.m[42], 'foo')
        self.assertEqual(self.m['foo'], 17)
        self.assertEqual(self.m['umm'], [])
    def testBadPut(self):
        self.stream.append(14) # non kvpair is an error
        self.assertRaises(fern.errors.TypeError, self.m.put, self.stream)
    def testReparentInStream(self):
        self.m['var'] = 17
        self.stream.put(KVPair('ref', NameRef('var')))
        self.m.put(self.stream)
        self.assertEqual(self.m['ref'], 17)