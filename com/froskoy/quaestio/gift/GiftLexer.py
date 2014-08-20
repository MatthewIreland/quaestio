'''
Created on 16 Aug 2014

@author: matthew
'''

import ply.lex as lex
import re

##### DECLARATION OF GLOBALS
__MODE_DEBUG__   = 1
##### END DECLARATION OF GLOBALS

##### TOKEN DELCARATIONS
tokens = ("QTITLEMARKER",
          "COMMENT",
          "WHITESPACE",
          "NEWLINE",
          "WORD",
          "ANSWEROPEN",
          "MULTICHOICEANSWEROPEN",
          "ANSWERNUMERICOPEN",
          "ANSWERCLOSE",
          "ANSWERCORRECTMARKER",
          "ANSWERWRONGMARKER",
          "ANSWERMATCHER",
          "NUMERIC",
          "NUMERICRANGE",
          "FEEDBACKMARKER",
          "CREDITMARKER"
          )
##### END TOKEN DELCARATIONS

##### TOKEN DEFINITIONS 
# Note that internally, lex.py uses the re module to do its patten matching.
# When building the master regular expression, rules are added in the following
# order:
## 1. All tokens defined by functions are added in the same order as they appear
##    in the lexer file.
## 2. Tokens defined by strings are added next by sorting them in order of
##    decreasing regular expression length (longer expressions are added first).
def t_COMMENT(t):
    r"//.*\n{0,1}"
    t.value = t.value.strip("\n").strip("//").strip(" ")
    t.lexer.lineno += len(t.value)
    # discard comment, for the time being
    #return t
    
def t_QTITLEMARKER(t):
    r"::"
    return t
    
def t_WHITESPACE(t):
    r"\ +"
    return t
    
def t_NUMERICRANGE(t):
    # both ints |left is not int|rght is not int| both are fractions
    r"\d+\.\.\d+|\d+\.\d+\.\.\d+|\d+\.\.\d+\.\d+|\d+\.\d+\.\.\d+\.\d+"
    parts = t.value.split("..")
    t.lowervalue=parts[0]
    t.uppervalue=parts[1]
    if __MODE_DEBUG__:
        print "NUMERIC RANGE: " + str(t.lowervalue) + " to " + str(t.uppervalue) 
    return t

def t_ANSWERNUMERICOPEN(t):
    r"{\#"
    return t
    
def t_FEEDBACKMARKER(t):
    r"\#"
    return t
    
def t_CREDITMARKER(t):
    r"%"
    return t
    
def t_NUMERIC(t):
    r"[\d:\.]*\d"
    parts = t.value.split(":")
    t.value = parts[0]
    if (len(parts) > 1):
        t.tolerance = parts[1]
    else:
        t.tolerance = 0
    if __MODE_DEBUG__:
        print "NUMERIC: " + str(t.value) + " +/- " + str(t.tolerance)
    return t

def t_MULTICHOICEANSWEROPEN(t):
    r"{m"
    return t

def t_ANSWEROPEN(t):
    r"{"
    return t
    
def t_ANSWERCLOSE(t):
    r"}"
    return t

def t_ANSWERCORRECTMARKER(t):
    r"="
    return t

def t_ANSWERWRONGMARKER(t):
    r"~"
    return t
    
def t_ANSWERMATCHER(t):
    r"\->"
    return t
    
def t_WORD(t):
    #r"[a-zA-Z0-9_@\.,@<>():'\\\"\+\*=?!]|[a-zA-Z0-9_@\.,@<>():'\\\"\+\*=?!][a-zA-Z0-9_@\.,@<>():'\ \\\"\+\*=?!]*[a-zA-Z0-9_@\.,@<>():'\\\"\+\*=?!]"
    r"[^\s:{}]+"  # TODO don't include # either
    return t

def t_NEWLINE(t):
    r"\n"
    t.lexer.lineno += len(t.value)
    return t
    
def t_error(t):
    raise TypeError("Unknown text at line %d '%s'" % (t.lexer.lineno, t.value))

# ignore tabs
t_ignore = '\t'
##### END TOKEN DEFINITIONS 


##### LEXER BUILDING
lexer = lex.lex()
##### END LEXER BUILDING 



def lexGift(giftStr):
    if not isinstance(giftStr, str):
        raise TypeError("GIFT input must be a string")
    
    lexer.input(giftStr)
    
    #if __MODE_DEBUG__:
    #    for tok in iter(lexer.token(), None):
    #        print repr(tok.type), repr(tok.value)
    
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
        print tok
            
            
            
"""
Quick test example
"""
if __name__ == '__main__':
    testStr="""// true-false
::Q1:: 1+1=2 {T}            // comments are okay here

// multiple choice with specific feedback
::Q2:: What's between orange and green in the spectrum?
{=yellow # correct! ~red # wrong, it's yellow ~blue # wrong, it's yellow}

// fill-in-the-blank
::Q3:: Two plus {=two =2} equals four.

// matching
::Q4:: Which animal eats which food? { =cat -> cat food =dog -> dog food }

// math range question -- note: {#1..5} is the same range
::Q5:: What is a number from 1 to 5? {#3:2}

// another math range question
::Q5.5:: What is a number from 1 to 5? {#1..5}

// multiple numeric answers with partial credit and feedback
::Q7:: When was Ulysses S. Grant born? {#
   =1822:0      # Correct! You get full credit.
   =%50%1822:2  # He was born in 1822. You get half credit for being close.
}

// essay
::Q8:: How are you? {}

// alternate layout
::Title 
:: Question {
=Correct answer 1
=Correct answer 2
~Wrong answer 1
#Response to wrong answer 1
~Wrong answer 2
#Response to wrong answer 2
}"""
    testStr2 ="""// true-false
::Q1:: 1+1=2 {T}            // comments are okay here"""

    testStr3="""// true-false
::Q1:: 1+1=2 {T}
::Q2:: select true as th3 answer 4 this question{T}

::Q3::Select false as the answer for th1s qu3st1on { F }
::Q4:: select true {TRUE}
::Q5:: select false { FALSE }

// multiple choice question
select four correct answers {m =this one is correct = this one is also correct ~this one is wrong ~ so is this one =this one is correct again ~ this one is wrong again = this one is the final correct answer ~and the final wrong one is here }

// multiple choice with specific feedback
::Q7:: What's between orange and green in the spectrum?
{m=yellow # correct! ~red # wrong, it's yellow ~blue # wrong, it's yellow}

// multiple choice question with varied feedback
::Q8:: What's betw33n or4nge and green 1n the spectrum?
{m=yellow ~red # wrong, it's yellow ~blue # wrong, it's yellow}
"""

    testStr5 = """::Q7:: What's between orange and green in the spectrum?
{=yellow # correct! ~red # wrong, it's yellow ~blue # wrong, it's yellow}"""


    lexGift(testStr5)
