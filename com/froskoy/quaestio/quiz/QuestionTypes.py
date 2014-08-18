'''
Created on 17 Aug 2014

@author: matthew
'''

import MultipleChoiceQuestion as MCQ
import ShortAnswerQuestion as SAQ

def map(questionType):
    if (questionType == MCQ.MultipleChoiceQuestion):
        return 'multiplechoice'
    if (questionType == SAQ.ShortAnswerQuestion):
        return 'shortanswer'
