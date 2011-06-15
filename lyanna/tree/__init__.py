from lyanna import simple

class Error(Exception):
    '''Semantic errors, regardless of syntax'''


class Node(object):
    pass

class KVPair(Node):
    def __init__(self, key, value):
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
        