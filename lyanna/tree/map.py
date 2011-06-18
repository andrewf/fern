from lyanna.tree.node import Node
from lyanna import simple
from lyanna.tree.tools import eval_if_possible, KVPair        

class Map(Node):
    def __init__(self):
        Node.__init__(self)
        self.children = []
        self.value = None
    def reparent(self, item):
        if isinstance(item, KVPair):
            Node.reparent(self, item.key)
            Node.reparent(self, item.value)
        else:
            Node.reparent(item)
    def put(self, kvpair):
        self.reparent(kvpair)
        self.children.append(kvpair)
        self.invalidate()
    def __getitem__(self, k):
        self.refresh()
        return self.value[k]
    def __setitem__(self, k, v):
        self.put(KVPair(k, v))
    def reference_impl(self, key):
        self.refresh()
        return self.value[key]
    def __contains__(self, key):
        self.refresh()
        return key in self.value
    def eval(self):
        self.refresh()
        return self.value
    @property
    def modified(self):
        return self.value is None
    def invalidate(self):
        self.value = None
    def refresh(self):
        'Make sure the fully evaluated version of self is up-to-date'
        if self.modified:
            # rebuild self.value:
            self.value = simple.Map()
            for pair in self.children:
                self.value[eval_if_possible(pair.key)] = eval_if_possible(pair.value)
            
