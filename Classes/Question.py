import os
import json

class Question:
    def __init__(self, question_file, label, marks, question_number ):
        self.__question_file = question_file        # where is the file located for the questions
        self.__label = label                        # short or long 
        self.__marks = marks                        # total number of marks for question
        self.__question_number = question_number    # question number

    def load_question_data(self):
        # if we can find file, read it and store it as data
        if os.path.exists(self.__question_file):
            with open(self.__question_file, 'r') as file:
                data = json.load(file)
                return data
        else:
            print("Could not find file")
            return None
