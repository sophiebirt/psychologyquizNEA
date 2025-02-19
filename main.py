from tkinter import * 
from tkinter import messagebox
from tkinter import scrolledtext
import tkinter as tk
import json 
import time
import random
import http.client
import json

global root
root = Tk()  


# ---- GUI SUBROUTINES ----

def generateWelcomeScreen(): #done
    spawnEntryUser()
    spawnEntryPassword()
    spawnLabelUser()
    spawnLabelPassword()
    spawnWelcomeLabel()
    spawnSubmitButton()
    spawnNewAccountButton()

def spawnEntryUser(): 
    # Entries for username and password
    global entryUser # remove later
    entryUser = Entry(root, width=50, bg="light green")
    entryUser.grid(row=2, column=1)
    return entryUser 

def spawnEntryPassword():
    global entryPassword # remove later
    entryPassword = Entry(root, width=50, bg="light green")
    entryPassword.grid(row=4, column=1)
    return entryPassword

def spawnLabelUser(): # Label prompting username entry
    global labelUser # remove later
    labelUser = Label(root, text="Enter your username:")
    labelUser.grid(row=1, column=1)
    return labelUser

def spawnLabelPassword(): # Label prompting password entry
    global labelPassword # remove later
    labelPassword = Label(root, text="Enter your password:")
    labelPassword.grid(row=3, column=1)
    return labelPassword

def spawnWelcomeLabel():
    # Welcome label to be displayed at the top of the screen
    global welcomeLabel
    welcomeLabel = Label(root, text = "Psychology Adaptive Quiz", font="Helvetica")
    welcomeLabel.grid(row=0, column = 1)
    return welcomeLabel

def spawnSubmitButton():
    # Buttons for submitting username/passwords and for switching to the new account screen
    global submitButton
    submitButton = Button(root, text="Submit", command=submitClick, bg="green")
    submitButton.grid(row=5, column =1)
    return submitButton

def spawnNewAccountButton():
    global newAccountButton
    newAccountButton = Button(root, text="Create new account", command=swapGUI, bg="green")
    newAccountButton.grid(row=6, column =1)
    return newAccountButton

def hideHomeScreen(): # Used to hide the home screen in preparation for generating the quiz screen
    labelUser.destroy() 
    labelPassword.destroy()
    entryUser.destroy()
    entryPassword.destroy()
    submitButton.destroy()
    newAccountButton.destroy()
    welcomeLabel.forget()
    root.geometry("850x500")
    

def generateLongAnswerGUI():
    global answerEntry

    answerEntry = scrolledtext.ScrolledText(root,  
                                      wrap = tk.WORD,  
                                      width = 40,  
                                      height = 10,  
                                      font = ("Helvetica", 
                                              15)) 
    
    answerEntry.place(x=50, y=250, width=300, height=200)
   
def spawnEB1(): # Entry box 1 for short answer GUI 
    global entryBox1
    entryBox1 = tk.Entry(root, width=30)
    entryBox1.place(x=50, y=375)

def spawnEB2(): # Entry box 2 for short answer GUI 
    global entryBox2
    entryBox2 = tk.Entry(root, width=30)
    entryBox2.place(x=50, y=400)

def spawnEB3(): # Entry box 3 for short answer GUI 
    global entryBox3
    entryBox3 = tk.Entry(root, width=30)
    entryBox3.place(x=50, y=425)

def spawnShortAnswerInstructions(): # Gives additional info on how to use the short answer GUI
    global instructionsLabel 
    instructionsLabel = Label(root, text="Fill in the gaps and press submit when you're done.", bg="light green", wraplength = 300, justify="center")
    instructionsLabel.place(x=55, y=350)

def generateShortAnswerGUI(): # Main procedure involved in generating short answer GUI
    answerEntry.destroy() # Removes entry box for long answer questions 
    numEntries = int(selectedQuestion["answerEntries"])
    
    spawnShortAnswerInstructions()

    # Generating correct number of entry boxes based on the number of gaps in the question
    if numEntries == 1:
        spawnEB1()

    elif numEntries == 2:
        spawnEB1()
        spawnEB2()

    elif numEntries == 3:
        spawnEB1()
        spawnEB2()
        spawnEB3()

    # Displays the ideal answer with gaps to the user
    templateBox = tk.Label(root, height=8, width=40, text=selectedQuestion["answerTemplate"], bg="light green", wraplength=200, justify="center")
    templateBox.place(x=50, y=230)

def spawnNextButton(): #Spawns the next button once the user has submitted an answer to the existing question
    global nextButton
    nextButton = Button(root, text="Next question", command=next(), bg="green")
    nextButton.place(x=750, y=450)


def generateQuizScreen(): #Generates the quiz screen
    global feedbackLabel
    global questionLabel

    generateLongAnswerGUI()

    feedbackLabel = Label(root, text="Feedback will appear here once answer is submitted", bg="light green", wraplength=300, justify="center")
    feedbackLabel.place(x=460, y=250, width=300, height=200)

    questionLabel = Label(root, text=" ", bg="light green", wraplength=300, justify="center")
    questionLabel.place(x=270, y=100, width=300, height=100)
    
    submitAnswerButton = Button(root, text="Submit Answer", command=submitAnswer, bg="green")
    submitAnswerButton.place(x=360, y=450)

# ---- NON GUI SUBROUTINES ----

def startQuiz(): # Starts the quiz
    userData = userDataLoad() 
    hideHomeScreen()
    generateQuizScreen()
    welcomeLabel.place(x=300, y=50)
    unseen(userData)

def next(): # Procedure for generating a new question
    userData = userDataLoad()
    if userData["numberQsSeen"] < 10: 
        chance = random.randint(1, 2)
        if chance == 1:
            seen(userData)
        else:
            unseen(userData)
        
