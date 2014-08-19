'''
Created on 17 Aug 2014

@author: matthew
'''

import TrueFalseQuestion as TFQ
import MultipleChoiceQuestion as MCQ
import ShortAnswerQuestion as SAQ
from com.froskoy.quaestio.jsonSerializing.WrongQuestionTypeError import WrongQuestionTypeError

def map(questionType):
    if (questionType == TFQ.TrueFalseQuestion):
        return 'truefalse'
    if (questionType == MCQ.MultipleChoiceQuestion):
        return 'multiplechoice'
    if (questionType == SAQ.ShortAnswerQuestion):
        return 'shortanswer'
    raise WrongQuestionTypeError(questionType+" is not a supported question type.")
