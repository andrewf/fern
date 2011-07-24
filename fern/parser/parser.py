import fern
from builder import ParseStack, Builder
from StringIO import StringIO

# setup lexer
from plex import *
letter = Range("AZaz")
identifier = letter + Rep(letter | Range("09") | Str("_"))
num = Rep1(Range('09'))
string = Str("'") + Rep(AnyBut("'")) + Str("'")
comment = Str('--') + Rep(AnyBut('\n')) + Str('\n')

lexicon = Lexicon([
    (comment, IGNORE), # must be before directive to ignore \n below
    (Any(' \n\t'), IGNORE),
    (Str('['), TEXT),
    (Str(']'), TEXT),
    (Str('{'), TEXT),
    (Str('}'), TEXT),
    (Str('('), TEXT),
    (Str(')'), TEXT),
    (Str('='), TEXT),
    (Str('@'), TEXT),
    (Str('if'), TEXT),
    (Str('then'), TEXT),
    (Str('elif'), TEXT),
    (Str('else'), TEXT),
    (Str('end'), TEXT),
    (Str('let'), TEXT),
    (Str('in'), TEXT),
    (Str('true'), TEXT),
    (Str('false'), TEXT),
    (Str('function'), TEXT),
    (identifier, 'ident'),
    (num, 'number'),
    (string, 'string'),
])

# token types
ident = 'ident'
number = 'number'
assign = '='
at = '@'
string = 'string'
list_start = '['
list_end = ']'
map_start = '{'
map_end = '}'

class MatchScanner(Scanner):
    def __init__(self, *args, **kwargs):
        Scanner.__init__(self, *args, **kwargs)
        self.next_token = self.read()
    def match(self, toktype):
        if self.next_token[0] == toktype:
            t = self.next_token
            self.next_token = self.read()
            return True
        else:
            return False
    def expect(self, toktype, msg):
        if not self.match(toktype):
            raise SyntaxError(msg + str(self.position()))
    @property
    def text(self):
        '''
        the text of self.next_token
        '''
        return self.next_token[1]

