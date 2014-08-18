'''
Created on 17 Aug 2014

@author: matthew
'''

from Answer import Answer
from com.froskoy.quaestio.jsonSerializing.WrongAnswerTypeError import WrongAnswerTypeError

class TrueFalseQuestionAnswer(Answer):
    '''
    classdocs
    '''


    def __init__(self, text="", correct=0, feedback=None, penalty=0, hidden=0, jsonDict=None):
        '''
        Constructor
        '''
        if (jsonDict is None):
            if (not isinstance(text, str)):
                raise ValueError("Question text must be of type string")
            if (not isinstance(correct, int)):
                raise ValueError("Correct must be of type int (non-zero values indicate a correct answer)")
        
            self.__text = text
            if (correct == 0):
                self.__correct = correct
            else:
                self.__correct = correct/correct
            
            self.__feedback = feedback
            self.__penalty  = penalty
            self.__hidden   = hidden
        else:
            if (jsonDict['type'] != "truefalsequestionanswer"):
                raise WrongAnswerTypeError("Attempting to construct truefalse answer from dictionary whose type element is not set to truefalsequestionanswer.")
            self.__text     = jsonDict['text']
            self.__correct  = int(jsonDict['correct'])
            self.__feedback = jsonDict['feedback'] if (jsonDict['feedback'] != "") else None
            self.__penalty  = jsonDict['penalty']
            self.__hidden   = jsonDict['hidden']
        
    def toJsonDict(self):
        feedback = self.__feedback if (self.__feedback is not None) else ""
        return {'type'     : 'truefalsequestionanswer',
                'text'     : self.__text,
                'correct'  : self.__correct,
                'feedback' : feedback,
                'penalty'  : self.__penalty,
                'hidden'   : self.__hidden}
