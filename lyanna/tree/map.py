from lyanna.tree.node import Node
from lyanna import simple

class KVPair(Node):
    def __init__(self, key, value):
        Node.__init__(self)
        self.key = key
        self.value = value
        self.reparent(self.key)
        self.reparent(self.value)
        

class Map(Node):
    def __init__(self):
        Node.__init__(self)
        self.children = []
        self.value = simple.Map()
    def put(self, kvpair):
        self.reparent(kvpair)
        self.children.append(kvpair)
        self.value[kvpair.key] = kvpair.value
    def __getitem__(self, k):
        return self.value[k]
    def __setitem__(self, k, v):
        self.put(KVPair(k, v))
    def reference_impl(self, key):
        return self.value[key]
