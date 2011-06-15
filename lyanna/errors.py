'''
Exception classes to be used throughout Lyanna
'''

class Error(Exception):
    '''Basic Lyanna Error'''

class SemanticError(Error):
    '''Syntax-agnostic error'''

class KeyError(SemanticError):
    '''Invalid key reference'''

class TypeError(SemanticError):
    '''When objects get put where they don't belong'''