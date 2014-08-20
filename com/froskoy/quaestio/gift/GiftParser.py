'''
Created on 16 Aug 2014

@author: matthew
'''

import ply.yacc as yacc
import GiftLexer
from GiftParseError import GiftParseError
from com.froskoy.quaestio.quiz.Quiz import Quiz
from com.froskoy.quaestio.quiz.TrueFalseQuestion import TrueFalseQuestion
from com.froskoy.quaestio.quiz.TrueFalseQuestionAnswer import TrueFalseQuestionAnswer
from com.froskoy.quaestio.quiz.MultipleChoiceQuestion import MultipleChoiceQuestion
from com.froskoy.quaestio.quiz.MultipleChoiceQuestionAnswer import MultipleChoiceQuestionAnswer
from com.froskoy.quaestio.quiz.ShortAnswerQuestion import ShortAnswerQuestion
from com.froskoy.quaestio.quiz.ShortAnswerQuestionAnswer import ShortAnswerQuestionAnswer
from GiftLexer import tokens

##### DEFINITION OF GLOBALS
__MODE_DEBUG__ = 0
questionName = None
questions = []
parserAnswers = []
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
        
class ParserMultiChoiceQuestionBody:
    def __init__(self, text, answers):
        # TODO: appropriate type checks
        self.text   = text
        self.answers = answers
        
class ParserShortAnswerQuestionBody:
    def __init__(self, text, answers):
        # TODO: appropriate type checks
        self.text   = text
        self.answers = answers

def parserAddQuestion(question):
    if __MODE_DEBUG__:
        print "Adding question!!!"
    global parserAnswers
    questions.append(question)
    parserAnswers = []    # TODO remove this global variable in favour of passing answers in a more tidy fashion (via p[0])
    
def parserConstructQuestion(name=None, questionBody=None):
    if (questionBody is None):
        raise InvalidQuestionBodyError("Question body must not be None!")
    if __MODE_DEBUG__:
        print name
    if (questionBody.__class__ == ParserTrueFalseQuestionBody):
        return TrueFalseQuestion(questionText=questionBody.text,
                                 isTrue=questionBody.correct,
                                 correctFeedback=None,
                                 incorrectFeedback=None,
                                 name=name)
    if (questionBody.__class__ == ParserMultiChoiceQuestionBody):
        return MultipleChoiceQuestion(questionText=questionBody.text,
                                      answers=questionBody.answers,
                                      name=name,
                                      single=None,
                                      shuffleAnswers=0,
                                      correctFeedback=None,
                                      partiallyCorrectFeedback=None,
                                      incorrectFeedback=None,
                                      answerNumbering="none")
    if (questionBody.__class__ == ParserShortAnswerQuestionBody):
        return ShortAnswerQuestion(questionText=questionBody.text,
                                   answers=questionBody.answers,
                                   name=name,
                                   feedback=None,
                                   hidden=0,
                                   usecase=0)
    raise ValueError("question class unrecognised")

##### End Internal class and method definitions


##### PARSING RULES
# quiz and quizbody
def p_quiz(p):
    'quiz : linegap quizbody'
    if __MODE_DEBUG__:
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
    p[0] = p[3].strip(" ")

def p_questionbody(p):
    """questionbody : truefalsequestionbody
                    | multiplechoicequestionbody
                    | shortanswerquestionbody"""
    p[0] = p[1]

"""    
def p_questionbody_missingword(p):
    'questionbody : missingwordquestionbody'
    
def p_questionbody_matching(p):
    'questionbody : matchingquestionbody'
    
def p_questionbody_numeric(p):
    'questionbody : numericquestionbody'
    
def p_questionbody_essay(p):
    'questionbody : essayquestionbody'
"""

def p_answerstring(p):
    'answerstring : string'
    p[0] = p[1]
    
def p_answerstring_withnumeral(p):
    'answerstring : NUMERIC string'
    p[0] = str(p[1]) + p[2]
    
def p_answerstring_withnumeralandwhitespace(p):
    'answerstring : NUMERIC WHITESPACE string'
    p[0] = str(p[1]) + " " + p[3]

def p_answerfeedback(p):
    'answerfeedback : FEEDBACKMARKER optionalwhitespace answerstring'
    p[0] = p[3]

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

## multiple choice question 
def p_multiplechoicequestionbody(p):
    'multiplechoicequestionbody : string optionalwhitespace MULTICHOICEANSWEROPEN multichoiceanswers optionalwhitespace ANSWERCLOSE'
    if __MODE_DEBUG__:
        print "Multiple choice question."
    #p[0] = ParserMultiChoiceQuestionBody(text=p[1], answers=p[4])
    global parserAnswers
    p[0] = ParserMultiChoiceQuestionBody(text=p[1], answers=parserAnswers)
    parserAnswers=[]

