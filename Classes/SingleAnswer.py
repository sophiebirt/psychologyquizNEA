from Classes.Question import Question
import os 
import json

class SingleAnswer(Question):
    def __init__(self, question, topic, label, marks, question_number, correct_answer):
        super(SingleAnswer, self).__init__(topic, label, marks, question_number)
        self.__question = question
        self.__answer = ""
        self.__correct_answer = correct_answer

    def get_question(self):
        return self.__question


