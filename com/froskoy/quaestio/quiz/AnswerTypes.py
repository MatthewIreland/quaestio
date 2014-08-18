'''
Created on 18 Aug 2014

@author: matthew

Equivalent of QuestionTypes.py, for answers.
'''

import MultipleChoiceQuestionAnswer as MCQA
import ShortAnswerQuestionAnswer as SAQA

def map(answerType):
    if (answerType == MCQA.MultipleChoiceQuestionAnswer):
        return 'multiplechoicequestionanswer'
    if (answerType == SAQA.ShortAnswerQuestionAnswer):
        return 'shortanswerquestionanswer'
