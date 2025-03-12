import json
import os

## TODO:
# -> hashing
# -> check user does not already exist




class User:
    def __init__(self, name, password, seen_questions= None, weakest_topics = None):
        self.__name = name
        self.__password = password

        self.__valid_username_length = 5
        self.__valid_password_length = 8

        # Stats Attributes:
        self.__questions_completed = 0
        self.__seen_questions = []
        self.__weakest_topics = []
        self.__completed_topics = [] 
        self.__quiz_scores = []
        self.__average_score_per_quiz = None
        

    def to_dict(self):
        return {
            "name": self.__name,
            "password": self.__password,
            "seen_questions": self.__seen_questions,
            "weakest_topics": self.__weakest_topics 
        }
    
    # user input validation - SOPHIE 
    def validate_username(self, username): 
        
        valid_length = len(username) >= self.__valid_username_length # is it longer than 5 chars?? 
        contains_punctuation = not username.isalnum()  

        if not valid_length: print(f"The length of {username} is not greater than {self.__valid_username_length}")
        
        valid_length
        
        return valid_length
    
    def validate_password(self, password): 
        valid_length = len(password) >= self.__valid_password_length    # is it longer than 8 chars?? 
        contains_number = any(char.isdigit() for char in password)      # are any of the characters digits?
        contains_punctuation = not password.isalnum()                       # any punctuation?

        # TODO 
        # -> Change this return the strings in print and display to UI 
        if not valid_length: print(f"The length of Password is not greater than {self.__valid_password_length}")
        if not contains_number: print(f"Password must contain a number")
        if not contains_punctuation: print(f"Password must contain punctuation")

        all_conditions = valid_length and contains_number and contains_punctuation
    
        return all_conditions

    @staticmethod
    def create_account(name, password, file_path):
        # Create object 
        user = User(name, password)
        user_data = user.to_dict()

        # update user Data.json

        # if we can find file, read it and store it as data
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
        # otherwise, say data is empty
        else:
            data = []

        if user.validate_username(name) and user.validate_password(password):
            # add our new user data
            data.append(user_data)
            print (">>> Account Successfully Created <<<")

        else:
            # Exit Function 
            return None


        # write back to the file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        return user
    
    @staticmethod
    def login(name, password, file_path):
        # check if the file path exists
        if os.path.exists(file_path):
            # Load existing users 
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            return None
    
        

        # Linear search (this can and should be improved later with hashing)

        print(data)
        for u in data:
            if u["name"] == name and u["password"] == password:
                print(">>> Login Successful <<<")
                user = User(u["name"], u["password"], u["seen_questions"], u["weakest_topics"])
                return user

        print(">>> Invalid Username or Password <<<")
        return None
    
    ## GETTER AND SETTER METHODS

    def get_name(self):
        return self.__name

    def get_questions_completed(self):
        return self.__questions_completed
    
    def get_weakest_topics(self):
        return self.__weakest_topics
    
    def get_completed_topics(self):
        return self.__completed_topics

    def get_average_score_per_quiz(self):
        return self.__average_score_per_quiz
