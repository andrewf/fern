from node import Node
from lyanna.primitives import Undefined

class NameRef(Node):
    '''
    Just a reference, delays lookup of name.
    '''
    def __init__(self, name):
        Node.__init__(self)
        self.name = name
#    def eval(self):
#        if self.parent is not None:
#            return self.parent.reference(self.name)
#        return Undefined
    def refresh_impl(self):
        if self.parent is not None:
            self.value = self.parent.reference(self.name)
        else:
            self.value = Undefined