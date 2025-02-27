from tkinter import * 
from tkinter import messagebox
from tkinter import scrolledtext
import tkinter as tk
import json 
import random
import http.client
import json

# ---- GUI OOP ----

# add encapsulation - for oop reasons
# fix long answer questions (currently doesnt show entry box)
# remove any unecessary print statements

class App(Tk): # Parent GUI class
    def __init__(self):
        super().__init__()
        self.title("Psychology Quiz")


        # -- Attributes -- 

        self.welcomeScreen = None

        self.welcomeScreen = welcomeFrame(self)

        self.generateWelcomeScreen() 

    # -- Methods -- 
    def generateWelcomeScreen(self): 
        if hasattr(self, 'quizFrame') and self.quizFrame.winfo_ismapped(): 
            self.quizFrame.pack_forget()  # If quiz frame exists, hide it

        self.welcomeScreen.pack()  # Show welcome frame

    def generateQuizScreen(self):
        self.quizScreen = quizFrame(self)
        self.welcomeScreen.pack_forget()  # If welcome frame exists, hide it
        self.quizScreen.pack()  # Show quiz screen


    def hideWelcomeScreen(self):
        welcomeFrame.forget()

    def userDataLoad(self, passedUsername): #Loads user's data based on username
            with open ("userData.json") as f:
                data = json.load(f)
            userEntry = next((u for u in data["users"] if u["username"] == passedUsername), None)
            self.userData = userEntry

    welcomeLabel = Label(text = "Psychology Adaptive Quiz", font="Helvetica")

    username = ""

class welcomeFrame(Frame): # Frame that shows upon opening the program - has login / create account screen
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.pack(pady=20) # Packing the welcome frame itself onto screen 

        # -- Attributes -- 

        # Title label
        self.titleLabel = Label(self, text = "Psychology Adaptive Quiz", font="Helvetica")
        self.titleLabel.grid(row=0, column = 1)

        # Entry box for username
        self.entryUser = Entry(self, width=50, bg="light green")
        self.entryUser.grid(row=2, column=1)

        # Entry box for password
        self.entryPassword = Entry(self, width=50, bg="light green")
        self.entryPassword.grid(row=4, column=1)

        # Label prompting username entry
        self.labelUser = Label(self, text="Enter your username:")
        self.labelUser.grid(row=1, column=1)

        # Label prompting password entry
        self.labelPassword = Label(self, text="Enter your password:")
        self.labelPassword.grid(row=3, column=1)

        # Button for submitting username + password
        self.submitButton = Button(self, text="Submit", command=self.submitClick, bg="green")
        self.submitButton.grid(row=5, column =1)

        # Button for switching to the new account screen
        self.newAccountButton = Button(self, text="Create new account", command=self.swapGUI, bg="green")
        self.newAccountButton.grid(row=6, column =1)

    # -- Methods -- 
        
    def submitClick(self): # Prodecure for clicking 'Submit' button whilst on home screen
        myLabel = Label(self, text="Success!")
        self.parent.username = self.entryUser.get()
        self.password = self.entryPassword.get()
        currentColour = self.entryUser.cget("bg")
        if currentColour == "light pink": #If on the new account screen, create a new account
            self.createNewAccount(self.parent.username, self.password)

        else: # Check username and password against the database to see if account exists
            self.userDetailsCheck(self.parent.username, self.password)

    def userDetailsCheck(self, submittedUsername, submittedPassword): # Checks user's details to see if they are correct or incorrect, then displays appropriate message
        with open("userDetails.json") as f:
            userDetails = json.load(f)
        counter = 0
        for detail in userDetails['userDetailsDict']:
            counter = counter + 1
            if detail['username'] == submittedUsername and detail['password'] == submittedPassword:
                messagebox.showinfo("Login success", "User login success. Loading your data")
                self.parent.userDataLoad(submittedUsername)
                self.parent.generateQuizScreen()
                return
    
        messagebox.showinfo("Login failed", "User login failed. Please try again or create a new account")


    def swapGUI(self): #Used to swap between the GUIs in the login screen
        currentColour = self.entryUser.cget("bg")
        if currentColour == "light green": # Login screen --> new account screen
            self.entryUser.config(bg="light pink")
            self.entryPassword.config(bg="light pink")
            self.submitButton.config(bg="light pink")
            self.newAccountButton.config(bg="light pink", text="Back to login page")

        elif currentColour == "light pink": # New account screen --> login screen
            self.entryUser.config(bg="light green")
            self.entryPassword.config(bg="light green")
            self.submitButton.config(bg="light green")
            self.newAccountButton.config(bg="light green", text="Create new account")

    
        
    def createNewAccount(newUsername, newPassword): # Creating a new account
        newUser = {"username": newUsername, "password": newPassword}
        with open("userDetails.json") as f: # User details file
            userDetails = json.load(f)

        for user in userDetails["userDetailsDict"]: # Checks if user already exists
            if user["username"] == newUsername:
                print ("User with this name already exists. Please try again with a new username.")
                return

        userDetails["userDetailsDict"].append(newUser) # Setting new details
        with open("userDetails.json", "w") as f: # Writing new details to userDetails 
            json.dump(userDetails, f, indent=4)

        with open("userData.json") as f: # User data file
            userData = json.load(f)

        # Template for creating a new user in the userData.json file
        newUserTemplate = { 
            "username": newUsername,
            "weakestTopics": "",
            "weakestQuestionType": "",
            "numberQsSeen": 0,
            "seenQs": ""
        }

        # Appends the new user
        userData["users"].append(newUserTemplate)

        # Adds + saves it to the file
        with open("userData.json", "w") as f:
            json.dump(userData, f, indent=4) 
    

        messagebox.showinfo("Account created", f"Account created with username {newUsername} and password {newPassword}")

