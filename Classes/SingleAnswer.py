from Classes.Question import Question
import os 
import json

'''
Single Answer Question Subclass
-> These questions only have one correct answer
-> These are of label short
'''

class SingleAnswer(Question):
    def __init__(self, q_id, question, topic, label, marks, correct_answer):
        super(SingleAnswer, self).__init__(q_id, topic, label, marks)
        self.__question = question
        self.__answer = ""
        self.__correct_answer = correct_answer

    def get_question(self):
        return self.__question
    
    # over simplified 
    def check_answer(self):
        if self.__answer.lower() == self.__correct_answer.lower():
            return True
        else:
            return False


