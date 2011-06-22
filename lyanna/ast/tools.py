'''
Things used temporarily when processing parse trees.
'''

from node import Node
import lyanna

class ItemStream(list):
    def put(self, item):
        self.append(item)

def simplify(item):
    if isinstance(item, Node):
        return item.eval()
    elif lyanna.primitives.is_primitive(item):
        return item
    if hasattr(item, '__class__'):
        s = str(item.__class__)
    else:
        s = str(type(item))
    raise lyanna.errors.TypeError("can't simplify object of type %s" % s)