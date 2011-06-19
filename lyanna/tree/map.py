from lyanna.tree.node import Node
from lyanna import simple
from lyanna.tree.tools import simplify, KVPair        
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
    def put(self, kvpair):
        self.reparent(kvpair)
        self.children.append(kvpair)
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
        # all keys, then all values. yeah, I know...
        return ( map(attrgetter('key'), self.children) +
                 map(attrgetter('value'), self.children) )
            
