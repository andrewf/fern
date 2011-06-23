from fern import errors
from fern.ast.node import Node
from fern import simple
from fern.ast.tools import simplify, ItemStream
from fern.ast.kvpair import KVPair       
from operator import attrgetter       

class Map(Node):
    def __init__(self):
        Node.__init__(self)
        self.children = [] # mostly kvpairs
        self.namebearing = True
    def reparent(self, item): # should not be necessary
        if isinstance(item, KVPair):
            Node.reparent(self, item.key)
            Node.reparent(self, item.value)
        else:
            Node.reparent(self, item)
    def put(self, thing):
        self.reparent(thing)
        if isinstance(thing, ItemStream):
            for pair in thing:
                if not isinstance(pair, KVPair):
                    raise errors.TypeError('Putting itemstream in map with non-kvpairs: %s' % str(type(pair)))
                self.children.append(pair)
        elif isinstance(thing, Node):
            self.children.append(thing)
        self.invalidate()
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
            if isinstance(pair, KVPair):
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
        def eval_pair(pair):
            self.value[simplify(pair.key)] = simplify(pair.value)
        for c in self.children:
            if isinstance(c, KVPair):
                eval_pair(c)
            else:
                it = c.eval()
                if isinstance(it, KVPair):
                    eval_pair(it)
                elif isinstance(it, ItemStream):
                    for item in it:
                        eval_pair(item)
            
    def get_children(self):
        return self.children
            
