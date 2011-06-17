from lyanna.tree.node import Node
from lyanna import simple
from lyanna.tree.tools import eval_if_possible

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
        return eval_if_possible(self.value[k])
    def __setitem__(self, k, v):
        self.put(KVPair(k, v))
    def reference_impl(self, key):
        return self.value[key]
    def __contains__(self, key):
        return key in self.value
    def eval(self):
        return self.value
