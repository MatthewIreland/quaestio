'''
Created on 16 Aug 2014

@author: matthew
'''

from abc import ABCMeta, abstractmethod

class Question(object):
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
        self.__version = 0
        
    @abstractmethod
    def jsonSerialize(self):
        pass
    
    @abstractmethod
    def jsonDeserialize(self):
        pass
    
    @abstractmethod
    def markAnswer(self, answer):
        pass