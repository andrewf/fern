import lyanna
from builder import ParseStack, Builder
from StringIO import StringIO

# setup lexer
from plex import *
letter = Range("AZaz")
identifier = letter + Rep(letter | Range("09"))
num = Rep1(Range('09'))
string = Str("'") + Rep(AnyBut("'")) + Str("'")

lexicon = Lexicon([
    (identifier, 'ident'),
    (num, 'number'),
    (Str('='), TEXT),
    (string, 'string'),
    (Str('@'), TEXT),
    (Any(' \n\t'), IGNORE),
    (Str('['), TEXT),
    (Str(']'), TEXT),
])

# token types
ident = 'ident'
number = 'number'
assign = '='
at = '@'
string = 'string'
list_start = '['
list_end = ']'

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
            raise SyntaxError(msg)
    @property
    def text(self):
        '''
        the text of self.next_token
        '''
        return self.next_token[1]

class Parser(object):
    def __init__(self, input):
        self.stack = ParseStack()
        self.tokens = MatchScanner(lexicon, StringIO(input))
    # parser functions, UGH, SRP
    def parse(self):
        'Parse the start/root symbol of the grammar'
        self.start()
        return self.result()
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
        while True:
            if self.tokens.next_token[0] is not None:
                if not self.kvpair():
                    raise SyntaxError('Expected kv-pairs in root object')
            else:
                break
            
    def kvpair(self):
        if not self.namedecl(): # leaves name on the stack
            return False
        name = self.stack.pop().get()
        self.stack.start_kvpair()
        self.stack.put(name)
        self.tokens.expect(assign, 'expected = after name declaration')
        if not self.expression(): # puts it on the stack
            raise SyntaxError('expected expression after =')
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
    def expression(self):
        text = self.tokens.text
        if self.tokens.match(number):
            self.stack.put(int(text))
            return True
        elif self.tokens.match(string):
            self.stack.put(text[1:-1])
            return True
        elif self.list():
            return True
        else:
            return False
    def list(self):
        if not self.tokens.match(list_start):
            return False
        self.stack.start_list()
        while self.expression(): pass
        if not self.tokens.match(list_end):
            raise SyntaxError('expected ] or expression in list')
        self.stack.finish_item()
        return True