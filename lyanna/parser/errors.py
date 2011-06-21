import lyanna

class Error(lyanna.errors.Error):
    '''Parser Error'''

class BuilderError(Error):
    '''Builder Error'''

class SyntaxError(Error):
    pass