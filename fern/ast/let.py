from node import Node
from map import Map
from list import List
from tools import ItemStream, simplify

class Let(Node):
    def __init__(self):
        Node.__init__(self)
        self.namebearing = True
        self._names = Map()
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
    def get_names(self):
        return self._names
    def set_names(self, newnames):
        if not newnames.namebearing:
            raise fern.errors.ValueError(
                    'trying to set non-namebearing Node as names for Let')
        self.reparent(newnames)
        self._names = newnames
    names = property(get_names, set_names)
