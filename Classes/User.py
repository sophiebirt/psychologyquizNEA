import json
import os

## TODO:
# -> hashing
# -> input validation 


class User:
    def __init__(self, name, password, seen_questions= None, weakest_topics = None):
        self.__name = name
        self.__password = password
        self.__seen_questions = seen_questions if seen_questions else []
        self.__weakest_topics = weakest_topics if weakest_topics else []

    def login():
        # check login details and create and return user obj
        pass

    def to_dict(self):
        return {
            "name": self.__name,
            "password": self.__password,
            "seen_questions": self.__seen_questions,
            "weakest_topics": self.__weakest_topics 
        }

    ## SOPHIE TODO: 
    # -> add in input validation, minimum length for username and password, no punctuation in username, etc 
    @staticmethod
    def create_account(name, password, file_path="userData.json"):
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

        # add our new user data
        data.append(user_data)

        # write back to the file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        return user
    
    @staticmethod
    def login(name, password, file_path="userData.json"):
        # check if the file path exists
        if os.path.exists(file_path):
            print("No user data found")
            return None
    
        # Load existing users 
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Linear search (this can and should be improved later with hashing)

        print(data)
        for u in data:
            if u["name"] == name and u["password"] == password:
                print(">>> Login Successful <<<")
                user = User(u["name"], u["password"], u["seen_questions"], u["weakest_topics"])
                return user

        print(">>> Invalid Username or Password <<<")
        return None