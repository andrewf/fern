'''
Defines data structures used as parse tree for Lyanna. This is
syntax-independent.
'''

class Error(Exception):
    'Semantic errors, regardless of syntax'
    pass

class KeyError(Error):
    '''
    For bad key/name lookups
    '''
    def __init__(self, key):
        self.key = key

class ItemStream(object):
    '''Items from a generator construct, to be placed in a container'''

class Node(object):
    '''
    Base class for all parse tree nodes.
    
    Specifically, those that can have children. All of them serve
    as name scopes. This class provides the default implementation,
    which is to look in the parent object.
    '''
    pass
    def __init__(self, parent):
        self.parent = parent
    def lookup(self, key):
        'punt to parent, else error. raises KeyError'
        if self.parent:
            return self.parent.lookup(key)
        else:
            raise KeyError(key)

class Container(Node):
    '''
    Stub base for containers, for identity purposes
    '''
    pass

class Map(Container):
    '''
    Key-value pairs, in order of appearance in source.
    
    Children can be kvpair objects or generators that produce
    streams of kvpairs. The kvpairs can repeat keys; later keys will
    override older ones in the conversion phase.
    '''
    def __init__(self, parent):
        Node.__init__(self, parent)
        self.children = []
    def put(self, item):
        '''Add a new child'''

class List(Container):
    '''
    List of items
    
    Children can be items or generators that return streams.
    '''
    def __init__(self, parent):
        Node.__init__(self, parent)
        self.children = []

class Generator(Node):
    '''
    Base class for all generators.
    
    Generators have a get method that, generally, returns
    a stream. It may just return a single object if that's all it holds.
    '''
    def __init__(self, parent):
        Node.__init__(self, parent)
    
class IfGenerator(Generator):
    '''
    Models a condition expression.
    
    Contains a series of condition/result pairs, which are evaluated
    in the order added. If all fail, else is returned, unless there
    is no else, in which case undefined is returned. 
    '''
    def __init__(self, p):
        Node.__init__(self, p)
        self.conditions = [] # [(expr, stream|item)]
        self.elseval = None # or expr
    def addCondition(self, condition, result):
        self.conditions.append((condition, result))
    def setElse(self, result):
        self.elseval = result

class LetGenerator(Generator):
    '''
    A let clause. Adds names to child objects, but those names aren't exported
    
    Contains a series of kvpairs, in order like in Map, then an item stream
    '''
    



    