def p_multiplechoicequestionbody_leadingtextnumeral(p):
    'multiplechoicequestionbody : NUMERIC string optionalwhitespace MULTICHOICEANSWEROPEN multichoiceanswers optionalwhitespace ANSWERCLOSE'
    if __MODE_DEBUG__:
        print "Multiple choice question (with leading numeral)."
    questiontext=str(p[1])+p[2]        # TODO proper communication with lexer i.e. extract value NOT tolerance
    #p[0] = ParserMultiChoiceQuestionBody(text=questiontext, answers=p[5])
    global parserAnswers
    p[0] = ParserMultiChoiceQuestionBody(text=questiontext, answers=parserAnswers)
    parserAnswers=[]

def p_multiplechoicequestionbody_leadingtextnumeralwhitespace(p):
    'multiplechoicequestionbody : NUMERIC WHITESPACE string optionalwhitespace MULTICHOICEANSWEROPEN multichoiceanswers optionalwhitespace ANSWERCLOSE'
    if __MODE_DEBUG__:
        print "Multiple choice question (with leading numeral and whitespace)."
    questiontext=str(p[1])+" "+p[3]    # TODO proper communication with lexer i.e. extract value NOT tolerance
    #p[0] = ParserMultiChoiceQuestionBody(text=questiontext, answers=p[6])
    global parserAnswers
    p[0] = ParserMultiChoiceQuestionBody(text=questiontext, answers=parserAnswers)
    parserAnswers=[]

def p_multichoiceanswers(p):
    'multichoiceanswers : optionalwhitespace multichoiceanswer multichoiceanswers'
    #if p[3] is not None:          # TODO think about this when awake
    #    p[0] = p[3].append(p[2])
    #p[0] = parserAnswers             # TODO remove
    
def p_multichoiceanswers_base(p):
    'multichoiceanswers : optionalwhitespace multichoiceanswer'
    p[0] = [p[2]]
    
def p_multichoiceanswer(p):
    """multichoiceanswer : multichoicecorrectanswer
                         | multichoiceincorrectanswer"""
    p[0] = p[1]
    
def p_multichoicecorrectanswer(p):
    'multichoicecorrectanswer : ANSWERCORRECTMARKER optionalwhitespace answerstring linegap'
    p[0] = MultipleChoiceQuestionAnswer(text=p[3].strip(" "), fraction=100, selectedFeedback=None)
    parserAnswers.append(p[0])   # TODO remove
    
def p_multichoicecorrectanswer_withfeedback(p):
    'multichoicecorrectanswer : ANSWERCORRECTMARKER optionalwhitespace answerstring optionalwhitespace answerfeedback linegap'
    p[0] = MultipleChoiceQuestionAnswer(text=p[3].strip(" "), fraction=100, selectedFeedback=p[5].strip(" "))
    parserAnswers.append(p[0])   # TODO remove
    
def p_multichoiceincorrectanswer(p):
    'multichoiceincorrectanswer : ANSWERWRONGMARKER optionalwhitespace answerstring linegap'
    p[0] = MultipleChoiceQuestionAnswer(text=p[3].strip(" "), fraction=0, selectedFeedback=None)
    parserAnswers.append(p[0])   # TODO remove
    
def p_multichoiceincorrectanswer_withfeedback(p):
    'multichoiceincorrectanswer : ANSWERWRONGMARKER optionalwhitespace answerstring optionalwhitespace answerfeedback linegap'
    p[0] = MultipleChoiceQuestionAnswer(text=p[3].strip(" "), fraction=0, selectedFeedback=p[5].strip(" "))
    parserAnswers.append(p[0])   # TODO remove

## shortanswerquestion
def p_shortanswerquestionbody(p):
    'shortanswerquestionbody : string optionalwhitespace ANSWEROPEN shortansweranswers optionalwhitespace ANSWERCLOSE'
    if __MODE_DEBUG__:
        print "Short answer question."
    #p[0] = ParserMultiChoiceQuestionBody(text=p[1], answers=p[4])
    global parserAnswers
    p[0] = ParserShortAnswerQuestionBody(text=p[1], answers=parserAnswers)
    parserAnswers=[]

