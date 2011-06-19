from lyanna.primitives import Undefined


class Node(object):
    def __init__(self):
        self._parent = None
        self.value = None
    def reference(self, key):
        '''
        Looks up a name/key reference in either this scope
        or the containing one.
        
        Returns primitives.Undefined if name is not found
        '''
        item = self.reference_impl(key)
        if item is Undefined: # we can't find item
            if self.parent is not None:
                return self.parent.reference(key)
            else: # with no parent, we're stuck
                return Undefined
        else:
            return item
    def reference_impl(self, key):
        '''
        Overridden by any class that can actually provide names. If name is
        not found return Undefined. Do not recur!
        '''
        return Undefined
    # easy parent access
    def get_parent(self):
        return self._parent
    def set_parent(self, new_parent):
        # later, set flag and check for None
        self._parent = new_parent
    parent = property(get_parent, set_parent)
    def reparent(self, new_child):
        '''If new_child is a Node, sets its parent to self
        
        If it's not a node, presumably it's a primitive'''
        if isinstance(new_child, Node):
            new_child.parent = self
    # caching
    @property
    def modified(self):
        '''
        Returns whether the node's value is up-to-date or needs to be refreshed
        '''
        return self.value == None
    def children_modified(self):
        '''
        Check whether any of the node's children are modified.
        '''
        return False
    def invalidate(self):
        '''
        Tell the node it will need to refresh before telling anyone its value
        '''
        if self.value is not None: # prevent needless recursion
            self.value = None
            if self._parent:
                self._parent.invalidate()
    def refresh(self, skip=None):
        '''
        Makes sure self.value is up to date.
        '''
        if self.modified:
            self.refresh_impl()
    def refresh_impl(self):
        '''
        Called to rebuild self.value from scratch. Implementations may
        assume self.value is now None.
        '''
        raise NotImplementedError(
            'Trying to call refresh on Node without refresh_impl')
    def children_modified(self):
        '''
        Check whether any of the node's children are modified.
        '''
        return False
    def eval(self):
        '''
        Get an up-to-date version of self.value, the whole thing
        '''
        self.refresh()
        return self.value
    def visit(self, fun):
        'Recursively call fun on self and all children'
        for c in self.get_children():
            if isinstance(c, Node):
                c.visit(fun)
        fun(self)
    def get_children(self):
        'Get a list of all children of the node, in no particular order'
        return []
