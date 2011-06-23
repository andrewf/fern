import unittest
from fern.parser.parser import Parser

class ParseConditional(unittest.TestCase):
    def testItemIf(self):
        p = Parser('var = false foo = if var then 13 else 17 end')
        m = p.parse()
        self.assertEqual(m['foo'], 17)
        m.set_key('var', True)
        self.assertEqual(m['foo'], 13)
    def testKVPairsIf(self):
        p = Parser('''
            var = true
            var2 = 'f'
            if var then
                foo = 3
                bar = 4
            elif var2 then
                foo = 4
                bar = 3
            else
                ggg = 5
            end
        ''')
        m = p.parse()
        self.assertEqual(m.eval(), {'var':True,'var2':'f','foo':3,'bar':4})
        m.set_key('var', False)
        self.assertEqual(m.eval(), {'var':False,'var2':'f','foo':4,'bar':3})
        m.set_key('var2', False)
        self.assertEqual(m.eval(), {'var':False,'var2':False,'ggg':5})
