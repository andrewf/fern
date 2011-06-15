import unittest

import lyanna.tree

class TestKVPair(unittest.TestCase):
    def setUp(self):
        self.k = lyanna.tree.KVPair('key', 'value')
    def testIsNode(self):
        self.failUnless(isinstance(self.k, lyanna.tree.Node))
    def testKey(self):
        self.assertEqual(self.k.key, 'key')
    def testValue(self):
        self.assertEqual(self.k.value, 'value')
    