def p_shortanswerquestionbody_leadingtextnumeral(p):
    'shortanswerquestionbody : NUMERIC string optionalwhitespace ANSWEROPEN shortansweranswers optionalwhitespace ANSWERCLOSE'
    if __MODE_DEBUG__:
        print "Short answer question (with leading numeral)."
    questiontext=str(p[1])+p[2]        # TODO proper communication with lexer i.e. extract value NOT tolerance
    #p[0] = ParserShortAnswerQuestionBody(text=questiontext, answers=p[5])
    global parserAnswers
    p[0] = ParserShortAnswerQuestionBody(text=questiontext, answers=parserAnswers)
    parserAnswers=[]

def p_shortanswerquestionbody_leadingtextnumeralwhitespace(p):
    'shortanswerquestionbody : NUMERIC WHITESPACE string optionalwhitespace ANSWEROPEN shortansweranswers optionalwhitespace ANSWERCLOSE'
    if __MODE_DEBUG__:
        print "Short answer question (with leading numeral and whitespace)."
    questiontext=str(p[1])+" "+p[3]    # TODO proper communication with lexer i.e. extract value NOT tolerance
    #p[0] = ParserShortAnswerQuestionBody(text=questiontext, answers=p[6])
    global parserAnswers
    p[0] = ParserShortAnswerQuestionBody(text=questiontext, answers=parserAnswers)
    parserAnswers=[]

def p_shortansweranswers(p):
    'shortansweranswers : optionalwhitespace shortansweranswer linegap shortansweranswers'
    pass
    #if p[3] is not None:          # TODO think about this when awake
    #    p[0] = p[3].append(p[2])
    #p[0] = parserAnswers             # TODO remove
    
def p_shortansweranswers_base(p):
    'shortansweranswers : optionalwhitespace shortansweranswer linegap'
    p[0] = [p[2]]
    
def p_shortansweranswer(p):
    """shortansweranswer : shortanswercorrectanswer
                         | shortanswerincorrectanswer"""
    p[0] = p[1]
    
def p_shortanswercorrectanswer(p):
    'shortanswercorrectanswer : ANSWERCORRECTMARKER optionalwhitespace answerstring linegap'
    p[0] = ShortAnswerQuestionAnswer(text=p[3].strip(" "), fraction=100, feedback=None, usecase=0)
    parserAnswers.append(p[0])   # TODO remove
    
def p_shortanswercorrectanswer_withfeedback(p):
    'shortanswercorrectanswer : ANSWERCORRECTMARKER optionalwhitespace answerstring optionalwhitespace answerfeedback linegap'
    p[0] = ShortAnswerQuestionAnswer(text=p[3].strip(" "), fraction=100, feedback=p[5].strip(" "), usecase=0)
    parserAnswers.append(p[0])   # TODO remove
    
def p_shortanswerincorrectanswer(p):
    'shortanswerincorrectanswer : ANSWERWRONGMARKER optionalwhitespace answerstring linegap'
    p[0] = ShortAnswerQuestionAnswer(text=p[3].strip(" "), fraction=0, feedback=None, usecase=0)
    parserAnswers.append(p[0])   # TODO remove
    
def p_shortanswerincorrectanswer_withfeedback(p):
    'shortanswerincorrectanswer : ANSWERWRONGMARKER optionalwhitespace answerstring optionalwhitespace answerfeedback linegap'
    p[0] = ShortAnswerQuestionAnswer(text=p[3].strip(" "), fraction=0, feedback=p[5].strip(" "), usecase=0)
    parserAnswers.append(p[0])   # TODO remove


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
"""
def p_error(p):
    raise GiftParseError("Syntax error in input!")
"""
##### END PARSING RULES

def parseGift(giftStr):

    # Build the parser
    parser = yacc.yacc()
    
    # ... and parse
    result = parser.parse(giftStr, GiftLexer.lexer)
    if __MODE_DEBUG__:
        if result is not None:
            print result.jsonSerialize()
        else:
            print("There were errors in the parse.")
    
    return result
    
