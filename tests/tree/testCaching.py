'''
Tests interactions between caching systems of various nodes
'''

import unittest
import lyanna
from lyanna.tree import Map, List

class NestedCaching(unittest.TestCase):
    def setUp(self):
        #root = {
        #    one = 42
        #    two = {
        #        var = 13
        #    }
        #    three = [
        #        1 2 3
        #    ]
        #}
        self.root = Map()
        self.root['one'] = 42
        self.two = Map()
        self.two['var'] = 13
        self.root['two'] = self.two
        self.three = List()
        self.three.put(1)
        self.three.put(2)
        self.three.put(3)
        self.root['three'] = self.three
        # flush changes now, so changes in tests are forced to invalidate map
        self.root.refresh() 
        self.expected = {'one': 42, 'two': {'var':13}, 'three':[1, 2, 3]}
    def testEval(self):
        self.assertEqual(self.root.eval(), self.expected)
    def testOne(self):
        self.root['one'] = 13
        expected = {'one': 13, 'two': {'var':13}, 'three':[1, 2, 3]}
        self.assertEqual(self.root.eval(), expected)
    def testTwo(self):
        self.two['var'] = 17
        expected = {'one': 42, 'two': {'var':17}, 'three':[1, 2, 3]}
        self.assertEqual(self.root.eval(), expected)
    def testThree(self):
        self.three.put('hey!')
        expected = {'one': 42, 'two': {'var':13}, 'three':[1, 2, 3, 'hey!']}
        self.assertEqual(self.root.eval(), expected)
