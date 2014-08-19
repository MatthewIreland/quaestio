'''
Created on 17 Aug 2014

@author: matthew
'''

from Answer import Answer
import AnswerTypes
from com.froskoy.quaestio.jsonSerializing.WrongAnswerTypeError import WrongAnswerTypeError

class TrueFalseQuestionAnswer(Answer):
    '''
    classdocs
    '''


    def __init__(self, true=0, correct=0, feedback=None, penalty=0, hidden=0, jsonDict=None):
        '''
        Constructor
        '''
        if (jsonDict is None):
            if (not isinstance(true, int)):
                raise ValueError("'true' must be of type int (non-zero values indicate a true answer)")
            if (not isinstance(correct, int)):
                raise ValueError("'correct' must be of type int (non-zero values indicate a correct answer)")
        
            self.__true = true
            if (true == 0):
                self.__text = "false"
            else:
                self.__text = "true"
                self.__true = self.__true / self.__true

            if (correct == 0):
                self.__correct = correct
            else:
                self.__correct = correct/correct
            
            self.__feedback = feedback
            self.__penalty  = penalty
            self.__hidden   = hidden
        else:
            if (jsonDict['type'] != AnswerTypes.map(self.__class__)):
                raise WrongAnswerTypeError("Attempting to construct truefalse answer from dictionary whose type element is not set to truefalsequestionanswer.")
            self.__text     = jsonDict['text']
            self.__correct  = int(jsonDict['correct'])
            self.__feedback = jsonDict['feedback'] if (jsonDict['feedback'] != "") else None
            self.__penalty  = jsonDict['penalty']
            self.__hidden   = jsonDict['hidden']
            
            if   (self.__text == "true"):
                self.__true=1
            elif (self.__text == "false"):
                self.__true=0
            else:
                raise WrongAnswerTypeError("true/false question answer text must be equal to 'true' or 'false'")
        
    def toJsonDict(self):
        feedback = self.__feedback if (self.__feedback is not None) else ""
        return {'type'     : 'truefalsequestionanswer',
                'text'     : self.__text,
                'correct'  : self.__correct,
                'feedback' : feedback,
                'penalty'  : self.__penalty,
                'hidden'   : self.__hidden}
        
    def getFeedback(self):
        return self.__feedback
        
    def isTrue(self):
        return self.__true
    
    def isFalse(self):
        return (not self.__true)
    
    def isCorrect(self):
        return self.__correct
    
    def isIncorrect(self):
        return (not self.__correct)
    
    def isWrong(self):
        return (self.isIncorrect())
