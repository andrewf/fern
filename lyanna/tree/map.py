from lyanna.tree.node import Node
from lyanna import simple

class KVPair(Node):
    def __init__(self, parent, key, value):
        self.parent = parent
        self.key = key
        self.value = value

class Map(Node):
    def __init__(self, parent):
        self.parent = parent
        self.children = []
        self.value = simple.Map()
    def put(self, kvpair):
        self.children.append(kvpair)
        self.value[kvpair.key] = kvpair.value
    def __getitem__(self, k):
        return self.value[k]
    def __setitem__(self, k, v):
        self.put(KVPair(self, k, v))
