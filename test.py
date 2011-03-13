import unittest
import lyanna

class testParse(unittest.TestCase):
	def testParseEmpty(self):
		obj = lyanna.parse('')
		self.assertTrue(isinstance(obj, lyanna.Map))
		self.assertEqual(len(obj), 0)
	def testNumberVariables(self):
		obj = lyanna.parse("var = 42 other = 13")
		self.assertEqual(obj['var'], 42)
		self.assertEqual(obj['other'], 13)
	def testStringVariables(self):
		obj = lyanna.parse("var = 'a string'")
		self.assertEqual(obj['var'], 'a string')
	def testStringAndNumberVariables(self):
		obj = lyanna.parse("one = 1 two='two'")
		self.assertEqual(obj['one'], 1)
		self.assertEqual(obj['two'], 'two')
	def testParseAtSign(self):
		obj = lyanna.parse("@'key'   = 'value'")
		self.assertEqual(obj['key'], 'value')
	def testParseMap(self):
		obj = lyanna.parse("foo = {key = 'value'}")
		foo = obj['foo']
		self.assertEqual(foo['key'], 'value')
	def testParseList(self):
		obj = lyanna.parse("foo = ['one' 2 'three']")
		l = obj['foo']
		self.assertEqual(len(l), 3)
		self.assertEqual(l[0], 'one')
		self.assertEqual(l[1], 2)
		self.assertEqual(l[2], 'three')
	def testMapInListInMap(self):
		obj = lyanna.parse("foo = {key1 = [1 {key2=42}]}")
		foo = obj['foo']
		l = foo['key1']
		inner_map = l[1]
		self.assertEqual(inner_map['key2'], 42)
	def testMapAsKey(self):
		obj = lyanna.parse("@{key = 'faz'}=13")
		idkey = obj.d.keys()[0]
		key = idkey[0]
		self.assertEqual(obj[key], 13)
	def testBoolValue(self):
		obj = lyanna.parse("t = True f = False")
		self.assertEqual(obj['t'], True)
		self.assertEqual(obj['f'], False)

class ScopeAndReferences(unittest.TestCase):
    def testReference(self):
        obj = lyanna.parse("one = 42 two = one")
        self.assertEqual(obj['one'], 42)
        self.assertEqual(obj['two'], 42)
    def testScope1(self):
        obj = lyanna.parse("var = 42 foo = {baz = var}")
        self.assertEqual(obj['foo']['baz'], 42)
    def testLexicalScope(self):
        obj = lyanna.parse("var = 42 foo = {var = 13 baz = var}")
        self.assertEqual(obj['foo']['baz'], 13)
    def testLexicalScope2(self):
        obj = lyanna.parse("var = 42 foo = [ 13 'junk'  {var = 17 baz = var}]")
        self.assertEqual(obj['foo'][2]['baz'], 17)    

class testMap(unittest.TestCase):
	def testMapAsKey(self):
		k = lyanna.Map()
		k['key'] = 'value'
		m = lyanna.Map()
		m[k] = 'keyed by a map'
		self.assertEqual(m[k], 'keyed by a map')
	def testListAsKey(self):
		l = lyanna.List()
		l.put('foop')
		m = lyanna.Map()
		m[l] = 'foobar'
		self.assertEqual(m[l], 'foobar')

if __name__ == '__main__':
	unittest.main()
