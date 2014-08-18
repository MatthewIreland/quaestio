'''
Created on 16 Aug 2014

@author: matthew
'''

from Question import Question
import QuestionTypes
from MultipleChoiceQuestionAnswer import MultipleChoiceQuestionAnswer
from com.froskoy.quaestio.jsonSerializing.WrongQuestionTypeError import WrongQuestionTypeError

class UnsupportedAnswerNumberingError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MultipleChoiceQuestion(Question):
    '''
    classdocs
    '''

    def __init__(self, questionText="", answers=[], name=None, single=None, shuffleAnswers=0, correctFeedback=None, partiallyCorrectFeedback=None, incorrectFeedback=None, answerNumbering="none", jsonDict=None):
        '''
        Constructor
        Allowed values of answer numbering: 'none', 'abc', 'ABCD' or '123'
        '''
        if (jsonDict is None):
            super(MultipleChoiceQuestion,self).__init__(questionText=questionText,name=name)
            self.__answers                  = answers
            self.__single                   = single
            self.__shuffleAnswers           = shuffleAnswers
            self.__correctFeedback          = correctFeedback
            self.__partiallyCorrectFeedback = partiallyCorrectFeedback
            self.__incorrectFeedback        = incorrectFeedback
            self.__answerNumbering          = self.__validateAnswerNumbering(answerNumbering)
        else:
            if (jsonDict['type'] != QuestionTypes.map(self.__class__)):
                raise WrongQuestionTypeError("Attempting to construct multiplechoice question from dictionary whose type element is not set to multiplechoice.")
            qName = jsonDict['name'] if (jsonDict['name'] != "") else None
            super(MultipleChoiceQuestion,self).__init__(questionText=jsonDict['questiontext'],name=qName)
            
            self.__single = jsonDict['single']
            self.__shuffleAnswers = jsonDict['shuffleAnswers']
            self.__correctFeedback = jsonDict['correctFeedback']
            self.__partiallyCorrectFeedback = jsonDict['partiallyCorrectFeedback']
            self.__incorrectFeedback = jsonDict['incorrectFeedback']
            self.__answerNumbering = self.__validateAnswerNumbering(jsonDict['answerNumbering'])
            
            self.__answers = []
            for answer in jsonDict['answers']:
                self.__answers.append(MultipleChoiceQuestionAnswer(jsonDict=answer))
                
    def toJsonDict(self):
        name = self._name if (self._name is not None) else ""
        return {'type'                     : QuestionTypes.map(self.__class__),
                'name'                     : name,
                'questiontext'             : self._questionText,
                'single'                   : self.__single,
                'shuffleAnswers'           : self.__shuffleAnswers,
                'correctFeedback'          : self.__correctFeedback,
                'partiallyCorrectFeedback' : self.__partiallyCorrectFeedback,
                'incorrectFeedback'        : self.__incorrectFeedback,
                'answerNumbering'          : self.__answerNumbering,
                'answers'                  : map(lambda x : x.toJsonDict(), self.__answers)
               }
    
    def markAnswer(self):
        raise NotImplementedError() 

    def __validateAnswerNumbering(self, answerNumbering):
        if (not answerNumbering in ['none', 'abc', 'ABCD', '123']):
            raise UnsupportedAnswerNumberingError(answerNumbering+" is not a valid answer numbering scheme.")
        return answerNumbering