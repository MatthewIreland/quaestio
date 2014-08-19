'''
Created on 16 Aug 2014

@author: matthew
'''

import ply.yacc as yacc
import GiftLexer
from com.froskoy.quaestio.quiz.Quiz import Quiz
from com.froskoy.quaestio.quiz.TrueFalseQuestion import TrueFalseQuestion
from com.froskoy.quaestio.quiz.TrueFalseQuestionAnswer import TrueFalseQuestionAnswer
from GiftLexer import tokens

##### DEFINITION OF GLOBALS
__MODE_DEBUG__ = 1
questionName = None
questions = []
##### END DEFINITION OF GLOBALS

##### Internal class and method definitions (need moving to separate files)
class InvalidQuestionBodyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidTrueFalseQuestionAnswer(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ParserTrueFalseQuestionBody:
    def __init__(self, text, answer):
        self.text   = text
        if ((answer!="TRUE") & (answer!="T") & (answer!="FALSE") & (answer!="F")):
            if (answer is not None):
                excpStr = answer + " is not a valid answer for a TRUE/FALSE question."
            else:
                excpStr = "Answer cannot be none!"
            raise InvalidTrueFalseQuestionAnswer(excpStr)
        else:
            self.answer = answer
        self.correct = ((self.answer == "TRUE") | (self.answer == "T"))

def parserAddQuestion(question):
    print "Adding question!!!"
    questions.append(question)
        
def parserConstructQuestion(name=None, questionBody=None):
    if (questionBody is None):
        raise InvalidQuestionBodyError("Question body must not be None!")
    print name
    if (questionBody.__class__ == ParserTrueFalseQuestionBody):
        return TrueFalseQuestion(questionText=questionBody.text,
                                 isTrue=questionBody.correct,
                                 correctFeedback=None,
                                 incorrectFeedback=None,
                                 name=name)
    raise ValueError("question class unrecognised")

##### End Internal class and method definitions


##### PARSING RULES
# quiz and quizbody
def p_quiz(p):
    'quiz : quizbody'
    print "Adding quiz!"
    p[0]=Quiz(name="A quiz converted from GIFT", description="The quiz has been converted from GIFT format")
    for question in questions:        # TODO move questions from global variable into quizbody, that is, p[1]
        p[0].addQuestion(question)
    
def p_quizbody_rec(p):
    'quizbody : question linegap quizbody'
    #parserAddQuestion(p[1])   # TODO why can't I add the question here instead of at the end of question production?
    pass
    
def p_quizbody(p):
    'quizbody : question linegap'
    #parserAddQuestion(p[1])   # TODO why can't I add the question here instead of at the end of question production?
    pass

# questions and answers
def p_question_withname(p):
    'question : questionname optionalwhitespace questionbody'
    questionName = p[1]
    p[0] = parserConstructQuestion(name=questionName,questionBody=p[3])
    if __MODE_DEBUG__:
        print "Question name: " + questionName
    parserAddQuestion(p[0])
    
def p_question_noname(p):
    'question : questionbody'
    p[0] = parserConstructQuestion(questionBody=p[1])
    if __MODE_DEBUG__:
        print "Question has no name." 
    parserAddQuestion(p[0])
        
def p_questionname(p):
    'questionname : QTITLEMARKER optionalwhitespace string optionalwhitespace QTITLEMARKER' 
    p[0] = p[3]

def p_questionbody_truefalse(p):
    'questionbody : truefalsequestionbody'
    p[0] = p[1]

"""    
def p_questionbody_multiplechoice(p):
    'questionbody : multiplechoicequestionbody'
    
def p_questionbody_shortanswer(p):
    'questionbody : shortanswerquestionbody'
    
def p_questionbody_missingword(p):
    'questionbody : missingwordquestionbody'
    
def p_questionbody_matching(p):
    'questionbody : matchingquestionbody'
    
def p_questionbody_numeric(p):
    'questionbody : numericquestionbody'
    
def p_questionbody_essay(p):
    'questionbody : essayquestionbody'
"""

## truefalse question
def p_truefalsequestionbody(p):
    'truefalsequestionbody : string optionalwhitespace ANSWEROPEN optionalwhitespace WORD optionalwhitespace ANSWERCLOSE'
    if __MODE_DEBUG__:
        print "True/false question answer: " + p[5]
    p[0] = ParserTrueFalseQuestionBody(text=p[1], answer=p[5])

def p_truefalsequestionbody_leadingtextnumeral(p):
    'truefalsequestionbody : NUMERIC string optionalwhitespace ANSWEROPEN optionalwhitespace WORD optionalwhitespace ANSWERCLOSE'
    if __MODE_DEBUG__:
        print "True/false question answer: " + p[6]
    questiontext=str(p[1])+p[2]        # TODO proper communication with lexer i.e. extract value NOT tolerance
    p[0] = ParserTrueFalseQuestionBody(text=questiontext, answer=p[6])

def p_truefalsequestionbody_leadingtextnumeralwhitespace(p):
    'truefalsequestionbody : NUMERIC WHITESPACE string optionalwhitespace ANSWEROPEN optionalwhitespace WORD optionalwhitespace ANSWERCLOSE'
    if __MODE_DEBUG__:
        print "True/false question answer: " + p[7]
    questiontext=str(p[1])+" "+p[3]    # TODO proper communication with lexer i.e. extract value NOT tolerance
    p[0] = ParserTrueFalseQuestionBody(text=questiontext, answer=p[7])

## shortanswerquestion
#def p_multiplechoicequestionbody(p):

## multiple choice question 


## missing word question


## matching question


## numeric question


## essay question


# strings/numerals
def p_string(p):
    'string : WORD stringbody'
    p[0] = p[1] + p[2]
    
def p_stringbody_word(p):
    'stringbody : WORD stringbody'
    p[0] = p[1] + p[2]
    
def p_stringbody_numeric(p):
    'stringbody : NUMERIC stringbody'
    #p[0] = p[1].value + p[2]    # TODO proper communication with lexer
    p[0] = str(p[1]) + p[2]
    
def p_stringbody_ws(p):
    'stringbody : WHITESPACE stringbody'
    p[0] = " " + p[2]

def p_stringbody_epsilon(p):
    'stringbody :'
    p[0] = ""

# whitespace/linegaps etc
def p_optionalwhitespace(p):
    'optionalwhitespace : linegap'
    pass

def p_linegap_newline(p):
    'linegap : NEWLINE linegap'
    pass
    
def p_linegap_whitespace(p):
    'linegap : WHITESPACE linegap'
    pass
    
def p_linegap_epsilon(p):
    'linegap :'
    pass
    
# errors
#def p_error(p):
#    print "Syntax error in input!"
##### END PARSING RULES

def parseGift(giftStr):

    # Build the parser
    parser = yacc.yacc()
    
    # ... and parse
    result = parser.parse(giftStr, GiftLexer.lexer)
    print result.jsonSerialize()
    
"""
Quick test example
"""
if __name__ == '__main__':
    testStr="""// true-false
::Q1:: 1+1=2 {T}            // comments are okay here

// multiple choice with specific feedback
::Q2:: What's between orange and green in the spectrum?
{=yellow # correct! ~red # wrong, it's yellow ~blue # wrong, it's yellow}

// short answer question
::Q3:: Matthew's middle name? {=Timothy = Tim ~James ~Matthew}

// alternate layout for short answre question
::Title 
:: Question {
=Correct answer 1
=Correct answer 2
~Wrong answer 1
#Response to wrong answer 1
~Wrong answer 2
#Response to wrong answer 2
}"""

    testStr2="""// true-false
::Q1:: 1+1=2 {T}
::Q2:: select true as th3 answer 4 this question{T}

::Q3::Select false as the answer for th1s qu3st1on { F }
::Q4:: select true {TRUE}
::Q5:: select false { FALSE }"""
    

    parseGift(testStr2)
    
    pass
