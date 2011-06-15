'''
This file contains any primitives for Lyanna that aren't just
borrowed from the language. Basically this is Nothing and Undefined,
which are singletons. That is, their classes are stuck here and only
selected instances are exported through __all__
'''

class NothingType(object):
    def __str__(self):
        return "Nothing"

class UndefinedType(object):
    def __str__(self):
        return "Undefined"

Nothing = NothingType()
Undefined = UndefinedType()

__all__ = ['Nothing', 'Undefined']


