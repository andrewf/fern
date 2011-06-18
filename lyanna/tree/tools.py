'''
Things used temporarily when processing parse trees.
'''

from node import Node

class ItemStream(list):
    def put(self, item):
        self.append(item)

def eval_if_possible(item):
    if hasattr(item, 'eval'):
        return item.eval()
    return item
