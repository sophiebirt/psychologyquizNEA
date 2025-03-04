import os
import json

class Question:
    def __init__(self, topic, label, marks, question_number ):
        # where is the file located for the questions
        self.__topic = topic
        self.__label = label                        # short or long 
        self.__marks = marks                        # total number of marks for question
        self.__question_number = question_number    # question number

 
       
