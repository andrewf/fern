from node import Node
from fern.primitives import Undefined

class NameRef(Node):
    '''
    Just a reference, delays lookup of name.
    '''
    def __init__(self, name):
        Node.__init__(self)
        self.name = name
    def refresh_impl(self):
        if self.parent is not None:
            self.value = self.parent.reference(self.name)
        else:
            self.value = Undefined