'''
Created on 3 Apr 2016

@author: John Beard
'''

from mnem.mnem import MnemError


class CompletionError(MnemError):
    pass


class CompletionNotAvailableError(CompletionError):
    """Exception raised when a completion is not available
    """

    def __init__(self, completion):
        self.completion = completion

    def __str__(self):
        return self.completion

    def getCompletion(self):
        return self.completion

