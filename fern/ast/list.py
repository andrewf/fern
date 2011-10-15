from node import Node
from fern.ast.tools import simplify, ItemStream
from fern.primitives import Undefined

class List(Node):
    def __init__(self):
        Node.__init__(self)
        self.children = []
        self.value = None
    def put(self, thingy):
        if isinstance(thingy, ItemStream):
            for it in thingy:
                self.put_item(it)
        else:
            self.put_item(thingy)
    def put_item(self, item):
        if not item is Undefined:
            self.reparent(item)
            self.children.append(item)
            self.invalidate()
    def __getitem__(self, index):
        self.refresh()
        return self.value[index]
    def refresh_impl(self):
        self.value = []
        for child in self.children:
            result = simplify(child)
            if isinstance(result, ItemStream):
                for it in result:
                    self.value.append(it)
            else:
                self.value.append(result)
    def get_children(self):
        return self.children
