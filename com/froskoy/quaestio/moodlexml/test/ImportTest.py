'''
Created on 16 Aug 2014

@author: matthew
'''
import unittest


class XMLImportTest(unittest.TestCase):
    """
    Question examples from: https://docs.moodle.org/24/en/Moodle_XML_format
    """
    
    def test_truefalse(self):
        """
        <question type="truefalse">
         <answer fraction="100">
            <text>true</text>
            <feedback><text>Correct!</text></feedback>
         </answer>
         <answer fraction="0">
            <text>false</text>
            <feedback><text>Ooops!</text></feedback>
         </answer>
        """
        pass
    
    def test_shortanswer(self):
        """
        <question type="shortanswer">
         <answer fraction="100">
         <text>The correct answer</text>
         <feedback><text>Correct!</text></feedback>
         </answer>
 
         <question type="shortanswer">
         <answer fraction="100">
             <text>The correct answer</text>
             <feedback><text>Correct!</text></feedback>
         </answer>
         <answer fraction="100">
             <text>An alternative answer</text>
             <feedback><text>Correct!</text></feedback>
         </answer>
        """
        pass

    def test_multichoice_partial_feedback(self):
        """
        <question type="multichoice">
 <answer fraction="100">
     <text>The correct answer</text>
    <feedback><text>Correct!</text></feedback>
 </answer>
 <answer fraction="0">
     <text>A distractor</text>
    <feedback><text>Ooops!</text></feedback>
 </answer>
 <answer fraction="0">
     <text>Another distractor</text>
    <feedback><text>Ooops!</text></feedback>
 </answer>
 <shuffleanswers>1</shuffleanswers>
 <single>true</single>
 <answernumbering>abc</answernumbering>
        """
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()