from Classes.User import User
from Classes.Question import Question
from Classes.SingleAnswer import SingleAnswer

import os
import json

# Static Variables
SINGLE_ANSWER_Q_FILE = "psychologyquizNEA\questions\single_answer.json"


class QuestionHandler():
    def __init__(self):
        pass

    def load_questions(self, file_location):
         # if we can find file, read it and store it as data
        if os.path.exists(file_location):
            with open(file_location, 'r') as file:
                data = json.load(file)
                return data
        else:
            print("Could not find file")
            return None
        
    def create_single_answer_question_objects(self, file_location):
        question_data = self.load_questions(file_location)
        question_array = question_data['questionsList']
        #print(question_array)

        question_objects = []

        print(len(question_array))

        for q in question_array:
            question_number = q["questionNo"]
            question = q["question"]
            topic = q["topic"]
            marks = q["TM"]
            correct_answer = q["correct_answer"]
            print(question_number)

            new_question = SingleAnswer(question, topic, "short", marks, question_number, correct_answer)
            question_objects.append(new_question)

        return question_objects
            
            



new_user = User.create_account("exampleuser200", "examplepassword200")
#print("New user created:", new_user)

question_handler = QuestionHandler()
single_answer_question_objects = question_handler.create_single_answer_question_objects(SINGLE_ANSWER_Q_FILE)

for question in single_answer_question_objects:
    print(question.get_question())

print(single_answer_question_objects)

#question1 = SingleAnswer(SINGLE_ANSWER_Q_FILE, "label", ) 

#new_user = User.login("james", "james123") # This should return and error

#new_user = User.login("exampleUser", "examplePassword")

#print(new_user)


