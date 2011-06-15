import unittest

import lyanna
from lyanna.tree import Node, Map, KVPair

class TestKVPair(unittest.TestCase):
    "Not much to see, it's basically just a pair"
    def setUp(self):
        self.k = KVPair(None, 'key', 'value')
    def testIsNode(self):
        self.failUnless(isinstance(self.k, Node))
    def testKey(self):
        self.assertEqual(self.k.key, 'key')
    def testValue(self):
        self.assertEqual(self.k.value, 'value')

class TestMap(unittest.TestCase):
    def setUp(self):
        self.m = Map(None)
    def testOnePair(self):
        self.m.put(KVPair(self.m, 'key', 'value'))
        self.assertEqual(self.m['key'], 'value')
    def testTwoPairs(self):
        self.m.put(KVPair(self.m, 13, 'value'))
        self.m.put(KVPair(self.m, 'key', 42))
        self.assertEqual(self.m[13], 'value')
        self.assertEqual(self.m['key'], 42)
    def testAssign(self):
        self.m['key'] = 34
        self.assertEqual(self.m['key'], 34)
    def testLaterKeySupersedes(self):
        self.m.put(KVPair(self.m, 'key', 4))
        self.m['key'] = 45
        self.m.put(KVPair(self.m, 'key', 13))
        self.assertEqual(self.m['key'], 13)

