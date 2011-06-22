import unittest
from fern import primitives

class TestNothing(unittest.TestCase):
    def testExists(self):
        nothing = primitives.Nothing

class TestUndefined(unittest.TestCase):
    def testExists(self):
        undef = primitives.Undefined

class NotPrimitive(object):
    'Just for testing is_primitive'

class TestIsPrimitive(unittest.TestCase):
    def testNothingIsPrimitive(self):
        self.assertTrue(primitives.is_primitive(primitives.Nothing))
    def testUndefinedIsPrimitive(self):
        self.assertTrue(primitives.is_primitive(primitives.Undefined))
    def testBoolIsPrimitive(self):
        self.assertTrue(primitives.is_primitive(True))
        self.assertTrue(primitives.is_primitive(False))
    def testIntIsPrimitive(self):
        self.assertTrue(primitives.is_primitive(14))
    def testStringIsPrimitive(self):
        self.assertTrue(primitives.is_primitive('iz a string'))
    def testNonPrimitive(self):
        self.assertFalse(primitives.is_primitive(NotPrimitive()))