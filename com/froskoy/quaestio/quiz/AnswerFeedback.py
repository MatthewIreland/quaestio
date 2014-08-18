'''
Created on 17 Aug 2014

@author: matthew
'''

class AnswerFeedback(object):
    '''
    Object returned by the markAnswer method.
    '''


    def __init__(self, correct, feedback=None):
        '''
        Constructor.
        correct == 0 => answer is not correct
        correct >  0 => answer is correct
        feedback is optional and may be of type string, to be displayed to the user
        '''
        if (not isinstance(correct, int)):
            raise ValueError("Correct must be of type int: any non-zero value indicates a correct answer.")
        if ((feedback is not None) and (not isinstance(feedback, str))):
            raise ValueError("Answer feedback must be of type string.")
        self.__correct  = correct
        self.__feedback = feedback
        