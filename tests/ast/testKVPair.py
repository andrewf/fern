import unittest
from lyanna.ast.kvpair import KVPair

class TestKVPair(unittest.TestCase):
    "Not much to see, it's basically just a pair"
    def setUp(self):
        self.k = KVPair('key', 'value')
    def testKey(self):
        self.assertEqual(self.k.key, 'key')
    def testValue(self):
        self.assertEqual(self.k.value, 'value')
        