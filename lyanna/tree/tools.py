'''
Things used temporarily when processing parse trees.
'''

from node import Node

class ItemStream(list):
    def put(self, item):
        self.append(item)

class KVPair(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

def eval_if_possible(item):
    if hasattr(item, 'eval'):
        return item.eval()
    return item
