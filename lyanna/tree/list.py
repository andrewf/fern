from node import Node
from lyanna import simple
from lyanna.tree.tools import eval_if_possible

class List(Node):
    def __init__(self):
        Node.__init__(self)
        self.children = []
        self.value = None
    def put(self, item):
        self.reparent(item)
        self.children.append(item)
        self.invalidate()
    def __getitem__(self, index):
        self.refresh()
        return self.children[index]
    def refresh_impl(self):
        self.value = simple.List()
        for item in self.children:
            self.value.append(eval_if_possible(item))
            
