from plex import *
from model import *
from StringIO import StringIO
letter = Range("AZaz")
identifier = letter + Rep(letter | Range("09"))
number = Rep1(Range('09'))
string = Str("'") + Rep(AnyBut("'")) + Str("'")

lexicon = Lexicon([
    (Str('}'),       'map_end'),
    (Str('{'),       'map_start'),
    (Str('['),       'list_start'),
    (Str(']'),       'list_end'),
    (Str('('),       'param_start'),
    (Str(')'),       'param_end'),
    (Str('='),       'assign'),
    (Str('@'),       'at_sign'),
    (Str('True'),    'true'),
    (Str('False'),   'false'),
    (Str('if'),      TEXT),
    (Str('then'),    TEXT),
    (Str('else'),    TEXT),
    (Str('end'),     TEXT),
    (Str('elif'),    TEXT),
    (Str('function'),TEXT),
    (Str('do'),      TEXT),
    (Any(' \n\t'),   IGNORE),
    (number,         'number'),
    (string,         'string'),
    (identifier,     'ident'),
])

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
    @property
    def text(self):
        '''
        the text of self.next_token
        '''
        return self.next_token[1]

class Builder:
    def __init__(self):
        '''
        Sets up item stack, prepares for items
        '''
        self.items = [Map(None)]
    @property
    def item(self):
        '''the top item in the stack'''
        if self.items:
            return self.items[-1]
        else:
            raise ValueError('no items in item stack')
    def put(self, item): # puts atomic items in the current container
        self.item.put(item)
    def reference(self, name):
        "Returns the named object, looking through item stack for maps"
        searchspace = reversed(filter(lambda x: isinstance(x, Map), self.items))
        for m in searchspace:
            if name in m:
                return m[name]
        raise ValueError('invalid name reference')
    def start_kvpair_key(self):
        '''Put a kvpair on the stack'''
        if not isinstance(self.item, Map): raise ValueError('adding kvpair to non-map')
        self.items.append(KVPair())
    def start_kvpair_value(self):
        if not self.item.has_key:
            raise ValueError('trying to start value without a key')
    def start_function(self):
        self.items.append(Function(self.top_scope))
    def start_map(self): # makes a new map be the current item
        self.items.append(Map(self.top_scope))
    def start_list(self):
        self.items.append(List(self.top_scope))
    def start_if(self):
        self.items.append(IfGenerator())
    def start_nameref(self):
        self.items.append(NameReference(self.top_scope))
    def finish_item(self):
        it = self.items.pop()
        self.item.put(it)
    @property
    def top_scope(self):
        '''topmost item that can look up names'''
        for item in reversed(self.items):
            if isinstance(item, Scope):
                return item
        raise ValueError('oh crap, no scope items in builder stack???!?')
    
    
##########################################
# recursive descent parser on plex tokens 
##########################################

# each function either returns false and consumes no input or returns true and consumes input

def start(scanner, builder):
    while True:
        # kvpair or die
        if scanner.next_token[0] is not None:
            if not kvpair(scanner, builder):
                raise ValueError('root object must be kvpairs')
        else:
            break
            

def kvpair(scanner, builder):
    if not match_namedecl(scanner, builder):
        return False
    if not scanner.match('assign'):
        raise ValueError('expected assignment after name declaration')
    builder.start_kvpair_value()
    if not expression(scanner, builder):
        raise ValueError('expected expression after assignment')
    builder.finish_item()
    return True

def match_map(scanner, builder):
    if scanner.match('map_start'):
        builder.start_map()
        while True:
            # first try to match '}'
            if scanner.match('map_end'):
                builder.finish_item()
                return True
            elif kvpair(scanner, builder):
                continue
            else:
                # if both failed, parse error
                raise ValueError('failed to parse \'}\' or kvpair in map')
    return False
        
def match_list(scanner, builder):
    if scanner.match('list_start'):
        builder.start_list()
        while True:
            if scanner.match('list_end'):
                builder.finish_item()
                return True
            if expression(scanner, builder):
                continue
            else:
                raise ValueError('failed to parse \']\' or expression in list')
    return False

def match_bool(scanner, builder):
    if scanner.match('true'):
        builder.put(True)
        return True
    elif scanner.match('false'):
        builder.put(False)
        return True
    else:
        return False

def match_if(scanner, builder):
    if not scanner.match('if'):
        return False
    builder.start_if()
    if not expression(scanner, builder):
        raise ValueError('invalid condition in if')
    if not scanner.match('then'):
        raise ValueError('must follow if condition with \'then\'')
    if not expression(scanner, builder):
        raise ValueError('must have expr after then')
    # look for 0..n elifs
    while scanner.match('elif'):
        if not expression(scanner, builder):
            raise ValueError('invalid elif condition')
        if not scanner.match('then'):
            raise ValueError('must follow if condition with \'then\'')
        if not expression(scanner, builder):
            raise ValueError('must have expr after then')
    # look for else clause
    if not scanner.match('else'):
        raise ValueError('expected "else"')
    builder.item.start_else()
    if not expression(scanner, builder):
        raise ValueError('expected else expression')
    if not scanner.match('end'):
        raise ValueError('expected "end" of if')
    builder.finish_item()
    return True

def match_function(scanner, builder):
    if not scanner.match('function'):
        return False
    builder.start_function()
    while True:
        text = scanner.text
        if not scanner.match('ident'): break
        builder.put(text)
    if not scanner.match('do'):
        raise ValueError('expected \'do\' after parameters')
    builder.item.end_params()
    if not expression(scanner, builder):
        raise ValueError('expected expression after \'do\'')
    if not scanner.match('end'):
        raise ValueError('must have \'end\' after function')
    builder.finish_item()
    return True

def match_nameref(scanner, builder):
    def match_paramlist():
        # open-close parens, with optional expressions
        if not scanner.match('param_start'):
            return False
        builder.item.start_params()
        while True:
            if not expression(scanner, builder): break
        if not scanner.match('param_end'):
            raise ValueError('expecting \')\' to end param list')
        return True
    text = scanner.text
    if scanner.match('ident'):
        # text is the name
        builder.start_nameref()
        builder.put(text)
        match_paramlist()
        builder.finish_item()
        return True
    elif scanner.match('at_sign'):
        builder.start_nameref()
        if not expression(scanner, builder):
            raise ValueError('no expression after \'@\'')
        match_paramlist()
        builder.finish_item()
        return True
    return False

def match_namedecl(scanner, builder):
    # mainly for use in kvpairt_, calls start_kvpair_key stuff
    text = scanner.text
    if scanner.match('ident'):
        builder.start_kvpair_key()
        builder.put(text)
        return True
    elif scanner.match('at_sign'):
        builder.start_kvpair_key()
        if not expression(scanner, builder):
            raise ValueError('no expression after \'@\' in name decl')
        return True
    return False
        

def expression(scanner, builder):
    text = scanner.text
    #print 'matching expr token', scanner.next_token
    if scanner.match('number'):
        builder.put(int(text))
        return True
    elif scanner.match('string'):
        # strip off one quote character on each end of the string
        builder.put(text[1:-1])
        return True
    elif match_map(scanner, builder):
        return True
    elif match_list(scanner, builder):
        return True
    elif match_bool(scanner, builder):
        return True
    elif match_if(scanner, builder):
        return True
    elif match_function(scanner, builder):
        return True
    elif match_nameref(scanner, builder):
        return True
    else:
        return False
    
    

##########################################


def parse(data):
    scanner = MatchScanner(lexicon, StringIO(data))
    builder = Builder()
    start(scanner, builder)
    return builder.items[0]
