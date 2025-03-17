from Classes.Question import Question
import os 
import json
import customtkinter as ctk
import tkinter

'''
Multiple Choice Question Subclass
-> These questions only have one correct answer
-> They have 4 possible options for answers (this is fixed)
-> These are of label short
'''

class MultipleChoice(Question):
    def __init__(self, q_id, question, topic, label, marks, correct_answer, answer_options):
        super(MultipleChoice, self).__init__(q_id, topic, label, marks)
        self.__question = question
        self.__answer = ""
        self.__correct_answer = correct_answer
        self.__answer_options = answer_options
        
    def get_question(self):
        return self.__question
    
    def check_answer(self):
        if self.__selected_option.get() == self.__correct_answer:
            print ("Correct")
            
        else:
            print("Incorrect")

    def display_question_page(self, quiz_object_window, current_question_number, total_number_of_questions):
        """Displays the unique setup for single answer questions"""
        for widget in quiz_object_window.winfo_children():
            widget.destroy()

        ctk.CTkLabel(quiz_object_window, text=(f"Multiple Choice Question - Topic: {self._topic}"), font=("Arial", 18)).pack(pady=10)
        ctk.CTkLabel(quiz_object_window, text=(f"{current_question_number} / {total_number_of_questions}"), font=("Arial", 10)).pack(pady=10)
        ctk.CTkLabel(quiz_object_window, text=self.__question, font=("Arial", 18)).pack(pady=10)
        
        # List of options
        options = self.__answer_options

        # Variable to track selected option
        self.__selected_option = ctk.StringVar(value="None")

        for option in options:
            radio_btn = ctk.CTkRadioButton(quiz_object_window, text=option, variable=self.__selected_option, value=option)
            radio_btn.pack(pady=10)        

        self.__correct = ctk.CTkButton(quiz_object_window, text="Submit Answer", command=self.check_answer)
        self.__correct.pack(pady=10)
        


