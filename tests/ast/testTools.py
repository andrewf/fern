import unittest

from fern.ast import tools
from fern.primitives import Undefined, Nothing

class TestItemStream(unittest.TestCase):
    def setUp(self):
        self.data = [1, 4, 'fooz', Nothing]
        self.s = tools.ItemStream(self.data)
    def testEquality(self):
        self.assertEqual(self.s, self.data)
    def testAppend(self):
        self.s.append(True)
        self.data.append(True)
        self.assertEqual(self.s, self.data)
