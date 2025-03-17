from Classes.Question import Question
import os 
import json
import customtkinter as ctk

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
        print("CHECKING QUESTION !!!")
        if self.__answer.lower() == self.__correct_answer.lower():
            return True
        else:
            return False
        
        
    def display_question_page(self, quiz_object_window, current_question_number, total_number_of_questions):
        """Displays the unique setup for single answer questions"""
        for widget in quiz_object_window.winfo_children():
            widget.destroy()

        ctk.CTkLabel(quiz_object_window, text=(f"Single Answer Question - Topic: {self._topic}"), font=("Arial", 18)).pack(pady=10)
        ctk.CTkLabel(quiz_object_window, text=(f"{current_question_number} / {total_number_of_questions}"), font=("Arial", 10)).pack(pady=10)
        ctk.CTkLabel(quiz_object_window, text=self.__question, font=("Arial", 18)).pack(pady=10)
        
        self.__answer = ctk.CTkEntry(quiz_object_window, placeholder_text="Answer")
        self.__answer.pack(pady=5)
        
        # Run Login Function
        self.__correct = ctk.CTkButton(quiz_object_window, text="Submit Answer", command=self.check_answer)
        self.__correct.pack(pady=10)

        print(self.__correct)

        


