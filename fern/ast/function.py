from node import Node
from let import Let
from copy import deepcopy as copy
from map import Map, KVPair
from tools import ItemStream
import fern

class Function(Node):
    def __init__(self, child, args=None):
        Node.__init__(self)
        self.child = child
        self.reparent(child)
        self.args = args or []
    def call(self, *args):
        '''evaluate the content of the function with the passed args
        mapped to the function's args. returns simplified object'''
        # create a scope for the call 
        call_scope = Let()
        if self.parent:
            self.parent.reparent(call_scope) # to make lexical scope work
        call_scope.put(copy(self.child))
        # load args into the call's scope
        arg_map = Map()
        if len(self.args) != len(args):
            raise fern.errors.SemanticError('calling function with %d arguments, should be %d' % (len(args), len(self.args)))
        for k, v in zip(self.args, args):
            arg_map.put(KVPair(k, v))
        call_scope.names = arg_map
        return call_scope.eval()
    def refresh_impl(self):
        # evaluates to itself, necessary, for being referred to by NameRef's
        self.value = self

class FunctionCall(Node):
    def __init__(self, fun, args=None):
        # fun can be any node that evaluates to a function
        Node.__init__(self)
        self.fun = fun
        self.reparent(fun)
        self.args = args or ItemStream()
    def refresh_impl(self):
        f = self.fun.eval()
        if not isinstance(f, Function):
            raise fern.errors.TypeError('trying to call a non-function')
        self.value = f.call(*self.args)
