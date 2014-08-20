'''
Created on 16 Aug 2014

@author: matthew
'''

from Question import Question

import QuestionTypes
from ShortAnswerQuestionAnswer import ShortAnswerQuestionAnswer
from com.froskoy.quaestio.jsonSerializing.WrongQuestionTypeError import WrongQuestionTypeError

class ShortAnswerQuestion(Question):
    '''
    classdocs
    '''

    def __init__(self, questionText="", answers=[], name=None, feedback=None, hidden=0, usecase=0, jsonDict=None):
        '''
        Constructor
        '''
        if (jsonDict is None):
            super(ShortAnswerQuestion,self).__init__(questionText=questionText,name=name)
            self.__answers  = answers
            self.__feedback = feedback
            self.__hidden   = hidden
            self.__usecase  = usecase
        else:
            if (jsonDict['type'] != QuestionTypes.map(self.__class__)):
                raise WrongQuestionTypeError("Attempting to construct shortanswer question from dictionary whose type element is not set to shortanswer.")
            qName = jsonDict['name'] if (jsonDict['name'] != "") else None
            super(ShortAnswerQuestion,self).__init__(questionText=jsonDict['questiontext'],name=qName)
            
            self.__feedback = jsonDict['feedback'] if (jsonDict['feedback'] != "") else None
            self.__hidden   = jsonDict['hidden']
            self.__usecase  = jsonDict['usecase']
            
            self.__answers = map(lambda x : ShortAnswerQuestionAnswer(jsonDict=x), jsonDict['answers'])
                
    def toJsonDict(self):
        name = self._name if (self._name is not None) else ""
        return {'type'                     : QuestionTypes.map(self.__class__),
                'name'                     : name,
                'questiontext'             : self._questionText,
                'feedback'                 : self.__feedback if (self.__feedback is not None) else "",
                'hidden'                   : self.__hidden,
                'usecase'                  : self.__usecase,
                'answers'                  : map(lambda x : x.toJsonDict(), self.__answers)
               }
        
    def toGiftString(self):
        giftStr = super(ShortAnswerQuestion, self).toGiftString()
        giftStr += " { "
        for answer in self.__answers:
            giftStr += answer.toGiftString()
            giftStr += "\n"
        giftStr += "}"
        return giftStr
    
    def markAnswer(self, answer):
        raise NotImplementedError() 