import unittest

import lyanna
from lyanna.tree.node import Node
from lyanna.tree.map import Map, KVPair

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
        self.assertEqual(self.m['I do not exist'], lyanna.primitives.Undefined)
    def testUndefinedValueDeletesKey(self):
        self.m['foo'] = 17
        self.m['foo'] = lyanna.primitives.Undefined
        self.failIf('foo' in self.m)
    def testGetKeyVsGetItem(self):
        # set up a child map
        self.m['key'] = Map()
        self.assertTrue(isinstance(self.m['key'], lyanna.simple.Map))
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
        

