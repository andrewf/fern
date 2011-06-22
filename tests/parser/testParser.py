import unittest
import lyanna
from lyanna.parser.parser import Parser
from StringIO import StringIO

class Basics(unittest.TestCase):
    def setUp(self):
        self.p = Parser("foo= 42@'bar' = 'ggg'")
        self.fdg = self.p.parse()
    def testIsMap(self):
        self.assertTrue(isinstance(self.fdg, lyanna.tree.Map))
    def testKeys(self):
        self.assertEqual(self.fdg['foo'], 42)
        self.assertEqual(self.fdg['bar'], 'ggg')

class FileAccess(unittest.TestCase):
    def testAcceptsFileLike(self):
        f = StringIO("foo=17 bar='ughu'")
        p = Parser(f)
        m = p.parse()
        self.assertEqual(m['foo'], 17)
        self.assertEqual(m['bar'], 'ughu')

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

class TestNameRef(unittest.TestCase):
    def testAlone(self):
        p=Parser('foo')
        self.assertTrue(p.nameref())
        self.assertEqual(p.result.name, 'foo')
    def testBasic(self):
        p=Parser('a=3 b=a')
        m = p.parse()
        self.assertEqual(m['b'], 3)
        m.set_key('a', 5)
        self.assertEqual(m['b'], 5)
    def testWithMaps(self):
        p=Parser('a={bar=42} b={foo=a}')
        m = p.parse()
        self.assertEqual(m.eval(), {'a':{'bar':42}, 'b':{'foo':{'bar':42}}})
    # we're not gonna do @ namerefs just yet


