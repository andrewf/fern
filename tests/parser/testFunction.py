import unittest
from fern.parser.parser import Parser

class ParseFunction(unittest.TestCase):
    def setUp(self):
        p = Parser('''
            f = function()  {urk = 42} end
            person = function(name age) {
                name = name
                age = age
            } end
            oop = f()
            p = person('Joe' 42)
        ''')
        self.root = p.parse()
    def testNoArgs(self):
        self.assertEqual(self.root['oop'], {'urk': 42})
    def testPersonFunction(self):
        self.assertEqual(self.root['p'], {'name':'Joe','age':42})