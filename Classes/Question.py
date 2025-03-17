import os
import json

class Question:
    def __init__(self, q_id, topic, label, marks):
        self.__q_id = q_id
        self._topic = topic
        self.__label = label                        # short or long 
        self.__marks = marks                        # total number of marks for question
         
       