class Parser(object):
    def __init__(self, input):
        self.stack = ParseStack()
        if isinstance(input, basestring):
            input = StringIO(input)
        self.tokens = MatchScanner(lexicon, input)
    def parse(self):
        'Parse the start/root symbol of the grammar'
        self.start()
        return self.result
    @property
    def result(self):
        '''Result of parsing whatever function, i.e. the top of the stack.
        
        For testing, I want to be able to call any parsing sub-function and
        get the result. I would just get stack.top, but I want a function to
        handle conditionally calling .get() on builders.
        '''
        it = self.stack.top
        if isinstance(it, Builder):
            return it.get()
        return it
    # All parser functions return True when successful, False when they fail
    # They do their work on the stack, occasionally leaving things there for
    # following functions to pick up.
    def start(self):
        "Parses the root map"
        self.stack.start_map()
        self.kvpairs()
    def kvpair(self):
        if not self.namedecl(): # leaves name on the stack
            return False
        name = self.stack.pop().get()
        self.stack.start_kvpair()
        self.stack.put(name)
        self.tokens.expect(assign, 'expected = after name declaration')
        if not self.expression(): # puts it on the stack
            raise SyntaxError('expected expression after =, %s' % str(self.tokens.position()))
        self.stack.finish_item()
        return True
    def namedecl(self):
        text = self.tokens.text
        if self.tokens.match(ident):
            self.stack.start_namedecl()
            self.stack.put(text)
            return True
        if self.tokens.match(at):
            self.stack.start_namedecl()
            if self.expression():
                return True
            raise SyntaxError('expected expression after @')
        else:
            return False
    def nameref(self):
        text = self.tokens.text
        if self.tokens.match(ident):
            self.stack.push(fern.ast.NameRef(text))
            self.fcall_tail()
            self.stack.finish_item()
            return True
        return False
    def item(self):
        text = self.tokens.text
        if self.tokens.match(number):
            self.stack.put(int(text))
            return True
        elif self.tokens.match(string):
            self.stack.put(text[1:-1])
            return True
        elif (self.list() or
              self.map() or
              self.nameref() or
              self.bool() or
              self.function()):
            return True
        else:
            return False
    def expression(self):
        return self.item() or self.cond_item() or self.let_item()
    def function(self):
        if not self.tokens.match('function'):
            return False
        self.stack.start_function()
        self.tokens.expect('(', 'Expected `(\' after `function\'')
        while True:
            if self.namedecl(): # leaves name on stack
                self.stack.put(self.stack.pop().get())
            else:
                break
        self.tokens.expect(')', 'Expected `)\' after function parameter list')
        self.stack.top.start_content()
        if not self.item():
            raise SyntaxError('Expected item after function parameters')
        self.tokens.expect('end', 'Expected `end\' after function body')
        self.stack.finish_item()
        return True
    def fcall_tail(self):
        # call with a (potential) function object already on the stack, i.e.
        # a literal function or a NameRef
        # leaves FCallBuilder on stack.
        if not self.tokens.match('('):
            return False
        # grab function off stack and start an fcall with it
        func = self.stack.pop()
        #if hasattr(func, 'get'): func = func.get() # if it's a builder 
        self.stack.start_fcall()
        self.stack.put(func)
        self.items()
        self.tokens.expect(')', 'Expected `)\' after function call params')
        return True
    def map(self):
        if not self.tokens.match(map_start):
            return False
        self.stack.start_map()
        self.kvpairs()
        if not self.tokens.match(map_end):
            raise SyntaxError('expected } or kvpair in map')
        self.stack.finish_item()
        return True
    def list(self):
        if not self.tokens.match(list_start):
            return False
        self.stack.start_list()
        self.items()
        if not self.tokens.match(list_end):
            raise SyntaxError('expected ] or expression in list')
        self.stack.finish_item()
        return True
    def bool(self):
        if self.tokens.match('true'):
            self.stack.put(True)
            return True
        if self.tokens.match('false'):
            self.stack.put(False)
            return True
        return False
    def cond_impl(self, item_fun):
        "item_fun is called to parse cond values, a bound method on self"
        # first if
        if not self.tokens.match('if'):
            return False
        self.stack.start_conditional()
        if not self.expression():
            raise SyntaxError('expected expression after if')
        self.tokens.expect('then', 'Expected `then` after if condition')
        item_fun()
        # 0-n elifs
        while self.tokens.match('elif'):
            if not self.expression():
                raise SyntaxError('expected expression after elif')
            self.tokens.expect('then', 'Expected `then` after elif condition')
            item_fun()
        # else
        if self.tokens.match('else'):
            self.stack.top.else_coming() # notify CondBuilder conditions are finished
            item_fun()
        # end of conditional
        self.tokens.expect('end', 'Expected `end` after conditional(s)')
        self.stack.finish_item()
        return True
    def cond_kvpairs(self):
        "Conditional with type kvpair stream"
        return self.cond_impl(self.kvpair_stream)
    def cond_item(self):
        "conditional for single item"
        return self.cond_impl(self.expression)
    def cond_itemstream(self):
        "Conditional for multiple items"
        return self.cond_impl(self.itemstream)
    def let_impl(self, fun):
        if not self.tokens.match('let'):
            return False
        self.stack.start_let()
        self.kvpairs()
        if not self.tokens.match('in'):
            raise SyntaxError('expected `in` after let kvpairs %s' % self.tokens.position())
        self.stack.top.start_content()
        fun()
        if not self.tokens.match('end'):
            raise SyntaxError('expected `end` after let content %s' % self.tokens.position())
        self.stack.finish_item()
        return True
    def let_item(self):
        return self.let_impl(self.item)
    def let_itemstream(self):
        return self.let_impl(self.items)
    def let_kvpairs(self):
        return self.let_impl(self.kvpairs)
    def items(self):
        'Puts a series of items in the current top object, does not create new stack frame'
        while not self.tokens.match(None): # while not EOF
            if self.item():
                continue
            if self.cond_itemstream():
                continue
            if self.let_itemstream():
                continue
            break
    def kvpairs(self):
        "puts a series of kvpairs in current top object"
        while not self.tokens.match(None): # while not EOF
            if self.kvpair():
                continue
            if self.cond_kvpairs():
                continue
            if self.let_kvpairs():
                continue
            break
    def itemstream(self):
        '''Actually creates an ItemStream on the stack, as opposed
        to just putting the items in whatever is already on the top'''
        self.stack.start_itemstream()
        self.items()
        self.stack.finish_item()
    def kvpair_stream(self):
        self.stack.start_itemstream()
        self.kvpairs()
        self.stack.finish_item()
