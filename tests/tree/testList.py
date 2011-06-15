import unittest
import lyanna.tree.list

class TestList(unittest.TestCase):
    def setUp(self):
        self.li = lyanna.tree.list.List(None)
    def testPutAndAccess(self):
        self.li.put(42)
        self.li.put('umm')
        self.assertEqual(self.li[0], 42)
        self.assertEqual(self.li[1], 'umm')