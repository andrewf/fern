from fern import errors
from fern.ast.node import Node
from fern import simple
from fern.ast.tools import simplify, ItemStream
from fern.ast.kvpair import KVPair       
from operator import attrgetter       

class Map(Node):
    def __init__(self):
        Node.__init__(self)
        self.children = []
        self.namebearing = True
    def reparent(self, item):
        if isinstance(item, KVPair):
            Node.reparent(self, item.key)
            Node.reparent(self, item.value)
        else:
            Node.reparent(self, item)
    def put(self,thing):
        if isinstance(thing, ItemStream):
            for pair in thing:
                self.put_pair(pair)
        else: # assume it's a pair. put_pair handles error case
            self.put_pair(thing)
    def put_pair(self, kvpair):
        if isinstance(kvpair, KVPair):
            self.reparent(kvpair)
            self.children.append(kvpair)
            self.invalidate()
        else:
            raise errors.TypeError('trying to put non-kvpair (%s) in Map' % str(type(kvpair)))
    def __getitem__(self, k):
        self.refresh()
        return self.value[k]
    def __setitem__(self, k, v):
        self.put(KVPair(k, v))
    def set_key(self, k, v):
        '''
        Set the key by mutating existing kvpairs where possible.
        
        Modify the last kvpair with the key, if there is one.
        Otherwise, add a new pair.
        '''
        for pair in reversed(self.children):
            if pair.key == k:
                pair.value = v
                self.invalidate()
                return
        self.put(KVPair(k, v))
    def reference_impl(self, key):
        self.refresh()
        return self.value[key]
    def __contains__(self, key):
        self.refresh()
        return key in self.value
    def refresh_impl(self):
        self.value = simple.Map()
        for pair in self.children:
            self.value[simplify(pair.key)] = simplify(pair.value)
    def get_children(self):
        return self.children
            
