'''
Tests interactions between caching systems of various nodes
'''

import unittest
import fern
from fern.ast import Map, List, NameRef

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

class DeepNesting(unittest.TestCase):
    def setUp(self):
        #root = {
        #    ref = [1 1 2 3]
        #    a = {aa = 14 ab = {foo = ref}}
        #    b = {ba = a}
        #}
        self.root = Map()
        # first toplevel item
        self.ref = List()
        self.ref.put(1)
        self.ref.put(1)
        self.ref.put(2)
        self.ref.put(3)
        self.root['ref'] = self.ref
        # second
        self.a = Map()
        self.a['aa'] = 14
        self.ab = Map()
        self.ab['foo'] = NameRef('ref')
        self.a['ab'] = self.ab
        self.root['a'] = self.a
        # third
        self.b = Map()
        self.b['ba'] = NameRef('a')
        self.root['b'] = self.b
        # expected simplified value
        self.expected = {
            'ref':[1, 1, 2, 3],
            'a':{
                'aa': 14,
                'ab': {'foo': [1, 1, 2, 3]}
            },
            'b':{
                'ba':{
                    'aa': 14,
                    'ab': {'foo': [1, 1, 2, 3]}
                }
            }
        }
    def testEvaluation(self):
        self.assertEqual(self.expected, self.root.eval())
    def testMutateNameRef(self):
        self.ref.put(5)
        self.expected['ref'].append(5)
        self.expected['a']['ab']['foo'].append(5)
        self.expected['b']['ba']['ab']['foo'].append(5)
        self.assertEqual(self.expected, self.root.eval())
