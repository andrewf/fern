import fern

class Error(fern.errors.Error):
    '''Parser Error'''

class BuilderError(Error):
    '''Builder Error'''

class SyntaxError(Error):
    pass