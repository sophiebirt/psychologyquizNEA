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
        super(SingleAnswer, self).__init__(q_id, topic, label, marks, question)
        self.__answer = ""
        self.__correct_answer = correct_answer

    def get_question(self):
        return self._question
    
    def get_marks(self):
        return super().get_marks()

    def display_question_page(self, quiz_object_window, current_question_number, total_number_of_questions, callback):
        """Displays a single-answer question page and calls callback when answered"""
        for widget in quiz_object_window.winfo_children():
            widget.destroy()

        ctk.CTkLabel(quiz_object_window, text=f"Question {current_question_number} / {total_number_of_questions}", font=("Arial", 18)).pack(pady=10)
        ctk.CTkLabel(quiz_object_window, text=f"Topic: {self._topic}", font=("Arial", 16)).pack(pady=5)
        ctk.CTkLabel(quiz_object_window, text=self._question, font=("Arial", 18)).pack(pady=10)

        self.__answer_entry = ctk.CTkEntry(quiz_object_window, placeholder_text="Your Answer")
        self.__answer_entry.pack(pady=5)

        def submit_and_continue():
            user_answer = self.__answer_entry.get()
            correct = user_answer.lower() == self.__correct_answer.lower()  # Check correctness
            callback(correct, self._topic)  # Call the callback function

        # Submit button that calls `submit_and_continue()`
        ctk.CTkButton(quiz_object_window, text="Submit", command=submit_and_continue).pack(pady=10)

    

        


