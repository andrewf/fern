import unittest
import lyanna
from lyanna.tree import NameRef

class BasicNameref(unittest.TestCase):
    '''Sans actual name lookups'''
    def setUp(self):
        self.nr = lyanna.tree.NameRef('name')
    def testNameMatches(self):
        self.assertEqual(self.nr.name, 'name')

class TestLookup(unittest.TestCase):
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
        self.two = lyanna.tree.List(); self.two.put(NameRef('var'))
        self.three = lyanna.tree.Map(); self.three['foo'] = NameRef('var')
        self.m = lyanna.tree.Map()
        self.m['var'] = 42
        self.m['one'] = self.one
        self.m['two'] = self.two
        self.m['three'] = self.three
    def testDirectRef(self):
        self.assertEqual(self.one.get(), 42)
    def testRefThroughMap(self):
        self.assertEqual(self.three['foo'].get(), 42)
    def testRefThroughList(self):
        self.assertEqual(self.two[0].get(), 42)
    def testDirectRefMutated(self):
        self.m['var'] = 13
        self.assertEqual(self.one.get(), 13)
    def testRefThroughMap(self):
        self.m['var'] = 13
        self.assertEqual(self.three['foo'].get(), 13)
    def testRefThroughList(self):
        self.m['var'] = 13
        self.assertEqual(self.two[0].get(), 13)
        
