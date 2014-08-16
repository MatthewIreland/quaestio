'''
Created on 16 Aug 2014

@author: matthew
'''

from Question import Question

class NumericQuestion(Question):
    '''
    Answers can take the form of a range, or multiple possibilities with partical credit and feedback
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        