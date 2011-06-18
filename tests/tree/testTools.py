import unittest

from lyanna.tree import tools

class TestItemStream(unittest.TestCase):
    def setUp(self):
        self.s = tools.ItemStream()
    def testPutAndAccess(self):
        items = ['one', 2, 'three']
        for it in items:
            self.s.put(it)
        for sit, it in zip(self.s, items):
            self.assertEqual(sit, it)

class TestKVPair(unittest.TestCase):
    "Not much to see, it's basically just a pair"
    def setUp(self):
        self.k = tools.KVPair('key', 'value')
    def testKey(self):
        self.assertEqual(self.k.key, 'key')
    def testValue(self):
        self.assertEqual(self.k.value, 'value')
