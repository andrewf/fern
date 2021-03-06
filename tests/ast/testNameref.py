import unittest
import fern
from fern.ast import NameRef

class BasicNameref(unittest.TestCase):
    '''Sans actual name lookups'''
    def setUp(self):
        self.nr = fern.ast.NameRef('name')
    def testNameMatches(self):
        self.assertEqual(self.nr.name, 'name')

class SimpleLookup(unittest.TestCase):
    def testSimple(self):
        m = fern.ast.Map()
        m['var'] = 42
        m['ref'] = NameRef('var')
        m.refresh()
        self.assertEqual(m['ref'], 42)

class TestLookup(unittest.TestCase):
    '''Besides just NameRef, this is a test of all name-lookup
    facilities in Lyanna. Kinda SRP-violating...'''
    def setUp(self):
        '''set up a simple but comprehensive test environment
        for looking up names
        '''
        # make a bunch of child objects
        # basically:
        # self.m = {
        #     var = 42
        #     one = var
        #     two = [var]
        #     three = {foo=var}
        # }
        self.one = NameRef('var')
        self.two = fern.ast.List(); self.two.put(NameRef('var'))
        self.three = fern.ast.Map(); self.three['foo'] = NameRef('var')
        self.m = fern.ast.Map()
        self.m['var'] = 42
        self.m['one'] = self.one
        self.m['two'] = self.two
        self.m['three'] = self.three
        self.m.refresh()        
    def testDirectRef(self):
        self.assertEqual(self.one.eval(), 42)
    def testRefThroughMap(self):
        self.assertEqual(self.three['foo'], 42)
    def testRefThroughList(self):
        self.assertEqual(self.two[0], 42)
    def testDirectRefMutated(self):
        self.m['var'] = 13 
        self.assertEqual(self.one.eval(), 13)
    def testRefThroughMapMutated(self):
        self.m.set_key('var', 13)
        self.m.refresh()
        self.assertEqual(self.three['foo'], 13)
    def testRefThroughListMutated(self):
        self.m['var'] = 13
        self.assertEqual(self.two[0], 13)
    def testInvalidKeyReturnsUndefined(self):
        invalid = NameRef('nope')
        self.three['bar'] = invalid
        self.assertEqual(invalid.eval(), fern.primitives.Undefined)
