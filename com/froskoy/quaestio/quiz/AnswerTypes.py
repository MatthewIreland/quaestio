'''
Created on 18 Aug 2014

@author: matthew

Equivalent of QuestionTypes.py, for answers.
'''

import TrueFalseQuestionAnswer as TFQA
import MultipleChoiceQuestionAnswer as MCQA
import ShortAnswerQuestionAnswer as SAQA
from com.froskoy.quaestio.jsonSerializing.WrongAnswerTypeError import WrongAnswerTypeError

def map(answerType):
    if (answerType == TFQA.TrueFalseQuestionAnswer):
        return 'truefalsequestionanswer'
    if (answerType == MCQA.MultipleChoiceQuestionAnswer):
        return 'multiplechoicequestionanswer'
    if (answerType == SAQA.ShortAnswerQuestionAnswer):
        return 'shortanswerquestionanswer'
    raise WrongAnswerTypeError(answerType+" is not a supported answer type.")
