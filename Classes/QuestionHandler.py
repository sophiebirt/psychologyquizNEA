import os
import json

from Classes.SingleAnswer import SingleAnswer


# TODO:
# -> create a function (inside this class) that loads multiple choice
#       -> creating multiple question in a json format
#       -> create a MultipleChoice class (use single answer as template)
#       -> create the loads objects function like below
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
        
    def create_single_answer_question_objects(self):
        question_data = self.load_questions(SINGLE_ANSWER_Q_FILE)
        question_array = question_data['questionsList']
        #print(question_array)

        question_objects = []

        print(len(question_array))

        for q in question_array:
            q_id = q["q_id"]
            question = q["question"]
            topic = q["topic"]
            marks = q["TM"]
            correct_answer = q["correct_answer"]
            

            new_question = SingleAnswer(q_id, question, topic, "short", marks, correct_answer)
            question_objects.append(new_question)

        return question_objects
            