def createNewAccount(newUsername, newPassword): # Creating a new account

    newUser = {"username": newUsername, "password": newPassword}
    with open("userDetails.json") as f: # User details file
        userDetails = json.load(f)

    for user in userDetails["userDetailsDict"]:
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


def getAIfeedback(userAnswer): #Gets AI feedback from user's answer 
    
    conn = http.client.HTTPSConnection("chat-gpt26.p.rapidapi.com")
    
    #Prompt to give to chatGPT 
    prompt = ("I have answered the following question:\n" 
          "{}"
          "Mark it with an integer number of marks out of {}\n at the start of your response"
          "This is my answer: {}\n"
          "An answer with no input should get no marks\n"
          "And then give me advice on how to improve the answer\n"
          "Keep the advice concise, ideally between 50 and 100 words").format(selectedQuestion["question"], selectedQuestion["TM"], userAnswer)

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
    feedbackLabel.config(text=response) # The AI's response is inserted into feedback label

def checkAnswer(keywordsList, counter, answerNumber): #Assists in checking the short answer entered by the user
    cText = feedbackLabel.cget("text")
    if keywordsList[counter] == selectedQuestion["answer{}".format(counter+1)]: # Checking if the correct keyword matches with the user's answer
        feedbackLabel.config(text=cText+"Answer {} correct, ".format(counter+1)) # Altering feedback label based on result

    else:
        feedbackLabel.config(text=cText+"Answer {} incorrect, ".format(counter+1))


def checkShortAnswer(keywordsList, numberEntries): 
    feedbackLabel.config(text="")
    numberLoops = selectedQuestion["answerEntries"] # For amount of possible answers, continue looping
    for i in range(0, numberLoops):
        answerNumber = str(i+1)
        checkAnswer(keywordsList, i, answerNumber)
    

def submitAnswer(): #Procedure for clicking the 'Submit' button on the quiz screen
    keywords = []
    spawnNextButton()

    if int(selectedQuestion["TM"]) > 6: #If over 6 marks, use the AI to generate feedback
        userAnswer = answerEntry.get("1.0", tk.END)
        getAIfeedback(userAnswer)

    else: #If under 6 marks, use the short answer procedure to generate feedback
        numEntries = int(selectedQuestion["answerEntries"])
        print (numEntries)
        if numEntries == 1:
            keywords.append(entryBox1.get())

        elif numEntries == 2:
            keywords.append(entryBox1.get())
            keywords.append(entryBox2.get())

        else:
            keywords.append(entryBox1.get())
            keywords.append(entryBox2.get())
            keywords.append(entryBox3.get())

        checkShortAnswer(keywords, numEntries)


def seen(userData):
    global selectedQuestion
    
def generateUnseenQ(questions, seenQuestions): # Generates unseen question
    while True: # Loops until it finds an unseen question
        selectedQuestion = random.choice(questions["questionsList"])  
        if selectedQuestion["questionNo"] not in seenQuestions: 
            return selectedQuestion 
            
def unseen(userData): #Procedure for an unseen question
    global selectedQuestion
    with open ("questions.json") as f:
        questions = json.load(f)

    influencedGenerator = random.randint(1,2) # 1 = influenced, 2 = non-influenced
    influencedGenerator = 2 # DELETE THIS LATER
    #if influencedGenerator == 1: 

    if influencedGenerator == 2: # Non-influenced
        seenQuestions = userData.get("seenQs", []) 
        generateUnseenQ(questions, seenQuestions) # 

        questionLabel.config(text=selectedQuestion["question"]) # Changing question label to display the question

        if int(selectedQuestion["TM"]) < 6: #Total marks less than six, use short answer GUI 
            generateShortAnswerGUI()    

        else: #Total marks more than six, use long answer GUI
            generateLongAnswerGUI()    
    
def userDataLoad(passedUsername): #Loads user's data based on username
    with open ("userData.json") as f:
        data = json.load(f)

    for user in data["users"]:
        if user.get("username") == passedUsername:
            userData = user
    
    return userData


def userDetailsCheck(submittedUsername, submittedPassword): #Checks user's details to see if they are correct or incorrect, then displays appropriate message
    with open("userDetails.json") as f:
        userDetails = json.load(f)
    counter = 0
    for detail in userDetails['userDetailsDict']:
        counter = counter + 1
        if detail['username'] == submittedUsername and detail['password'] == submittedPassword:
            messagebox.showinfo("Login success", "User login success. Loading your data")
            userDataLoad(submittedUsername)
            return
            # Here would be where you load the user's profile
    
    messagebox.showinfo("Login failed", "User login failed. Please try again or create a new account")


def submitClick(): #Prodecure for clicking 'Submit' button whilst on home screen
    myLabel = Label(root, text="Success!")
    username = entryUser.get()
    password = entryPassword.get()
    currentColour = entryUser.cget("bg")
    if currentColour == "light pink": #If on the new account screen, create a new account
        createNewAccount(username, password)

    else: # Check username and password against the database to see if account exists
        userDetailsCheck(username, password)

def swapGUI(): #Used to swap between the GUIs in the login screen
    currentColour = entryUser.cget("bg")
    if currentColour == "light green": # Login screen --> new account screen
        entryUser.config(bg="light pink")
        entryPassword.config(bg="light pink")
        submitButton.config(bg="light pink")
        newAccountButton.config(bg="light pink", text="Back to login page")

    elif currentColour == "light pink": # New account screen --> login screen
        entryUser.config(bg="light green")
        entryPassword.config(bg="light green")
        submitButton.config(bg="light green")
        newAccountButton.config(bg="light green", text="Create new account")



# ---- PROGRAM START ----
generateWelcomeScreen()

root.mainloop()
