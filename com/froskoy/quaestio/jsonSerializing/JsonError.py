'''
Created on 18 Aug 2014

@author: matthew

All exceptions in this package should inherit from this.
'''

class JsonError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)