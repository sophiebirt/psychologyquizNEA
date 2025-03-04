from Classes.User import User
from Classes.Question import Question
from Classes.SingleAnswer import SingleAnswer
from Classes.QuestionHandler import QuestionHandler

import os
import json
import random



class Quiz:
    
    def __init__(self, user):
        self.__question_handler = QuestionHandler()

        # load all questions from JSON as objects
        self.__single_answer_qs = self.__question_handler.create_single_answer_question_objects()
        #self.__multiple_choice_qs = [] # you will update this
        self.__user = user # this is a user object 

        # a 2d list of all question objects, separated by type
        self.__all_questions = [
            self.__single_answer_qs  
        ]



    def create_question_chunk(self):
        # Get one question of each type
        question_chunk = []

        for i in range(len(self.__all_questions)):
            # pick one random question from each 

            random_index = random.randint(0, len(self.__all_questions[i]))

            question_to_be_added = self.__all_questions[i][random_index]
            # TODO update the uses completed question list, check they havent already done it
            question_chunk.append(question_to_be_added)

        return question_chunk


if __name__ == "__main__":
    user = User.create_account("exampleuser200", "examplepassword200")
    quiz = Quiz(user=user)
    quiz_chunk = quiz.create_question_chunk()
    print(quiz_chunk)




