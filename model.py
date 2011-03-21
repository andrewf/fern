'''
Defines the syntax-agnostic data model of Lyanna.
'''

from copy import deepcopy as copy


class IdKey(tuple):
    '''
    Wrap a mutable object in this to allow it to be used as a dict key.
    Compares by identity.'''
    def __new__(cls, obj):
        return tuple.__new__(cls, (obj,))

class Scope(object):
    '''
    stub object that behaves like a scope: looks up names,
    or defers to the outer scope. Override reference with custom lookup logic,
    and be sure to call parent if you can't find it'''
    def __init__(self, outer):
        self.scope = outer
    def reference(self, key):
        if self.scope:
            return self.scope.reference(key)
        else:
            raise ValueError('invalid reference key ' + str(key))
            

class KVPair(object):
    '''
    Just for building
    '''
    def __init__(self):
        self.has_key = False
    def put(self, item):
        if not self.has_key:
            self.key = item
            self.has_key = True
        else:
            self.value = item

class Map(Scope):
    '''
    A wrapper for dict that allows Map's and List's as keys.

    When used as keys
    '''
    def __init__(self, scope):
        Scope.__init__(self, scope)
        self.d = {}
    def __len__(self):
        return len(self.d)
    def __getitem__(self, k):
        item = self.d[hashable_key(k)]
        if isinstance(item, NameReference):
            return item.get()
        return item
    def __setitem__(self, k, v):
        self.d[hashable_key(k)] = v
    def put(self, kvpair):
        assert(isinstance(kvpair, KVPair))
        self[kvpair.key] = kvpair.value
    def reference(self, key):
        if key in self:
            return self[key]
        else:
            return Scope.reference(self, key)
    def __contains__(self, item):
        return hashable_key(item) in self.d

class List(Scope):
    def __init__(self, scope):
        Scope.__init__(self, scope)
        self.l = []
    def __len__(self):
        return len(self.l)
    def __getitem__(self, k):
        item = self.l[k]
        if isinstance(item, NameReference):
            return item.get()
        return item
    def __setitem__(self, k, v):
        self.d[k] = v
    def put(self, v):
        self.l.append(v)

class NameReference(object):
    '''
    A key reference actually. Delays name/key lookup until a context is available.
    May also be a function call
    '''
    def __init__(self, scope):
        self.name = None
        self.scope = scope
        self.expecting = 'name'
        self.params = None
    def put(self, item):
        if self.expecting == 'name':
            self.name = item
            self.expecting = 'params'
        elif self.expecting == 'params':
            self.params.append(item)
    def start_params(self):
        self.expecting = 'params'
        self.params = []
    def get(self):
        it = self.scope.reference(self.name)
        if self.params is not None:
            if isinstance(it, Function):
                it = it.call(*self.params)
            else:
                raise ValueError('trying to call non-function')
        # in case this ref points to another ref...
        if isinstance(it, NameReference):
            it = it.get()
        return it

class IfGenerator(object):
    def __init__(self):
        self.conds = []
        self.else_value = None
        self.expecting = 'cond' # cond | value | else
        self.current = None # a condition if self.expecting == 'value'
    def put(self, item):
        if self.expecting == 'cond':
            self.current = item
            self.expecting = 'value'
        elif self.expecting == 'value':
            self.conds.append((self.current, item))
            self.expecting = 'cond'
        elif self.expecting == 'else':
            self.expecting = None # seriously, no more
            self.else_value = item
        else:
            raise ValueError('trying to add to full if')
    def start_else(self):
        self.expecting = 'else'
    def get(self):
        for cond in self.conds:
            if self.istrue(cond[0]):
                return cond[1]
        if self.else_value is not None:
            return self.else_value
        else:
            raise ValueError('no else value in if')
    def istrue(self, item):
        if isinstance(item, NameReference):
            return bool(item.get())
        return bool(item)

class Function(object):
    def __init__(self, scope):
        self.expecting = 'params' # params | value | None
        self.params = []
        self.value = None
        self.scope = scope # definition scope
    def put(self, item):
        if self.expecting == 'params':
            self.params.append(item)
        elif self.expecting == 'value':
            self.value = item
            self.expecting = None
        else:
            raise ValueError('trying to add item to full function')
    def end_params(self):
        self.expecting = 'value'
    def call(self, *params):
        namedparams = dict(zip(self.params, params))
        invocation_scope = Map(self.scope)
        invocation_scope.d = namedparams
        result = copy(self.value)
        if isinstance(self.value, (Map, List, NameReference)):
            result.scope = invocation_scope
        return result

def hashable_key(obj):
    'Makes sure the obj is hashable, wrapping in IdKey if needed'
    # actually, it's not that picky. Just makes sure to wrap Map and List
    if isinstance(obj, (Map, List)):
        return IdKey(obj)
    else:
        return obj
