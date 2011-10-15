'''
Things used temporarily when processing parse trees.
'''

import node
import fern
from fern.primitives import Nothing, Undefined

class ItemStream(list):
    def put(self, it):
        self.append(it)
    def map(self, fn):
        return ItemStream(map(fn, self))

def simplify_item(item):
    if isinstance(item, fern.ast.kvpair.KVPair):
        return item
    elif isinstance(item, node.Node):
        return item.eval()
    elif fern.primitives.is_primitive(item):
        return item
    if hasattr(item, '__class__'):
        s = str(item.__class__)
    else:
        s = str(type(item))
    raise fern.errors.TypeError("can't simplify object of type %s" % s)

def simplify(thing):
    if isinstance(thing, ItemStream):
        return thing.map(simplify)
    else:
        return simplify_item(thing)

def truthy(item):
    if not item or (item is Undefined) or (item is Nothing):
        return False
    return True
            
