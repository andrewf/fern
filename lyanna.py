from plex import *
from StringIO import StringIO

letter = Range("AZaz")
identifier = letter + Rep(letter | Range("09"))
number = Rep1(Range('09'))
string = Str("'") + Rep(AnyBut("'")) + Str("'")

lexicon = Lexicon([
    (Str('}'),      'map_end'),
    (Str('{'),      'map_start'),
    (Str('['),      'list_start'),
    (Str(']'),      'list_end'),
    (Str('='),      'assign'),
    (Str('@'),      'at_sign'),
    (Str('True'),   'true'),
    (Str('False'),  'false'),
    (Str('if'),     TEXT),
    (Str('then'),   TEXT),
    (Str('else'),   TEXT),
    (Str('end'),    TEXT),
    (Any(' \n\t'),  IGNORE),
    (number,        'number'),
    (string,        'string'),
    (identifier,    'ident'),
])

class IdKey(tuple):
    '''
    Wrap a mutable object in this to allow it to be used as a dict key.
    Compares by identity.'''
    def __new__(cls, obj):
        return tuple.__new__(cls, (obj,))

class Map(object):
    '''
    A wrapper for dict that allows Map's and List's as keys.

    When used as keys
    '''
    def __init__(self):
        self.d = {}
    def __len__(self):
        return len(self.d)
    def __getitem__(self, k):
        return self.d[hashable_key(k)]
    def __setitem__(self, k, v):
        self.d[hashable_key(k)] = v
    def put(self, kvpair):
        assert(isinstance(kvpair, KVPair))
        self[kvpair.key] = kvpair.value
    def __contains__(self, item):
        return item in self.d

class List(object):
    def __init__(self):
        self.l = []
    def __len__(self):
        return len(self.l)
    def __getitem__(self, k):
        return self.l[k]
    def __setitem__(self, k, v):
        self.d[k] = v
    def put(self, v):
        self.l.append(v)

class IfGenerator(object):
    def __init__(self):
        self.cond = None
        self.first = None
        self.second = None
    def put(self, item):
        if self.cond is None:
            self.cond = item
        elif self.first is None:
            self.first = item
        elif self.second is None:
            self.second = item
        else:
            raise ValueError('too much stuff in if')
    def get(self):
        if self.cond:
            return self.first
        else:
            return self.second

def hashable_key(obj):
    'Makes sure the obj is hashable, wrapping in IdKey if needed'
    # actually, it's not that picky. Just makes sure to wrap Map and List
    if isinstance(obj, (Map, List)):
        return IdKey(obj)
    else:
        return obj

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

class KVPair(object):
    '''
    Just for building
    '''
    def __init__(self):
        self.has_key = False
    def put(self, item):
        if not self.has_key:
            self.key = item
            self.has_key = True
        else:
            self.value = item

class Builder:
    def __init__(self):
        '''
        Sets up item stack, prepares for items
        '''
        self.items = [Map()]
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
    def end_kvpair(self):
        '''pop pair and put it in previous container'''
        self.finish_item()
    def start_map(self): # makes a new map be the current item
        self.items.append(Map())
    def end_map(self):
        self.finish_item()
    def start_list(self):
        self.items.append(List())
    def end_list(self):
        self.finish_item()
    def start_if(self):
        self.items.append(IfGenerator())
    def end_if(self):
        self.finish_item()
    def finish_item(self):
        it = self.items.pop()
        self.item.put(it)
    
    
##########################################
# recursive descent parser on plex tokens 
##########################################

# each function either returns false and consumes no input or returns true and consumes input

def start(scanner, builder):
    while kvpair(scanner, builder): pass

def kvpair(scanner, builder):
    text = scanner.text
    if scanner.match('ident'):
        builder.start_kvpair_key()
        builder.put(text)
        if scanner.match('assign'):
            builder.start_kvpair_value()
            if expression(scanner, builder):
                builder.end_kvpair()
                return True
            else:
                # there was an assignment, but no valid expr
                raise ValueError('assignment of invalid expr')
        else:
            return False
    elif scanner.match('at_sign'):
        builder.start_kvpair_key()
        if expression(scanner, builder):
            builder.start_kvpair_value()
            if scanner.match('assign'):
                builder.start_kvpair_value()
                if expression(scanner, builder):
                    builder.end_kvpair()
                    return True
                else:
                    # there was an assignment, but no valid expr
                    raise ValueError('assignment of invalid expr')
            else:
                # didn't match assignment
                raise ValueError('\'@\' with no assignment')
        else:
             raise ValueError('\'@\' with no expression')
    else:
        return False

def match_map(scanner, builder):
    if scanner.match('map_start'):
        builder.start_map()
        while True:
            # first try to match '}'
            if scanner.match('map_end'):
                builder.end_map()
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
                builder.end_list()
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
    if not scanner.match('else'):
        raise ValueError('expected "else"')
    if not expression(scanner, builder):
        raise ValueError('expected else expression')
    if not scanner.match('end'):
        raise ValueError('expected "end" of if')
    builder.end_if()
    return True

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
    elif scanner.match('ident'):
        builder.put(builder.reference(text))
        return True
    else:
        return False
    
    

##########################################


def parse(data):
    scanner = MatchScanner(lexicon, StringIO(data))
    builder = Builder()
    start(scanner, builder)
    return builder.items[0]


def get_tokens(data):
    tokens = []
    s = Scanner(lexicon, StringIO(data))
    while True:
        t = s.read()
        tokens.append(t)
        if t[0] is None:
            break
    return tokens
