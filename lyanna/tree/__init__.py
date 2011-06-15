class Error(Exception):
    '''Semantic errors, regardless of syntax'''


class Node(object):
    pass

class KVPair(Node):
    def __init__(self, key, value):
        self.key = key
        self.value = value