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
        super(MultipleChoice, self).__init__(q_id, topic, label, marks, question)
        self.__answer = ""
        self.__correct_answer = correct_answer
        self.__answer_options = answer_options
        
    def get_question(self):
        return self._question
    
    def get_marks(self):
        return super().get_marks()

    def display_question_page(self, quiz_object_window, current_question_number, total_number_of_questions, callback):
        """Displays the unique setup for multiple-choice questions"""
        for widget in quiz_object_window.winfo_children():
            widget.destroy()

        ctk.CTkLabel(quiz_object_window, text=f"Multiple Choice Question - Topic: {self._topic}", font=("Arial", 18)).pack(pady=10)
        ctk.CTkLabel(quiz_object_window, text=f"{current_question_number} / {total_number_of_questions}", font=("Arial", 10)).pack(pady=5)
        ctk.CTkLabel(quiz_object_window, text=self._question, font=("Arial", 18)).pack(pady=10)
        
        # Create a variable to track selected answer
        self.__selected_option = ctk.StringVar(value="None")

        # Create radio buttons for each answer option
        for option in self.__answer_options:
            ctk.CTkRadioButton(quiz_object_window, text=option, variable=self.__selected_option, value=option).pack(pady=5)

        # Submit button with a callback to check the answer and move forward
        submit_button = ctk.CTkButton(quiz_object_window, text="Submit Answer", 
                                    command=lambda: self.submit_and_continue(callback))
        submit_button.pack(pady=10)

    def submit_and_continue(self, callback):
        """Checks answer, updates stats, and calls the next question."""
        selected_answer = self.__selected_option.get()
        is_correct = selected_answer.lower() == self.__correct_answer.lower()

        print(f"Selected Answer: {selected_answer}, Correct Answer: {self.__correct_answer}, Result: {is_correct}")

        # Call the callback function to proceed to the next question
        callback(is_correct, self._topic)



