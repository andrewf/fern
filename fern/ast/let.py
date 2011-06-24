from node import Node
from map import Map
from list import List
from tools import ItemStream, simplify

class Let(Node):
    def __init__(self):
        Node.__init__(self)
        self.namebearing = True
        self.names = Map()
        self.content = None
    def put(self, item):
        # self.content should be None if there is no content
        # one item, or an ItemStream if there is more than one item
        self.reparent(item)
        if self.content is None:
            self.content = item
        elif isinstance(self.content, ItemStream):
            self.content.put(item)
        else:
            self.content = ItemStream([self.content, item])
    def reference_impl(self, key):
        return self.names.reference_impl(key)
    def refresh_impl(self):
        self.value = simplify(self.content)
