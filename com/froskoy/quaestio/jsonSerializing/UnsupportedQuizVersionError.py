'''
Created on 17 Aug 2014

@author: matthew
'''

class UnsupportedQuizVersionError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
