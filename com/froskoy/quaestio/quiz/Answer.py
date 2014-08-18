'''
Created on 17 Aug 2014

@author: matthew
'''

from abc import ABCMeta, abstractmethod

class Answer(object):
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta

    def __init__(self, params):
        '''
        Constructor
        '''
        self.__base_id = 0
        self.__quiz_id = 0
        self.__question_id = 0
        self.__version = 0
        
    @abstractmethod
    def toJsonDict(self):
        pass
    
