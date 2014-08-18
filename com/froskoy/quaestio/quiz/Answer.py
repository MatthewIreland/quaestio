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

    def __init__(self):
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
    
    def _validateFraction(self, fraction):
        if ((not isinstance(fraction, int)) | fraction<0 | fraction>100):
            raise ValueError("Correct must be of type int (between 0 and 100")
        
    def _validateText(self, text):
        if (not isinstance(text, str)):
            raise ValueError("Question text must be of type string")