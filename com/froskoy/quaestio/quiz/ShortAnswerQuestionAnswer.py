'''
Created on 18 Aug 2014

@author: matthew
'''

from Answer import Answer
import AnswerTypes
from com.froskoy.quaestio.jsonSerializing.WrongAnswerTypeError import WrongAnswerTypeError

class ShortAnswerQuestionAnswer(Answer):
    '''
    classdocs
    '''


    def __init__(self, text="", fraction=0, feedback=None, penalty=0, hidden=0, usecase=0, jsonDict=None):
        '''
        Constructor
        '''
        super(ShortAnswerQuestionAnswer,self).__init__()
        if (jsonDict is None):
            self._validateText(text)
            self._validateFraction(fraction)
        
            self.__text     = text
            self.__fraction = fraction
            self.__feedback = feedback
            self.__penalty  = penalty
            self.__hidden   = hidden
            self.__useCase  = usecase
        else:
            if (jsonDict['type'] != AnswerTypes.map(self.__class__)):
                raise WrongAnswerTypeError("Attempting to construct shortanswerquestion answer from dictionary whose type element is not set to shortanswerquestionanswer.")
            self.__text                = jsonDict['text']
            self.__fraction            = jsonDict['fraction']
            self.__feedback            = jsonDict['feedback'] if (jsonDict['feedback'] != "") else None
            self.__penalty             = jsonDict['penalty']
            self.__hidden              = jsonDict['hidden']
            self.__useCase             = jsonDict['usecase']
        
    def toJsonDict(self):
        return {'type'                : AnswerTypes.map(self.__class__),
                'text'                : self.__text,
                'fraction'            : self.__fraction,
                'feedback'            : self.__feedback if (self.__feedback is not None) else "",
                'penalty'             : self.__penalty,
                'hidden'              : self.__hidden,
                'usecase'             : self.__useCase }
        
    def toGiftString(self):
        """
        Note: Partial credit not yet supported.
        """
        giftStr = ""
        if (self.__fraction == 100): 
            giftStr = "="
        elif (self.__fraction == 0):
            giftStr = "~"
        else:
            raise NotImplementedError()
        giftStr += self.__text
        if (self.__feedback is not None):
            giftStr += " # "
            giftStr += self.__feedback
        return giftStr
        