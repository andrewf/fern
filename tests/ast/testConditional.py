import unittest

from fern.ast.conditional import Conditional
from fern.ast.map import Map
from fern.ast.list import List
from fern.ast.kvpair import KVPair
from fern.ast.nameref import NameRef
from fern.ast.tools import ItemStream
from fern.primitives import Undefined

class TestIfItem(unittest.TestCase):
    def setUp(self):
        self.scope = Map()
        self.scope['var'] = True
        self.m = Map()
        self.scope['bar'] = self.m
        self.c = Conditional()
        self.scope['cond'] = self.c
    def testOneCond(self):
        self.c.put_cond(NameRef('var'), 'foo')
        self.assertEqual(self.c.eval(), 'foo')
        self.scope.set_key('var', False)
        self.assertEqual(self.c.eval(), Undefined)
    def testTwoConds(self):
        # one
        self.c.put_cond(NameRef('var'), 'foo')
        self.c.put_cond(NameRef('bar'), 'fuzz')
        self.assertEqual(self.c.eval(), 'foo')
        # two
        self.scope.set_key('var', False)
        self.assertEqual(self.c.eval(), Undefined)
        # three
        self.m['nothing'] = 42
        self.assertEqual(self.c.eval(), 'fuzz')
    def testElse(self):
        self.scope.set_key('var', False)
        self.c.refresh() # make sure setting else works after refresh
        self.c.else_val = 'guth'
        self.assertEqual(self.c.eval(), 'guth')

class TestPairStream(unittest.TestCase):
    def setUp(self):
        self.scope = Map()
        self.scope['var'] = True
        self.c = Conditional()
        self.scope.put(self.c)
    def testStream(self):
        self.c.put_cond(
            NameRef('var'),
            ItemStream([ KVPair('ag', 56), KVPair('ug', NameRef('var')) ])
        )
        self.assertEqual(self.scope['ag'], 56)
        self.assertEqual(self.scope['ug'], True)
    def testUndefinedHasNoEffect(self):
        self.scope.set_key('var', False)
        self.assertEqual(self.scope.eval(), {'var':False}) # and nothing else

class TestStreamInList(unittest.TestCase):
    def setUp(self):
        self.stream = ItemStream([
            'Fuzz', NameRef('var')
        ])
        self.scope = Map()
        self.scope['var'] = True
        self.l = List()
        self.c = Conditional()
        self.c.put_cond(NameRef('var'), self.stream)
        self.l.put('first')
        self.l.put(self.c)
        self.scope['list'] = self.l
    def testItems(self):
        self.assertEqual(self.l.eval(), ['first', 'Fuzz', True])
    