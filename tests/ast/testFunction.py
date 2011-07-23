import unittest

from fern.ast.function import Function, FunctionCall
from fern.ast.map import Map, KVPair
from fern.ast.nameref import NameRef
from fern.errors import SemanticError

class TestFunction(unittest.TestCase):
    def testNoArgs(self):
        m = Map()
        m.put(KVPair('foo', 42))
        f = Function(m)
        r = f.call()
        self.assertEqual(r, {'foo': 42})
    def testOneArg(self):
        m = Map()
        m.put(KVPair('foo', NameRef('arg')))
        f = Function(m, ['arg'])
        r = f.call(42)
        self.assertEqual(r, {'foo': 42})
    def testTwoArgs(self):
        m = Map()
        m.put(KVPair('foo', NameRef('arg1')))
        m.put(KVPair('bar', NameRef('arg2')))
        f = Function(m, ['arg1', 'arg2'])
        r = f.call(42, 'ackup')
        self.assertEqual(r, {'foo': 42,'bar':'ackup'})
    def testArgListMismatch(self):
        f = Function(Map(), ['arg1', 'arg2'])
        self.assertRaises(SemanticError, f.call, 'ackup', 13, 'urp')

class TestCall(unittest.TestCase):
    def setUp(self):
        # create functions
        m0 = Map()
        m0.put(KVPair('guk', NameRef('foo')))
        self.f0 = Function(m0)
        m1 = Map()
        m1.put(KVPair('ack', NameRef('arg')))
        self.f1 = Function(m1, ['arg'])
        m2 = Map()
        m2.put(KVPair('froz', NameRef('arg1')))
        m2.put(KVPair('fuzz', NameRef('arg2')))
        self.f2 = Function(m2, ['arg1', 'arg2'])
        # put them in place
        self.m = Map()
        self.m.put(KVPair('foo', 42))
        self.m.put(KVPair('f0',self.f0))
        self.m.put(KVPair('f1',self.f1))
        self.m.put(KVPair('f2',self.f2))
        self.m.put(KVPair('call0', FunctionCall(NameRef('f0'))))
        self.m.put(KVPair('call1', FunctionCall(NameRef('f1'), [13])))
        self.m.put(KVPair('call2', FunctionCall(NameRef('f2'), ['ack', 17])))
    def testCall0(self):
        self.assertEqual(self.m['call0'], {'guk':42})
    def testCall1(self):
        self.assertEqual(self.m['call1'], {'ack': 13})
    def testCall2(self):
        self.assertEqual(self.m['call2'], {'froz':'ack', 'fuzz': 17})
