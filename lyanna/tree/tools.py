'''
Things used temporarily when processing parse trees.
'''

class ItemStream(list):
    def put(self, item):
        self.append(item)
