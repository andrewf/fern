import lyanna
from lyanna.ast.kvpair import KVPair
from lyanna.parser.errors import BuilderError

class Builder(object):
    pass

class NameDeclBuilder(Builder):
    def __init__(self):
        self.decl = None
    def put(self, item):
        if self.decl is None:
            self.decl = item
        else:
            raise BuilderError('put too many objects in NameDeclBuilder')
    def get(self):
        if self.decl:
            return self.decl
        else:
            raise BuilderError('didn\'t put any objects in NameDecl')

class KVPairBuilder(Builder):
    def __init__(self):
        self.expecting = 'key'
        self.key = None
        self.pair = None
    def put(self, item):
        if self.expecting == 'key':
            self.key = item
            self.expecting = 'value'
        elif self.expecting == 'value':
            self.pair = KVPair(self.key, item)
            self.expecting = None
        else:
            raise BuilderError('put too many objects in KVPairBuilder')
    def get(self):
        if self.pair is None:
            raise BuilderError("didn't put enough objects in KVPairBuilder")
        return self.pair

class ParseStack(object):
    def __init__(self):
        self.stack = []
    # stack ops
    def get_top(self):
        "The top item on the stack"
        if self.stack:
            return self.stack[-1]
        return None
    def set_top(self, item):
        if self.stack:
            self.stack[-1] = item
        else:
            self.stack.append(item)
    top = property(get_top, set_top)
    def pop(self):
        return self.stack.pop()
    def start_kvpair(self):
        self.stack.append(KVPairBuilder())
    def start_namedecl(self):
        self.stack.append(NameDeclBuilder())
    def start_map(self):
        self.stack.append(lyanna.ast.Map())
    def start_list(self):
        self.stack.append(lyanna.ast.List())
    def finish_item(self):
        if len(self.stack) > 1:
            it = self.stack.pop()
            if isinstance(it, KVPairBuilder):
                self.top.put(it.get())
            else:
                self.top.put(it)
        # if there's only one item, nothing to do
    def put(self, item):
        "Insert the item in the current top item"
        if self.top:
            self.top.put(item) # top had better have a put method
        else:
            self.stack.append(item)
    def push(self, item):
        '''New stack entry
        
        Use in places where start_* is overkill. Be sure to either call
        finish_item eventually or otherwise handle the object (for ex.,
        replacing it with another)
        '''
        self.stack.append(item)
