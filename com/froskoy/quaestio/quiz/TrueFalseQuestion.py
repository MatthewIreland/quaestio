'''
Created on 16 Aug 2014

@author: matthew

Issues: answer ordering (why not just have answers input as a list and add a shuffled option?)
'''

from Question import Question
import QuestionTypes
from TrueFalseQuestionAnswer import TrueFalseQuestionAnswer
from com.froskoy.quaestio.jsonSerializing.WrongQuestionTypeError import WrongQuestionTypeError
from com.froskoy.quaestio.jsonSerializing.JsonError import JsonError

class TrueFalseQuestion(Question):
    '''
    classdocs
    '''

    def __init__(self, questionText="", isTrue=0, correctFeedback=None, incorrectFeedback=None, name=None, jsonDict=None):
        '''
        Constructor
        '''
        if (jsonDict is None):
            super(TrueFalseQuestion,self).__init__(questionText=questionText,name=name)
            self.__isTrue=isTrue
            self.__correctAnswerFeedback = correctFeedback
            self.__wrongAnswerFeedback   = incorrectFeedback
            
            # self.__answers is *ONLY* used in converting to/from a json dict
            if (isTrue):
                correctAnswer   = TrueFalseQuestionAnswer(true=1, correct=1, feedback=correctFeedback,   penalty=0, hidden=0)
                incorrectAnswer = TrueFalseQuestionAnswer(true=0, correct=0, feedback=incorrectFeedback, penalty=0, hidden=0)
            else:
                correctAnswer   = TrueFalseQuestionAnswer(true=0, correct=1, feedback=correctFeedback,   penalty=0, hidden=0)
                incorrectAnswer = TrueFalseQuestionAnswer(true=1, correct=0, feedback=incorrectFeedback, penalty=0, hidden=0)
            self.__answers = [correctAnswer, incorrectAnswer]

        else:
            if (jsonDict['type'] != QuestionTypes.map(self.__class__)):
                raise WrongQuestionTypeError("Attempting to construct truefalse question from dictionary whose type element is not set to truefalse.")
            qName = jsonDict['name'] if (jsonDict['name'] != "") else None
            super(TrueFalseQuestion,self).__init__(questionText=jsonDict['questiontext'],name=qName)
            
            # self.__answers is *ONLY* used in converting to/from a json dict
            self.__answers = []
            for answer in jsonDict['answers']:
                answer = TrueFalseQuestionAnswer(jsonDict=answer)
                if (answer.isCorrect()):
                    self.__correctAnswerFeedback = answer.getFeedback()
                    if (answer.isTrue()):
                        self.__isTrue=1
                    else:
                        self.__isTrue=0
                elif (answer.isWrong()):
                    self.__incorrectAnswerFeedback = answer.getFeedback()
                else:
                    raise JsonError("answer is neither correct nor incorrect... something's gone wrong")
                self.__answers.append(answer)
            assert(len(self.__answers) == 2)
        
    def toJsonDict(self):
        name = self._name if (self._name is not None) else ""
        return {'type'         : 'truefalse',
                'name'         : name,
                'questiontext' : self._questionText,
                'answers'      : map(lambda x : x.toJsonDict(), self.__answers)
               }
        
    def toGiftString(self):
        """
        Note: current GIFT representation does not allow for feedback
              or partial credit.
        """
        giftStr = super(TrueFalseQuestion, self).toGiftString()
        giftStr += " {"
        if (self.__isTrue):
            giftStr += "T"
        else:
            giftStr += "F"
        giftStr += "}"
        return giftStr
            
    
    def markAnswer(self, answer):
        raise NotImplementedError() 