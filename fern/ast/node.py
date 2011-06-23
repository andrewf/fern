from fern.primitives import Undefined
import tools

class Node(object):
    def __init__(self):
        self._parent = None
        self.value = None
        self.namebearing = False
    def reference(self, key):
        '''
        Looks up a name/key reference in either this scope
        or the containing one.
        
        Returns primitives.Undefined if name is not found
        '''
        if self.namebearing:
            item = self.reference_impl(key)
            if item is not Undefined: # we found the item
                return item
        # try the parent
        if self.parent is not None:
            return self.parent.reference(key)
        else: # with no parent, we're stuck
            return Undefined
    def reference_impl(self, key):
        '''
        Overridden by any class that can actually provide names. If name is
        not found return Undefined. Do not recur!
        '''
        return NotImplementedError(
            'Probably calling reference_impl on non-namebearing Node')
    # easy parent access
    def get_parent(self):
        return self._parent
    def set_parent(self, new_parent):
        # later, set flag and check for None
        self._parent = new_parent
    parent = property(get_parent, set_parent)
    def reparent(self, new_child):
        '''If new_child is a Node, sets its parent to self
        
        If it's not a node or ItemStream, presumably it's a primitive'''
        if isinstance(new_child, Node):
            new_child.parent = self
        elif isinstance(new_child, tools.ItemStream):
            for c in new_child:
                if isinstance(c,  Node):
                    c.parent = self
    # caching
    def get_modified(self):
        '''
        Whether the node is up-to-date or needs to be refreshed
        '''
        return self.value == None 
    def set_modified(self, b):
        '''
        Invalidate just this node.
        '''
        if b:
            self.value = None
        else:
            raise RuntimeError('you don\'t get to set node.modified to false')
    modified = property(get_modified, set_modified)
    def invalidate(self):
        '''
        Tell the node it will need to refresh before telling anyone its value
        '''
        if not self.modified: # prevent needless recursion
            self.modified = True
            if self._parent:
                self._parent.invalidate()
        if self.namebearing:
            self.invalidate_namerefs()
    def invalidate_namerefs(self):
        '''
        Invalidate all NameRef's that are children of this node
        '''
        def invalidate_if_nameref(n):
            if isinstance(n, Node):
                n.modified = True
        self.visit(invalidate_if_nameref)
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
