'''
Things used temporarily when processing parse trees.
'''

import node
import fern

class ItemStream(list):
    def put(self, it):
        self.append(it)

def simplify(item):
    if isinstance(item, node.Node):
        return item.eval()
    elif fern.primitives.is_primitive(item):
        return item
    if hasattr(item, '__class__'):
        s = str(item.__class__)
    else:
        s = str(type(item))
    raise fern.errors.TypeError("can't simplify object of type %s" % s)
