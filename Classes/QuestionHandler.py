import os
import json

from Classes.SingleAnswer import SingleAnswer
from Classes.MultipleChoice import MultipleChoice

SINGLE_ANSWER_Q_FILE = "questions\single_answer.json"
MULTIPLE_CHOICE_Q_FILE = "questions\multiple_choice.json"

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
        print(question_array)

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
   
    def create_multiple_choice_question_objects(self): 
        question_data = self.load_questions(MULTIPLE_CHOICE_Q_FILE)
        question_array = question_data['questionsList']

        question_objects = []

        print(len(question_array))
        
        for q in question_array:
            q_id = q["q_id"]
            question = q["question"]
            topic = q["topic"]
            marks = q["TM"]
            correct_answer = q["correct_answer"]
            answer_options = [q["answer_option_1"], q["answer_option_2"], q["answer_option_3"], q["answer_option_4"]]
            
            new_question = MultipleChoice(q_id, question, topic, "short", marks, correct_answer, answer_options)
            question_objects.append(new_question)

        return question_objects
