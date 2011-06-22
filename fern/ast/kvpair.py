from node import Node

class KVPair(Node):
    def __init__(self, key, value):
        Node.__init__(self)
        self.key = key
        self.value = value
        self.outofdate = True
    def get_children(self):
        return [self._key, self._value]
    def setkey(self, k):
        self.reparent(k)
        self._key = k
    def getkey(self):
        return self._key
    key = property(getkey, setkey)
    def setvalue(self, v):
        self.reparent(v)
        self._value = v
    def getvalue(self):
        return self._value
    value = property(getvalue, setvalue)
    # Node interface stuff
    def refresh_impl(self):
        self._key.refresh()
        self._value.refresh()
    def get_modified(self):
        return self.outofdate
    def set_modified(self, b):
        if b:
            self.outofdate = True
        else:
            raise RuntimeError('do not set kvpair.modified = False')
    modified = property(get_modified, set_modified)
    def eval(self):
        raise NotImplementedError('Trying to call eval() on a KVPair, bad idea')
