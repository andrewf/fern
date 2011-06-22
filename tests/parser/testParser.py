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
        result = p.result
        self.assertTrue(isinstance(result, lyanna.tree.kvpair.KVPair))
        self.assertEqual(result.key, 'foo')
        self.assertEqual(result.value, 42)
    def testStringToString(self):
        p=Parser("foo='bar'")
        self.assertTrue(p.kvpair())
        result = p.result
        self.assertEqual(result.key, 'foo')
        self.assertEqual(result.value, 'bar')
    def testAtKey(self):
        p=Parser("@'foo'=42")
        self.assertTrue(p.kvpair())
        result = p.result
        self.assertEqual(result.key, 'foo')
        self.assertEqual(result.value, 42)

class TestLiterals(unittest.TestCase):
    '''Parsing of literal objects'''
    def testParseEmptyList(self):
        p=Parser("[]")
        self.assertTrue(p.list())
        self.assertEqual([], p.result.eval())
    def testParseList(self):
        p=Parser("[1 2 'foo' ['hey' 5] 4]")
        self.assertTrue(p.list())
        result = p.result
        self.assertTrue(isinstance(result, lyanna.tree.List))
        self.assertEqual(result.eval(), [1, 2, 'foo', ['hey', 5], 4])
    def testParseEmptyMap(self):
        p=Parser('{}')
        self.assertTrue(p.map())
        self.assertEqual({}, p.result.eval())
    def testParseMap(self):
        p=Parser("{a=42 b={foo='bar'} @'guh' =   [3 4]}")
        self.assertTrue(p.map())
        self.assertEqual({'a':42,'b':{'foo':'bar'}, 'guh':[3, 4]}, p.result.eval())
        
        