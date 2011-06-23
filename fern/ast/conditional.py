from operator import itemgetter

from node import Node
from fern.primitives import Undefined
from fern.simple import truthy
from fern.ast.tools import simplify, ItemStream

class Conditional(Node):
    '''
    A conditional statement, if/elif/else
    '''
    def __init__(self):
        Node.__init__(self)
        self.conditions = []
        self._else = Undefined
    def set_else(self, val):
        self._else = val
        self.reparent(val)
        self.invalidate()
    def get_else(self):
        return self._else
    else_val = property(get_else, set_else)
    def put_cond(self, cond, val):
        self.reparent(cond)
        self.reparent(val)
        self.conditions.append((cond, val))
        self.invalidate()
    def refresh_impl(self):
        for c in self.conditions:
            if truthy(simplify(c[0])):
                if isinstance(c[1], ItemStream):
                    self.value = c[1]
                else:
                    self.value = simplify(c[1])
                return
        self.value = simplify(self.else_val)
    def get_children(self):
        return (map(itemgetter(0), self.conditions) +
                map(itemgetter(1), self.conditions) +
                [self.else_val])
