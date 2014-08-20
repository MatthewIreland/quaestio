'''
Created on 17 Aug 2014

@author: matthew
'''

from Answer import Answer
import AnswerTypes
from com.froskoy.quaestio.jsonSerializing.WrongAnswerTypeError import WrongAnswerTypeError

class MultipleChoiceQuestionAnswer(Answer):
    '''
    classdocs
    '''


    def __init__(self, text="", fraction=0, selectedFeedback=None, notSelectedFeedback=None, penalty=0, hidden=0, jsonDict=None):
        '''
        Constructor
        Selected feedback used as a "default" for generic feedback.
        fraction = 100 => a correct answer
        '''
        if (jsonDict is None):
            if (not isinstance(text, str)):
                raise ValueError("Question text must be of type string")
            if ((not isinstance(fraction, int)) | fraction<0 | fraction>100):
                raise ValueError("Correct must be of type int (between 0 and 100")
        
            self.__text     = text
            self.__fraction = fraction
            self.__selectedFeedback    = selectedFeedback
            self.__notSelectedFeedback = notSelectedFeedback
            self.__penalty             = penalty
            self.__hidden              = hidden
        else:
            if (jsonDict['type'] != AnswerTypes.map(self.__class__)):
                raise WrongAnswerTypeError("Attempting to construct multiplechoice answer from dictionary whose type element is not set to multiplechoicequestionanswer.")
            self.__text                = jsonDict['text']
            self.__fraction            = jsonDict['fraction']
            self.__penalty             = jsonDict['penalty']
            self.__hidden              = jsonDict['hidden']
            
            selectedFeedback           = jsonDict['selectedFeedback']
            notSelectedFeedback        = jsonDict['notSelectedFeedback']
            self.__selectedFeedback    = selectedFeedback if (selectedFeedback != "") else None
            self.__notSelectedFeedback = notSelectedFeedback if (notSelectedFeedback != "") else None

        
    def toJsonDict(self):
        selectedFeedback    = self.__selectedFeedback if (self.__selectedFeedback is not None) else ""
        notSelectedFeedback = self.__notSelectedFeedback if (self.__notSelectedFeedback is not None) else ""
        return {'type'                : AnswerTypes.map(self.__class__),
                'text'                : self.__text,
                'fraction'            : self.__fraction,
                'selectedFeedback'    : selectedFeedback,
                'notSelectedFeedback' : notSelectedFeedback,
                'penalty'             : self.__penalty,
                'hidden'              : self.__hidden}
        
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
        if (self.__selectedFeedback is not None):
            giftStr += " # "
            giftStr += self.__selectedFeedback
        return giftStr
        