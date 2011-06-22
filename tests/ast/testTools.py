import unittest

from lyanna.ast import tools

class TestItemStream(unittest.TestCase):
    def setUp(self):
        self.s = tools.ItemStream()
    def testPutAndAccess(self):
        items = ['one', 2, 'three']
        for it in items:
            self.s.put(it)
        for sit, it in zip(self.s, items):
            self.assertEqual(sit, it)
