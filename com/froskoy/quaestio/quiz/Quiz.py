'''
Created on 16 Aug 2014

@author: matthew
'''

class Quiz(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.__base_id = 0
        self.__host_id = 0
        self.__version = 0
        self.__questions = []
        
        
    def addQuestion(self, question):
        self.__questions.append(question)
        
    def jsonSerialize(self):
        raise NotImplementedError()
    
    def jsonDeserialize(self):
        raise NotImplementedError()