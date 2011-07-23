from fern import primitives
import fern

class Map(dict):
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return primitives.Undefined
    def __setitem__(self, key, value):
        if value is primitives.Undefined:
            if key in self:
                del self[key]
        else:
            dict.__setitem__(self, key, value)

class List(list):
    def append(self, item):
        if not is_simple(item):
            raise fern.errors.TypeError('Only simple values in lists')
        list.append(self, item)

class AbstractCall(object):
    '''A call to a function that doesn't exist, for semantic purposes'''
    def __init__(self, name, *args):
        self.name = name
        self.args = args
    def __getitem__(self, index):
        return self.args[index]

class TreeNode(object):
    '''Like an XML element, only more flexible
    
    type is analogous to the tag name
    '''
    def __init__(self, type):
        self.type = type

def is_simple(item):
    return (primitives.is_primitive(item) or
            isinstance(item, (Map, List, AbstractCall, TreeNode)))

from primitives import Undefined, Nothing

def truthy(item):
    if not item or (item is Undefined) or (item is Nothing):
        return False
    return True
