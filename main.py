from Classes.User import User
from Classes.Question import Question
from Classes.SingleAnswer import SingleAnswer
from Classes.QuestionHandler import QuestionHandler


import customtkinter as ctk
import os
import json
import random

# Static
ACCOUNT_DATA = "psychologyquizNEA/Account/student_data.json" # this may vary depending on machine and dev environment 


class QuizApp():
    
    def __init__(self):

        # TKinter Data
        self.__window = ctk.CTk()
        self.__window.title("Psychology Quiz")
        self.__window.geometry("600x400")

        # Question Data 
        self.__question_handler = QuestionHandler()
        self.__single_answer_qs = self.__question_handler.create_single_answer_question_objects()
        self.__multiple_choice_qs = self.__question_handler.create_multiple_choice_question_objects()

        print(f"Lengths - SA: {len(self.__single_answer_qs)}, MC: {len(self.__multiple_choice_qs)}")


        self.__all_questions = [
            self.__single_answer_qs, 
            self.__multiple_choice_qs 
        ]

        # User Data 
        self.__user = None # this is a user object 

        self.create_login_page()

    def create_login_page(self):
        """Creates the login page UI."""
        for widget in self.__window.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.__window, text="Login", font=("Arial", 18)).pack(pady=10)
        
        self.__username_entry = ctk.CTkEntry(self.__window, placeholder_text="Username")
        self.__username_entry.pack(pady=5)
        
        self.__password_entry = ctk.CTkEntry(self.__window, placeholder_text="Password", show="*")
        self.__password_entry.pack(pady=5)
        
        # Run Login Function
        self.__login_button = ctk.CTkButton(self.__window, text="Login", command=self.login)
        self.__login_button.pack(pady=10)

        # Load Login Page
        self.__signup_button = ctk.CTkButton(self.__window, text="Sign Up", command=self.create_signup_page)
        self.__signup_button.pack(pady=5)

    def create_signup_page(self):
        """Creates the sign-up page UI."""
        for widget in self.__window.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.__window, text="Sign Up", font=("Arial", 18)).pack(pady=10)
        
        self.__new_username_entry = ctk.CTkEntry(self.__window, placeholder_text="New Username")
        self.__new_username_entry.pack(pady=5)

        self.__new_password_entry = ctk.CTkEntry(self.__window, placeholder_text="New Password", show="*")
        self.__new_password_entry.pack(pady=5)

        self.__confirm_signup_button = ctk.CTkButton(self.__window, text="Create Account", command=self.signup)
        self.__confirm_signup_button.pack(pady=10)

        self.__back_button = ctk.CTkButton(self.__window, text="Back to Login", fg_color="gray", command=self.create_login_page)
        self.__back_button.pack(pady=5)

    def login(self):
        username = self.__username_entry.get()
        password = self.__password_entry.get()

        self.__user = User.login(username, password, ACCOUNT_DATA)

        if self.__user: 
            print(f"{self.__user.get_name()} has logged in!")
        else: 
            print(f"Username or Password not correct")

    def signup(self):
        new_username = self.__new_username_entry.get()
        new_password = self.__new_password_entry.get()

        if new_username and new_password:
            new_user = User.create_account(new_username, new_password, ACCOUNT_DATA)
            if new_user:
                print(f"Account created for {new_user.get_name()}!")
                self.create_login_page()  # Redirect to login after signing up
            else:
                print("Error creating account.")
        else:
            print("Please enter a valid username and password.")
    

    def run(self):
        self.__window.mainloop()    
        
    def create_question_chunk(self):
        # Get one question of each type
        question_chunk = []

        for i in range(len(self.__all_questions)):
            # pick one random question from each 

            random_index = random.randint(0, len(self.__all_questions[i]) - 1)


            question_to_be_added = self.__all_questions[i][random_index]
            # TODO update the uses completed question list, check they havent already done it
            question_chunk.append(question_to_be_added)

        return question_chunk


if __name__ == "__main__":
    #user = User.create_account("exampleuser200", "examplepassword200")
    quiz = QuizApp()
    quiz_chunk = quiz.create_question_chunk()
    quiz.run()
    print(quiz_chunk)




