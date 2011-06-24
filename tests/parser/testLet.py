import unittest
from fern.parser.parser import Parser

class ParseLet(unittest.TestCase):
    def setUp(self):
        p = Parser(
            '''let a=4 b='hey' in
                root_var = [a b]
            end
            
            list = [1 let x=4 in {f = x} end 'arg']
            
            var = let y='herp' in {saying=y} end
        ''')
        self.root = p.parse()
    def testRootVar(self):
        self.assertEqual(self.root['root_var'], [4, 'hey'])
    def testList(self):
        self.assertEqual(self.root['list'], [1, {'f': 4}, 'arg'])
    def testVar(self):
        self.assertEqual(self.root['var'], {'saying':'herp'})