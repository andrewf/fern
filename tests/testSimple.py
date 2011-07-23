import unittest
from fern import simple, primitives, errors
import fern

class NonSimple(object):
    'just for testing purposes'

class TestMap(unittest.TestCase):
    def setUp(self):
        self.m = simple.Map()
    def testStringKey(self):
        self.m['iz a string'] = 14
        self.assertEqual(self.m['iz a string'], 14)
    def testNumberKey(self):
        self.m[42] = 'foo'
        self.assertEqual(self.m[42], 'foo')
    def testNothingKey(self):
        self.m[primitives.Nothing] = 'fuzz'
        self.assertEqual(self.m[primitives.Nothing], 'fuzz')
    def testMissingKeyisUndefined(self):
        self.assertEqual(self.m['I do not exist'], primitives.Undefined)
    def testUndefinedValueDeletesKey(self):
        self.m['foo'] = 17
        self.m['foo'] = primitives.Undefined
        self.failIf('foo' in self.m)
        
class TestList(unittest.TestCase):
    def setUp(self):
        self.l = simple.List()
    def testAppend(self):
        self.l.append(42)
        self.assertEqual(self.l[0], 42)
    def testNonSimpleValue(self):
        self.assertRaises(
            fern.errors.TypeError,
            self.l.append, NonSimple)

class TestFunctionCall(unittest.TestCase):
    def setUp(self):
        self.f = simple.AbstractCall('foo', 42, 'gah!')
    def testName(self):
        self.assertEqual(self.f.name, 'foo')
    def testArgAccess(self):
        self.assertEqual(self.f[0], 42)
        self.assertEqual(self.f[1], 'gah!')

class TestTreeNode(unittest.TestCase):
    def setUp(self):
        self.t = simple.TreeNode('node')
    def testType(self):
        self.t.type = 'node'

class TestIsSimple(unittest.TestCase):
    def testMapIsSimple(self):
        self.assertTrue(simple.is_simple(simple.Map()))
    def testListIsSimple(self):
        self.assertTrue(simple.is_simple(simple.List()))
    def testAbstractCallIsSimple(self):
        self.assertTrue(simple.is_simple(simple.AbstractCall('f')))
    def testTreeNodeIsSimple(self):
        self.assertTrue(simple.is_simple(simple.TreeNode('x')))
    def testPrimitivesAreSimple(self):
        self.assertTrue(simple.is_simple(primitives.Undefined))
        self.assertTrue(simple.is_simple(primitives.Nothing))
        self.assertTrue(simple.is_simple(True))
        self.assertTrue(simple.is_simple(17))
        self.assertTrue(simple.is_simple('iz in ur string'))

class TestTruthy(unittest.TestCase):
    def testBoolean(self):
        self.assertTrue(simple.truthy(True))
        self.assertFalse(simple.truthy(False))
    def testUndefined(self):
        self.assertFalse(simple.truthy(primitives.Undefined))
    def testNothing(self):
        self.assertFalse(simple.truthy(primitives.Nothing))
    def testEmptyString(self):
        self.assertFalse(simple.truthy(''))
    def testString(self):
        self.assertTrue(simple.truthy('fff'))
    def testEmptyMap(self):
        self.assertFalse(simple.truthy(simple.Map()))
    def testMap(self):
        m = simple.Map()
        m['foo'] = 17
        self.assertTrue(simple.truthy(m))

