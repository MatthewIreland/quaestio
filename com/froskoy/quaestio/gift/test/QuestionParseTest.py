'''
Created on 16 Aug 2014

@author: matthew
'''
import unittest


class QuestionParseTest(unittest.TestCase):
    """
    Just for individual questions.
    
    Question examples from: https://docs.moodle.org/23/en/GIFT_format#Hints_and_Tips
    """
    
    def test_questiontitle(self):
        """
        Tests that the title is correctly transcribed when provided, and absent when not provided.
        """
        pass
    
    def test_description(self):
        """
        Tests that the description, where present, is correctly transcribed.
        """
        pass

    def test_truefalse(self):
        """
        // true/false
        ::Q1:: 1+1=2 {T}
        
        // question: 0 name: TrueStatement using {T} style
        ::TrueStatement about Grant::Grant was buried in a tomb in New York City.{T}

        // question: 0 name: FalseStatement using {FALSE} style
        ::FalseStatement about sun::The sun rises in the West.{FALSE}
        """
        pass

    def test_multichoice_singleanswer(self):
        """
        //Comment line 
        ::Question title 
        :: Question {
        =A correct answer
        ~Wrong answer1
        #A response to wrong answer1
        ~Wrong answer2
        #A response to wrong answer2
        ~Wrong answer3
        #A response to wrong answer3
        ~Wrong answer4
        #A response to wrong answer4
        }
        
        Question{= A Correct Answer ~Wrong answer1 ~Wrong answer2 ~Wrong answer3 ~Wrong answer4 }
        
        // multiple choice with specified feedback for right and wrong answers
        ::Q2:: What's between orange and green in the spectrum? 
        { =yellow # right; good! ~red # wrong, it's yellow ~blue # wrong, it's yellow }
        
        Who's buried in Grant's tomb?{=Grant ~no one ~Napoleon ~Churchill ~Mother Teresa }
        
        // question: 1 name: Grants tomb
        ::Grants tomb::Who is buried in Grant's tomb in New York City? {
        =Grant
        ~No one
        #Was true for 12 years, but Grant's remains were buried in the tomb in 1897
        ~Napoleon
        #He was buried in France
        ~Churchill
        #He was buried in England
        ~Mother Teresa
        #She was buried in India
        }
        """
        pass
    
    def test_multichoice_multianswer(self):
        """
        What two people are entombed in Grant's tomb? {
           ~%-100%No one
           ~%50%Grant
           ~%50%Grant's wife
           ~%-100%Grant's father
        }
        """
        pass
    
    def test_multichoice_partialcredit(self):
        """
        ::Jesus' hometown::Jesus Christ was from {
           ~Jerusalem#This was an important city, but the wrong answer.
           ~%25%Bethlehem#He was born here, but not raised here.
           ~%50%Galilee#You need to be more specific.
           =Nazareth#Yes! That's right!
        }.
        """
        pass
    
    def test_shortanswer_onecorrect(self):
        pass
    
    def test_shortanswer_multicorrect(self):
        """
        Who's buried in Grant's tomb?{=Grant =Ulysses S. Grant =Ulysses Grant}
        
        Two plus two equals {=four =4}
        """
        pass
    
    def test_shortanswer_partialcredit(self):
        """
        ::Jesus' hometown:: Jesus Christ was from {
           =Nazareth#Yes! That's right!
           =%75%Nazereth#Right, but misspelled.
           =%25%Bethlehem#He was born here, but not raised here.
        }
        """
        pass
    
    def test_matching(self):
        """
        // matching
        ::Q4:: Which animal eats which food? { =cat -> cat food =dog -> dog food }
        
        Match the following countries with their corresponding capitals. {
           =Canada -> Ottawa
           =Italy  -> Rome
           =Japan  -> Tokyo
           =India  -> New Delhi
        }
        """
        pass
    
    def test_missingword(self):
        """
        // fill-in-the-blank
        ::Q3:: Two plus {=two =2} equals four.
        
        Moodle costd{~lots of money =nothing ~a small amount} to download from moodle.org.
        
        Mahatma Gandhi birthday is an Indian holiday on  {
        ~15th
        ~3rd
        =2nd
        } of October.
        
        Since {
          ~495 AD
          =1066 AD
          ~1215 AD
          ~ 43 AD
        }
        the town of Hastings England has been "famous with visitors".
        """
        pass
    
    def test_numerical_singleanswer(self):
        pass
    
    def test_numerical_range(self):
        """
        // math range question
        ::Q5:: What is a number from 1 to 5? {#3:2}
        
        When was Ulysses S. Grant born?{#1822:5}
        
        What is the value of pi (to 3 decimal places)? {#3.14159:0.0005}.
        """
        pass
    
    def test_numerical_interval(self):
        """
        // math range specified with interval end points
        ::Q6:: What is a number from 1 to 5? {#1..5}
        // translated on import to the same as Q5, but unavailable from Moodle question interface
        
        What is the value of pi (to 3 decimal places)? {#3.141..3.142}.
        """
        pass
    
    def test_numerical_multicredit(self):
        """
        // multiple numeric answers with partial credit and feedback
        ::Q7:: When was Ulysses S. Grant born? {#
             =1822:0      # Correct! Full credit.
             =%50%1822:2  # He was born in 1822. Half credit for being close.
        }
        """
        pass
    
    def test_essay(self):
        """
        // essay
        ::Q8:: How are you? {}
        
        Write a short biography of Dag Hammarskjöld. {}
        """
        pass
    
    def test_specchar_escape(self):
        pass
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()