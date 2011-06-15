from lyanna import simple, errors

class Node(object):
    pass

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

class List(Node):
    def __init__(self, parent):
        self.children = []
    def put(self, item):
        self.children.append(item)
    def __getitem__(self, index):
        return self.children[index]