"""
Quick test example
"""
if __name__ == '__main__':
    testStr="""// true-false
::Q1:: 1+1=2 {T}            // comments are okay here

// multiple choice with specific feedback
::Q2:: What's between orange and green in the spectrum?
{m=yellow # correct! ~red # wrong, it's yellow ~blue # wrong, it's yellow}

// short answer question
::Q3:: Matthew's middle name? {=Timothy = Tim ~James ~Matthew}

// alternate layout for short answer question
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
select true {TRUE}
::Q5:: select false { FALSE }

// multiple choice question
select four correct answers {m =this one is correct = this one is also correct ~this one is wrong ~ so is this one =this one is correct again ~ this one is wrong again = this one is the final correct answer ~and the final wrong one is here}

// multiple choice with specific feedback
::Q7:: What's between orange and green in the spectrum?
{m=yellow # correct! ~red # wrong, it's yellow ~blue # wrong, it's yellow}

// multiple choice question with varied feedback
::Q8:: What's betw33n or4nge and green 1n the spectrum?
{m=yellow ~red # wrong, it's yellow ~blue # wrong, it's yellow}
"""

    testStr3 = """::Q7:: Type a correct answer
{ =correct # feedback = a correct answer ~a wrong answer #multi word feedback ~ another wrong answer # some more feedback}"""

    testStr4 = """// multiple choice question
this time there are four correct answers { =this one is correct = this one is also correct ~this one is wrong ~ so is this one =this one is correct again ~ this one is wrong again = this one is the final correct answer ~and the final wrong one is here}

// short answer with (more) specific feedback
::Q7:: What's between orange and green in the spectrum?
{=yellow # correct! ~red # wrong, it's yellow ~blue # wrong, it's yellow}

// multiple choice question with varied feedback
::Q8:: What's betw33n or4nge and green 1n the spectrum?
{=yellow ~red # wrong, it's yellow ~blue # wrong, it's yellow}
"""
    testStr5 = """::Q7:: What's between orange and green in the spectrum?
{=yellow # correct! ~red # wrong, it's yellow ~blue # wrong, it's yellow}"""

    testStr7 = """// alternate layout for short answer question
::Title
:: Question {m
= Correct answer 1
= Correct answer 2
~ Wrong answer 1
# Response to wrong answer 1
~ Wrong answer 2
# Response to wrong answer 2
}
"""

    testStr8 = """// true-false
::Q1:: 1+1=2 {T}            // comments are okay here

// multiple choice with specific feedback
::Q2:: What's between orange and green in the spectrum?
{m=yellow # correct! ~red # wrong, it's yellow ~blue # wrong, it's yellow}

// short answer question
::Q3:: Matthew's middle name? {=Timothy = Tim ~James ~Matthew}

// alternate layout for short answer question
::Title 
:: Question {
=Correct answer 1
=Correct answer 2
~Wrong answer 1
#Response to wrong answer 1
~Wrong answer 2
#Response to wrong answer 2
}

::Title
:: Question {m
= Correct answer 1
= Correct answer 2
~ Wrong answer 1
# Response to wrong answer 1
~ Wrong answer 2
# Response to wrong answer 2
}

::Title
:: Question {
= Correct answer 1
= Correct answer 2
~ Wrong answer 1
# Response to wrong answer 1
~ Wrong answer 2
# Response to wrong answer 2
}

::Title:: Question {
= Correct answer 1
= Correct answer 2
~ Wrong answer 1
# Response to wrong answer 1
~ Wrong answer 2
# Response to wrong answer 2
}

::Title:: Question {m
= Correct answer 1
= Correct answer 2
~ Wrong answer 1
# Response to wrong answer 1
~ Wrong answer 2
# Response to wrong answer 2
}

// short answer question
this time there are four correct answers { =this one is correct = this one is also correct ~this one is wrong ~ so is this one =this one is correct again ~ this one is wrong again = this one is the final correct answer ~and the final wrong one is here}

// short answer with (more) specific feedback
::Q7:: What's between orange and green in the spectrum?
{=yellow # correct! ~red # wrong, it's yellow ~blue # wrong, it's yellow}

// multiple choice question with varied feedback
::Q8:: What's betw33n or4nge and green 1n the spectrum?
{=yellow ~red # wrong, it's yellow ~blue # wrong, it's yellow}


// multiple choice question
this time there are four correct answers {m =this one is correct = this one is also correct ~this one is wrong ~ so is this one =this one is correct again ~ this one is wrong again = this one is the final correct answer ~and the final wrong one is here}

// short answer with (more) specific feedback
::Q7:: What's between orange and green in the spectrum?
{m=yellow # correct! ~red # wrong, it's yellow ~blue # wrong, it's yellow}

// multiple choice question with varied feedback
::Q8:: What's betw33n or4nge and green 1n the spectrum?
{m=yellow ~red # wrong, it's yellow ~blue # wrong, it's yellow}

::Q1a:: 1+1=2 {T}            // comments are okay here

::Q1b::
1+1=2
{T}

::Q1c:: 1+1=2 {
T} 

::Q1d:: 1+1=2 {TRUE}            // comments are okay here

::Q1e:: 1+1=2 {FALSE}            // comments are okay here

// multiple choice with specific feedback
::Q2a:: What's between orange and green in the spectrum?
{m
=yellow
# correct!
~red
# wrong, it's yellow
~blue
# wrong, it's yellow}

// short answer question
::Q3a:: Matthew's middle name? {=Timothy = Tim ~James ~Matthew}
 
"""

    parseGift(testStr8)
    
    pass
