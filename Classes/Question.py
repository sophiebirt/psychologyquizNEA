import os
import json
import re

class Question:
    def __init__(self, q_id, topic, label, marks, question):
        self.__q_id = q_id
        self._topic = topic
        self.__label = label                            # short or long 
        self._marks = int(marks)                       # total number of marks for question
        self._question = self.insert_newlines(question)

         
    def get_marks(self): 
        return self._marks
    
    @staticmethod
    def insert_newlines(text, line_length=20):
        # Use a regular expression to match groups of words that fit within the line length
        return '\n'.join(re.findall(r'.{1,' + str(line_length) + r'}(?:\s+|$)', text))
