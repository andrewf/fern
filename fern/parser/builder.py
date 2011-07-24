import fern
from fern.ast.kvpair import KVPair
from fern.parser.errors import BuilderError
from fern.ast.conditional import Conditional
from fern.ast.let import Let
from fern.ast.function import Function, FunctionCall
from fern.ast.tools import ItemStream

class Builder(object):
    "semantic class, just a marker for RTTI"

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

class CondBuilder(Builder):
    def __init__(self):
        self.conditional = Conditional()
        self.curr_cond = None # if not None, expecting a value
        self.expecting_else = False
    def put(self, item):
        if self.expecting_else:
            self.conditional.else_val = item
            self.expecting_else = False
        elif self.curr_cond is None:
            self.curr_cond = item
        else:
            self.conditional.put_cond(self.curr_cond, item)
            self.curr_cond = None
    def else_coming(self):
        self.expecting_else = True
    def get(self):
        return self.conditional

class LetBuilder(Builder):
    def __init__(self):
        self.expecting = 'names'
        self.let = Let()
    def put(self, item):
        if self.expecting == 'names':
            self.let.names.put(item)
        else:
            self.let.put(item)
    def start_content(self):
        self.expecting = 'content'
    def get(self):
        return self.let
        

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

class FunctionBuilder(Builder):
    def __init__(self):
        self.expecting = 'params'
        self.params = []
        self.fun = None
    def start_content(self):
        self.expecting = 'body'
    def put(self, item):
        if self.expecting == 'params':
            self.params.append(item) # assuming it's a string...
        elif self.expecting == 'body':
            self.fun = Function(item, self.params)
            self.expecting = None
        else:
            raise BuilderError('put stuff in Function after it has a body')
    def get(self):
        if self.fun is None:
            raise BuilderError('didn\'t finish building Function')
        return self.fun

class FCallBuilder(Builder):
    def __init__(self):
        self.expecting = 'func'
        self.func = None
        self.args = ItemStream()
    def put(self, item):
        if self.expecting == 'func':
            self.func = item
            self.expecting = 'params'
        else:
            self.args.put(item)
    def get(self):
        return FunctionCall(self.func, self.args)    

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
        self.stack.append(fern.ast.Map())
    def start_list(self):
        self.stack.append(fern.ast.List())
    def start_itemstream(self):
        # careful, ItemStream is not a Node
        self.stack.append(fern.ast.tools.ItemStream())
    def start_conditional(self):
        self.stack.append(CondBuilder())
    def start_let(self):
        self.stack.append(LetBuilder())
    def start_function(self):
        self.stack.append(FunctionBuilder())
    def start_fcall(self):
        self.stack.append(FCallBuilder())
    def finish_item(self):
        if len(self.stack) > 1:
            it = self.stack.pop()
            if isinstance(it, Builder):
                self.top.put(it.get())
            else:
                self.top.put(it)
        # if there's only one item, nothing to do
    def put(self, item):
        "Insert the item in the current top item"
        if self.top is not None: # check None in case self.top evals to False
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
