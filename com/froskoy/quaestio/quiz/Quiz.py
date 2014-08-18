'''
Created on 16 Aug 2014

@author: matthew
'''

import json
from Question import Question
from TrueFalseQuestion import TrueFalseQuestion
from com.froskoy.quaestio.jsonSerializing.UnsupportedQuizVersionError import UnsupportedQuizVersionError
from com.froskoy.quaestio.jsonSerializing.UnsupportedQuestionTypeError import UnsupportedQuestionTypeError

class Quiz(object):
    '''
    classdocs
    '''
    __jsonReprVersion = 0.1


    def __init__(self, name="", description=None, jsonDict=None):
        '''
        Constructor
        '''
        
        if (jsonDict is not None):
            # TODO: worth running the dictionary through a validator here
            self.__base_id = 0
            self.__host_id = 0
            self.__version = 0
            self.__name = ""
            self.__description = ""
            self.__questions = []
            self.__createFromJsonDict(jsonDict)
        else:
            if (name == ""):
                raise ValueError("Quiz must have a name.")
            self.__base_id = 0
            self.__host_id = 0
            self.__version = 0
            self.__name = name
            self.__description = description
            self.__questions = []
        
        
    def addQuestion(self, question):
        if (isinstance(question, Question)):
            newQuestion = question
        elif (isinstance(question, dict)):
            # construct appropriate Question subclass based on type of question
            # types based on those supported by Moodle XML
            if (question['type'] == 'truefalse'):
                newQuestion = TrueFalseQuestion(jsonDict=question)
            elif (question['type'] == 'multichoice'):
                raise NotImplementedError()
            elif (question['type'] == 'shortanswer'):
                raise NotImplementedError()
            elif (question['type'] == 'matching'):
                raise NotImplementedError()
            elif (question['type'] == 'cloze'):
                raise NotImplementedError()
            elif (question['type'] == 'essay'):
                raise NotImplementedError()
            elif (question['type'] == 'numerical'):
                raise NotImplementedError()
            elif (question['type'] == 'description'):
                raise NotImplementedError()
            else:
                raise UnsupportedQuestionTypeError("Question type " + question['type'] + " is not recongised.")
        else:
            raise ValueError("Question must subclass Question or be of dictionary type.")
        self.__questions.append(newQuestion)
        
    def __toJsonDict(self):
        description = self.__description if (self.__description is not None) else ""
        return {'quizencodingversion' : self.__jsonReprVersion,
                'name'        : self.__name,
                'description' : description,
                'questions'   : map(lambda x : x.toJsonDict(), self.__questions)
               }        
        
    def __createFromJsonDict(self, quizDict):
        if (not isinstance(quizDict, dict)):
            # TODO: could do with running quizDict through a validator... again...
            raise ValueError("Must be called with a dictionary.")
        if (quizDict['quizencodingversion'] != self.__jsonReprVersion):
            raise UnsupportedQuizVersionError("Quiz JSON representation version "+str(self.__jsonReprVersion)+" is not supported.")
        self.__name = quizDict['name']
        self.__description = quizDict['description'] if (quizDict['description'] != "") else None 
        for questionDict in quizDict['questions']:
            self.addQuestion(questionDict)
    
    def jsonSerialize(self):
        return json.dumps(self.__toJsonDict())
    
