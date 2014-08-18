'''
Created on 16 Aug 2014

@author: matthew

Issues: answer ordering (why not just have answers input as a list and add a shuffled option?)
'''

from Question import Question
from TrueFalseQuestionAnswer import TrueFalseQuestionAnswer
from com.froskoy.quaestio.jsonSerializing.WrongQuestionTypeError import WrongQuestionTypeError

class TrueFalseQuestion(Question):
    '''
    classdocs
    '''

    def __init__(self, questionText="", correctAnswer=None, wrongAnswer=None, name=None, jsonDict=None):
        '''
        Constructor
        '''
        if (jsonDict is None):
            super(TrueFalseQuestion,self).__init__(questionText=questionText,name=name)
            self.__answers = [correctAnswer, wrongAnswer]
        else:
            if (jsonDict['type'] != "truefalse"):
                raise WrongQuestionTypeError("Attempting to construct truefalse question from dictionary whose type element is not set to truefalse.")
            qName = jsonDict['name'] if (jsonDict['name'] != "") else None
            super(TrueFalseQuestion,self).__init__(questionText=jsonDict['questiontext'],name=qName)
            
            self.__answers = []
            for answer in jsonDict['answers']:
                self.__answers.append(TrueFalseQuestionAnswer(jsonDict=answer))
            assert(len(self.__answers) == 2)
        
    def toJsonDict(self):
        name = self._name if (self._name is not None) else ""
        return {'type'         : 'truefalse',
                'name'         : name,
                'questiontext' : self._questionText,
                'answers'      : map(lambda x : x.toJsonDict(), self.__answers)
               }
    
    def markAnswer(self):
        raise NotImplementedError() 