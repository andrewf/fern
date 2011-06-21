import unittest
import lyanna
from lyanna.parser.parser import Parser

class StartSymbol(unittest.TestCase):
    def setUp(self):
        self.p = Parser("foo= 42@'bar' = 'ggg'")
        self.fdg = self.p.parse()
    def testIsMap(self):
        self.assertTrue(isinstance(self.fdg, lyanna.tree.Map))
    def testKeys(self):
        self.assertEqual(self.fdg['foo'], 42)
        self.assertEqual(self.fdg['bar'], 'ggg')

class TestKVPair(unittest.TestCase):
    def testStringKey(self):
        p=Parser('foo=42')
        self.assertTrue(p.kvpair())
        result = p.result()
        self.assertTrue(isinstance(result, lyanna.tree.kvpair.KVPair))
        self.assertEqual(result.key, 'foo')
        self.assertEqual(result.value, 42)
    def testStringToString(self):
        p=Parser("foo='bar'")
        self.assertTrue(p.kvpair())
        result = p.result()
        self.assertEqual(result.key, 'foo')
        self.assertEqual(result.value, 'bar')
    def testAtKey(self):
        p=Parser("@'foo'=42")
        self.assertTrue(p.kvpair())
        result = p.result()
        self.assertEqual(result.key, 'foo')
        self.assertEqual(result.value, 42)
