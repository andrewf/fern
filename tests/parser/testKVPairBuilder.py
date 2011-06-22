import unittest
import fern
from fern.parser.builder import KVPairBuilder

class TestKVPairBuilder(unittest.TestCase):
    def setUp(self):
        self.b = KVPairBuilder()
    def testCorrectPath(self):
        # case where all goes according to plan
        self.b.put('key')
        self.b.put('value')
        pair = self.b.get()
        self.assertEqual(pair.key, 'key')
        self.assertEqual(pair.value, 'value')
    def testErrorOnNoObjects(self):
        self.assertRaises(fern.parser.errors.BuilderError, self.b.get)
    def testErrorOnOneObject(self):
        self.b.put('fff')
        self.assertRaises(fern.parser.errors.BuilderError, self.b.get)
    def testErrorOnThreeObjects(self):
        self.b.put('fff')
        self.b.put('ggg')
        self.assertRaises(fern.parser.errors.BuilderError, self.b.put, 'hhh')