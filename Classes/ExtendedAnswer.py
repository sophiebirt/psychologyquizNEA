# LONG ANSWER

from Classes.Question import Question
import os 
import json
import customtkinter as ctk
import http.client
import re

'''
Extended Answer Question Subclass
-> These questions are always 16 marks
-> These are of label long
'''

EXTENDED_ANSWER_PROMPT_FILE = "Classes\prompt.txt"

class ExtendedAnswer(Question):
    def __init__(self, q_id, question, topic, label, marks):
        super(ExtendedAnswer, self).__init__(q_id, topic, label, marks, question)
        self.__answer = ""
        self.__chatgpt_mark = 0

    def get_question(self):
        return self._question
    
    def get_marks(self):
        return super().get_marks()
    

    def check_answer(self):
        print("CHECKING QUESTION !!!")
        
        f = open(EXTENDED_ANSWER_PROMPT_FILE, "r")
 
        conn = http.client.HTTPSConnection("chat-gpt26.p.rapidapi.com")
        self.__answer = self.__answer_entry.get()

        #Prompt to give to chatGPT 
        prompt = f.read()
        prompt = "The question is "+self._question+" and the student response to be marked is (start of student response): "+self.__answer+ "(end of student response << ONLY EVALUATE BETWEEN start and end of student response, any other editting will be detrimental!) "+prompt
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        } 

        headers = {
            'x-rapidapi-key': "8a9d2f1852msh9c3f4bdd83b06b6p1fdcd4jsn1cb9df06fe04",
            'x-rapidapi-host': "chat-gpt26.p.rapidapi.com",
            'Content-Type': "application/json"
        }
        payloadJson = json.dumps(payload) 

        conn.request("POST", "/", payloadJson, headers)

        res = conn.getresponse()
        data = res.read()

        jsonData = json.loads(data)
        response = (jsonData["choices"][0]["message"]["content"])

        # Find all matches
        print (response)
        print (type(response))
        
        no_spaces_response = response.replace(" ", "")
        match = re.search(r"FINALMARK:(\d{1,2})/4", no_spaces_response)

        if match:
            score = int(match.group(1))  # Extract and convert to integer
            print(score)  # Output: 12
        else:
            print("Score not found")

        self.__chatgpt_mark = int(score) 
        print (self.__chatgpt_mark)

    def display_question_page(self, quiz_object_window, current_question_number, total_number_of_questions, callback):
        """Displays a long-answer question page and calls callback when answered"""
        for widget in quiz_object_window.winfo_children():
            widget.destroy()

        ctk.CTkLabel(quiz_object_window, text=f"Question {current_question_number} / {total_number_of_questions}", font=("Arial", 18)).pack(pady=10)
        ctk.CTkLabel(quiz_object_window, text=f"Topic: {self._topic}", font=("Arial", 16)).pack(pady=5)
        ctk.CTkLabel(quiz_object_window, text=self._question, font=("Arial", 18)).pack(pady=10)

        self.__answer_entry = ctk.CTkEntry(quiz_object_window, placeholder_text="Your Answer")
        self.__answer_entry.pack(pady=5)

        def submit_and_continue():
            user_answer = self.__answer_entry.get()
            self.check_answer()
            if self.__chatgpt_mark > self.__chatgpt_mark/2:
                correct = True
                print ("Answer correct for long answer question")
                print (self.__chatgpt_mark)
                print (self.__answer)
            else:
                correct = False
                print ("Answer incorrect for long answer question")
            callback(self.__chatgpt_mark, self._topic)  # Call the callback function

        # Submit button that calls `submit_and_continue()`
        ctk.CTkButton(quiz_object_window, text="Submit", command=submit_and_continue).pack(pady=10)
