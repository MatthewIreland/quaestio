'''
Created on 20 Aug 2014

@author: matthew
'''

class GiftParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
