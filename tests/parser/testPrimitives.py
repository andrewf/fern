import unittest
from fern.parser.parser import Parser

class ParseBool(unittest.TestCase):
    def testTrue(self):
        p=Parser('true')
        p.bool()
        self.assertEqual(p.result, True)
    def testFalse(self):
        p=Parser('false')
        p.bool()
        self.assertEqual(p.result, False)
    def testExpression(self):
        p=Parser('true')
        p.expression()
        self.assertEqual(p.result, True)
