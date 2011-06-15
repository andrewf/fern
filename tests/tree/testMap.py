import unittest

from lyanna.tree import Node, Map, KVPair

class TestKVPair(unittest.TestCase):
    def setUp(self):
        self.k = KVPair('key', 'value')
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
        self.m.put(KVPair('key', 'value'))
        self.assertEqual(self.m['key'], 'value')
    def testTwoPairs(self):
        self.m.put(KVPair(13, 'value'))
        self.m.put(KVPair('key', 42))
        self.assertEqual(self.m[13], 'value')
        self.assertEqual(self.m['key'], 42)
