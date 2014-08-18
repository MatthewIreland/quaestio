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

    def __init__(self, questionText="", name=None):
        '''
        Constructor
        '''
        self.__base_id = 0
        self.__quiz_id = 0
        self.__version = 0
        self._name = name
        self._questionText = questionText
        
    @abstractmethod
    def toJsonDict(self):
        pass
    
    @abstractmethod
    def markAnswer(self, answer):
        pass
        
    def _validateText(self, text):
        if (not isinstance(text, str)):
            raise ValueError("Question text must be of type string")