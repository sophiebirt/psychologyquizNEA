from Classes.Question import Question
import os 
import json

'''
Multiple Choice Question Subclass
-> These questions only have one correct answer
-> They have 4 possible options for answers (this is fixed)
-> These are of label short
'''

class MultipleChoice(Question):
    def __init__(self, q_id, question, topic, label, marks, correct_answer, answer_options):
        super(MultipleChoice, self).__init__(q_id, topic, label, marks)
        self.__question = question
        self.__answer = ""
        self.__correct_answer = correct_answer
        self.__answer_options = answer_options
        

    def get_question(self):
        return self.__question
    
    def check_answer(self):
        if self.__answer == self.__correct_answer:
            return True
        else:
            return False