class quizFrame(Frame): # Frame used for the quiz element of the program 
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.pack(pady=50) # Packing the quiz frame itself onto screen 
        self.configure(width=1000, height=1000)
        self.update_idletasks()

        # -- Attributes -- 
        
        # Displays the question
        self.questionLabel = Label(self, text="QUESTION PLACEHOLDER VALUE", bg="light green", wraplength=300, justify="center")
        self.questionLabel.place(x=270, y=100, width=300, height=100)

        # Displays feedback
        self.feedbackLabel = Label(self, text="Feedback will appear here once answer is submitted", bg="light green", wraplength=300, justify="center")
        self.feedbackLabel.place(x=460, y=250, width=300, height=200)

        # Displays the button to submit answer
        self.submitAnswerButton = Button(self, text="Submit Answer", command=self.submitAnswer, bg="green")
        self.submitAnswerButton.place(x=360, y=450)

        # Entry for long answer questions
        self.answerEntry = scrolledtext.ScrolledText(self,  
                                      wrap = tk.WORD,  
                                      width = 40,  
                                      height = 3,  
                                      font = ("Helvetica", 
                                              15))         

        # Entries for the short answer GUI 
        self.entryBox1 = Entry(self, width=30)

        self.entryBox2 = Entry(self, width=30)

        self.entryBox3 = Entry(self, width=30)

        # Label with instructions on how to do the short answer question
        self.instructionsLabel = Label(self, text="Fill in the gaps and press submit when you're done.", bg="light green", wraplength = 300, justify="center")

        # Displays the ideal answer with gaps to the user during short answer questions
        self.templateBox = Label(self, height=8, width=40, text="", bg="light green", wraplength=200, justify="center")
        self.templateBox.place(x=50, y=230)

        # Next question button
        self.nextButton = Button(self, text="Next question", command=self.nextQuestion, bg="green")

        self.nextQuestion()


    # -- Methods --
    def clearForNextQuestion(self):
        self.entryBox1.forget()
        self.entryBox2.forget()
        self.entryBox3.forget()
        self.instructionsLabel.forget()
        self.nextButton.forget()
        self.answerEntry.place_forget()
        self.feedbackLabel.config(text="")

    def nextQuestion(self): # Procedure for generating a new question
        userData = self.parent.userDataLoad(App.username)
        if userData["numberQsSeen"] < 10: # If user has seen over 10 questions
            chance = random.randint(1, 2) # Randomise between seen and unseen
            chance = 2 # TEMPORARY - DELETE LATER
            self.clearForNextQuestion()
            if chance == 1:
                self.seen(userData)
            else:
                self.unseen(userData)

    def generateShortAnswerGUI(self): # Main procedure involved in generating short answer GUI
        numEntries = int(self.selectedQuestion["answerEntries"])
        self.answerEntry.place_forget()
        self.instructionsLabel.place(x=55, y=350)
        self.templateBox.config(text=self.selectedQuestion["answerTemplate"])

        # Generating correct number of entry boxes based on the number of gaps in the question

        if numEntries == 1:
            self.entryBox1.place(x=50, y=375)

        elif numEntries == 2:
            self.entryBox1.place(x=50, y=375)
            self.entryBox2.place(x=50, y=400)

        elif numEntries == 3:
            self.entryBox1.place(x=50, y=375)
            self.entryBox2.place(x=50, y=400)
            self.entryBox3.place(x=50, y=425)

    def submitAnswer(self): #Procedure for clicking the 'Submit' button on the quiz screen
        keywords = []
        self.nextButton.place(x=750, y=450)

        if int(self.selectedQuestion["TM"]) > 6: #If over 6 marks, use the AI to generate feedback
            userAnswer = self.answerEntry.get("1.0", tk.END)
            self.getAIfeedback(userAnswer)

        else: #If under 6 marks, use the short answer procedure to generate feedback
            numEntries = int(self.selectedQuestion["answerEntries"])
            print (numEntries)
            
            if numEntries == 1:
                keywords.append(self.entryBox1.get())

            elif numEntries == 2:
                keywords.append(self.entryBox1.get())
                keywords.append(self.entryBox2.get())

            else:
                keywords.append(self.entryBox1.get())
                keywords.append(self.entryBox2.get())
                keywords.append(self.entryBox3.get())

                self.checkShortAnswer(keywords, numEntries)

    def getAIfeedback(self, userAnswer): #Gets AI feedback from user's answer 
    
        conn = http.client.HTTPSConnection("chat-gpt26.p.rapidapi.com")
    
        #Prompt to give to chatGPT 
        prompt = ("I have answered the following question:\n" 
            "{}"
            "Mark it with an integer number of marks out of {}\n at the start of your response"
            "This is my answer: {}\n"
            "An answer with no input should get no marks\n"
            "And then give me advice on how to improve the answer\n"
            "Keep the advice concise, ideally between 50 and 100 words").format(self.selectedQuestion["question"], self.selectedQuestion["TM"], userAnswer)

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
        self.feedbackLabel.config(text=response) # The AI's response is inserted into feedback label

    def checkAnswer(self, keywordsList, counter, answerNumber): #Assists in checking the short answer entered by the user
        cText = self.feedbackLabel.cget("text")
        if keywordsList[counter] == self.selectedQuestion["answer{}".format(counter+1)]: # Checking if the correct keyword matches with the user's answer
            self.feedbackLabel.config(text=cText+"Answer {} correct, ".format(counter+1)) # Altering feedback label based on result

        else:
            self.feedbackLabel.config(text=cText+"Answer {} incorrect, ".format(counter+1))

    def checkShortAnswer(self, keywordsList, numberEntries): 
        self.feedbackLabel.config(text="")
        numberLoops = self.selectedQuestion["answerEntries"] # For amount of possible answers, continue looping
        for i in range(0, numberLoops):
            answerNumber = str(i+1)
            self.checkAnswer(keywordsList, i, answerNumber)
    
    def seen(self, userData):
        pass # fix this

    def generateUnseenQ(self, questions, seenQuestions): # Generates unseen question
        while True: # Loops until it finds an unseen question
            self.selectedQuestion = random.choice(questions["questionsList"])  
            if self.selectedQuestion["questionNo"] not in seenQuestions: 
                return self.selectedQuestion 
            
    def unseen(self, userData): #Procedure for an unseen question
        with open ("questions.json") as f:
            questions = json.load(f)

        influencedGenerator = random.randint(1,2) # 1 = influenced, 2 = non-influenced
        influencedGenerator = 2 # DELETE THIS LATER
        
        if influencedGenerator == 1: 
            pass # fix this later

        elif influencedGenerator == 2: # Non-influenced
            seenQuestions = userData.get("seenQs", []) 
            self.selectedQuestion = self.generateUnseenQ(questions, seenQuestions) 

        self.questionLabel.config(text=self.selectedQuestion["question"]) # Changing question label to display the question
        if int(self.selectedQuestion["TM"]) < 6: #Total marks less than six, use short answer GUI 
            self.generateShortAnswerGUI()    

        else: #Total marks more than six, use long answer GUI
            self.clearForNextQuestion()
            self.feedbackLabel.forget() 
            self.answerEntry.place(x=50, y=300, width=300, height=150)

    

# ---- PROGRAM START ----
app = App()
app.mainloop()
