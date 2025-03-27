from Classes.User import User
from Classes.Question import Question
from Classes.SingleAnswer import SingleAnswer
from Classes.QuestionHandler import QuestionHandler
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


import customtkinter as ctk
import os
import json
import random
import math 

# Static
ACCOUNT_DATA = "Account\student_data.json" # this may vary depending on machine and dev environment 

class QuizApp():
    
    def __init__(self):
        
        # TKinter Data 
        self.__window = ctk.CTk()
        self.__window.title("Psychology Quiz")
        self.__window.geometry("600x400")

        # Question Data 
        self._question_handler = QuestionHandler()
        self.__single_answer_qs = self._question_handler.create_single_answer_question_objects()
        self.__multiple_choice_qs = self._question_handler.create_multiple_choice_question_objects()
        self.__extended_answer_qs = self._question_handler.create_extended_answer_question_objects()

        print(f"Lengths - SA: {len(self.__single_answer_qs)}, MC: {len(self.__multiple_choice_qs)}")


        self.__all_questions = [
            self.__single_answer_qs, 
            self.__multiple_choice_qs,
            self.__extended_answer_qs
        ]

        # User Data 
        self.__user = None # this is a user object 

        self.create_login_page()

    def create_pie_chart(self, data):
        """Creates a pie chart from a dictionary and embeds it in the Tkinter window."""
        if not data:
            return  # No data to plot

        # Extract labels and values
        labels = list(data.keys())
        sizes = list(data.values())

        # Create Matplotlib Figure
        fig = Figure(figsize=(4, 4))
        ax = fig.add_subplot(111)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

        return fig

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


    def create_quiz_dashboard(self):
        """Creates the login page UI."""
        for widget in self.__window.winfo_children():
            widget.destroy()

        weakest_topics = self.__user.get_weakest_topics()
        questions_completed = self.__user.get_questions_completed()
        
        average_percentage_per_quiz = self.__user.get_quiz_percentages()

        # Title Label
        self.title_label = ctk.CTkLabel(self.__window, text="Welcome to Your Quiz Dashboard!", font=("Arial", 20, "bold", "underline"))
        self.title_label.pack(pady=20)
        
        # Weakest Topics
        self.weak_label = ctk.CTkLabel(self.__window, text=f"Weakest Topics: {weakest_topics}", font=("Arial", 16))
        self.weak_label.pack(pady=10)

        # Pie Chart - Show Weakest Topics
        topic_counts = weakest_topics
        if topic_counts:
            fig = self.create_pie_chart(topic_counts)
            if fig:
                canvas = FigureCanvasTkAgg(fig, master=self.__window)
                canvas.get_tk_widget().pack(pady=10)
                canvas.draw()


        # Total Questions Completed
        self.total_label = ctk.CTkLabel(self.__window, text=f"Total Questions Completed: {questions_completed}", font=("Arial", 16))
        self.total_label.pack(pady=10)
        
        # TODO AVERAGE QUIZ PERCENTAGE

        # Average score per quiz 
        self.average_marks_per_quiz_label = ctk.CTkLabel(self.__window, text=f"Average marks per quiz: {average_percentage_per_quiz}", font=("Arial", 16))
        self.average_marks_per_quiz_label.pack(pady=10)

        # Start Quiz Button
        self.start_button = ctk.CTkButton(self.__window, text="Start Quiz", command=self.run_quiz_chunk)
        self.start_button.pack(pady=20)

    def create_question_chunk(self):
        question_chunk = []

        for i in range(len(self.__all_questions)):
            # pick one random question from each 

            random_index = random.randint(0, len(self.__all_questions[i]) - 1)

            question_to_be_added = self.__all_questions[i][random_index]
            # TODO update the uses completed question list, check they havent already done it
            question_chunk.append(question_to_be_added)

        return question_chunk
    
    def ask_question(self, index):
        """Displays questions one at a time and waits for completion before moving to the next."""
        if index < len(self._question_chunk):  # Ensure there are questions left
            question = self._question_chunk[index]
            
            # Define a callback function to run when the question is answered
            def on_question_complete(marks_achieved, topic):
                correct = marks_achieved == question.get_marks()

                self.__total_potential_marks += question.get_marks()
                
                
                if correct:
                    self.__total_correct += 1
                    self.__total_quiz_marks += marks_achieved # MARKS ACHIEVED does not always equal the amount the question is worth
                else:
                    self.__failed_topics.append(topic)

                print(f"TOTAL POTENTIAL MARKS: {self.__total_potential_marks}")
                print(f"TOTAL QUIZ MARKS: {self.__total_quiz_marks}")
                print(f"QUESTION MARKS ACHIEVED: {marks_achieved}")
                
                # Move to the next question
                self.ask_question(index + 1)
            
            # Display the question and pass the callback
            question.display_question_page(
                quiz_object_window=self.__window, 
                current_question_number=index + 1, 
                total_number_of_questions=len(self._question_chunk),
                callback=on_question_complete  # Pass callback function
            )
        else:
            self.finish_quiz()  # If all questions are done, show results
    
    
    def run_quiz_chunk(self):
        print("=== STARTED QUIZ CHUNK ===")
    
        self._question_chunk = self.create_question_chunk()  # Store all questions
        self.__total_correct = 0            # Track correct answers (1 for each question)
        self.__failed_topics = []           # Track failed topics
        self.__total_quiz_marks = 0         # Track the total marks that are achieved
        self.__total_potential_marks = 0    # Track the total marks that could be achieved
        
        self.ask_question(0)  # Start with the first question
    
    def finish_quiz(self):
        """Displays quiz results after all questions are answered"""
        for widget in self.__window.winfo_children():
            widget.destroy()

        print(f"TOTAL QUIZ MARKS ACHIEVED: {self.__total_quiz_marks}")
        print(f"TOTAL POTENTIAL MARKS: {self.__total_potential_marks}")

        quiz_chunk_percentage = int(self.__total_quiz_marks/self.__total_potential_marks * 100)

        ctk.CTkLabel(self.__window, text="Quiz Completed!", font=("Arial", 20)).pack(pady=20)
        ctk.CTkLabel(self.__window, text=f"Total Correct: {self.__total_correct}", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(self.__window, text=f"Quiz Percentage Achieved: {quiz_chunk_percentage}", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(self.__window, text=f"Topics Failed: {', '.join(self.__failed_topics) if self.__failed_topics else 'None'}", font=("Arial", 16)).pack(pady=10)
       
        
        # Update user stats
        self.__user.increment_weakest_topics(self.__failed_topics)
        self.__user.increase_questions_completed(len(self._question_chunk))
        self.__user.update_quiz_percentages(quiz_chunk_percentage)
        self.__user.update_user_stats(ACCOUNT_DATA)

        self.start_button = ctk.CTkButton(self.__window, text="Back To Homepage", command=self.create_quiz_dashboard)
        self.start_button.pack(pady=20)

    def login(self):
        username = self.__username_entry.get()
        password = self.__password_entry.get()

        self.__user = User.login(username, password, ACCOUNT_DATA)

        if self.__user: 
            print(f"{self.__user.get_name()} has logged in!")
            self.create_quiz_dashboard()

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
        

if __name__ == "__main__":
    #user = User.create_account("exampleuser200", "examplepassword200")
    quiz = QuizApp()
    quiz_chunk = quiz.create_question_chunk()
    quiz.run()
    print(quiz_chunk)



