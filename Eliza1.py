import re
import random
import math
"""
9/23/2021
Henry Trinh
CS 4242 NLP PA 1
Eliza the Career Counselor

Description:
The purpose of this Eliza program is to have the program talk to a student/you. 
The program will simulate a career counselor for a student at UMD. 
This program is a basic chatterbot. How this program works is the student/user will tell the Eliza program
a question or statement.Then the program will use their response and transform it into a question 
with the help of regular expressions.
The program also detects for gibberish and profanity from the user. 
Such as:

UserInput: "I like pizza."
ElizaOutput: "Why you like pizza?"

Will keep going as long as the user inputs a response to the program. 

Potential Output:
[eliza] Nice to meet you, what's your name?
[user ] My name is Henry.
[eliza] Hello Henry! Could you explain why your here?
[user ] I am here to find love.
[eliza] Why are you here to find love?
[user ] I am lonely.

Usage Instruction:
    1. Make sure that python and python compiler is installed on the computer
    2. If using an IDE then have the program open and compile/run the program.
       If using an terminal then compile this "Eliza.py" and run.
    3. The program will ask your name. Enter your name into the "[user ]" box.
    4. The program will keep responding as long as the user enters something in the "[user ]" textbox.
    5. Type bye or goodbye to exit the program.

Algorithms used:
    Note:
    The function names will appear and be spaced out for clarity
    such as main() is at the otter edge since it's the first function you encounter.

    Eliza Response Algorithm
    main()
    1. Eliza Program will ask for the user's name.

    2. Then a while loop will run until the user enters bye or goodbye into the input box. 

    3. Inside the while loop is the function elizaResponds.
        4. First will run through the user's message and check from each word for gibberish with the elizaGibDet function,
           If gibberish is found then return the appropriate response. Otherwise continue.

        elizaresponds()
        5. elizaResponds will take the user's input into a loop that will check 
           for regular expression pattern matching to the inputted string.

        6. It will check for profanity of the user's message, 
           if found then will return a appropriate response.

        7. Otherwise, will find a regular expression pattern from the a_elizaDict dictionary.

        8. After a match have been found, 
           return a random response from the a_elizaDict dictionary of the regular expression pattern.

        10. Save the random response in a variable. 

        11. Then the algorithm will grab the regular expression pattern groups and run those groups
           into a loop with elizaReflection().

            elizaReflection()
            12. Then take the user's message  and run it into a loop with elizaReflection for each word.

                13. If the word is in the list of a_elizaReflectDict dictionary then switch it

                14. Then return the reflected user's message out.

        15. After those groups are made they are then injected with .format() into the the random response variable.

        16. Then will check for extra punctuation and make fixes. 

        17. Print out the response out to the user.

        18. Repeat until user enter's bye or goodbye. 

Links used: 
    1.https://medium.com/understand-the-python/understanding-the-asterisk-of-python-8b9daaa4a558 
        -This link helped myself some more python string manipulations. I learned that python can for loop with in
        the operator "*". This had helped me as I was not capturing groups correctly with my previous methods of not
        replacing the placeholder symbols to the user's message for the program.

    2.https://www.omnicalculator.com/other/password-entropy
        -This linked helped myself make a gibberish detection. I used this link to understand how to calculate
        the entropy which is the randomness of the object. I used the forumla and figured out how many characters are there.

"""

# Responses from eliza
a_elizaDict = {
    #Profanity Filter matches any partial words that are in the list
    r'.*(fuck|shit|bitch|stupid|ass|hell).*': ["That isn't very nice. Please refrain from any more foul language.",
                                               "I am merely your career counselor, not your punching bag!",
                                               "No wonder your here. Now tell me what you need you ruffian.",
                                               "You really need to stop. What would your mother say about this?",
                                               "I don't get paid enough for this. Can you tell me why your even here?"],
    #Regex that goes until the first punctation
    r'My name is ([^.!?]+)': ["Hello, {0}! What is your major?",
                              "Greetings {0}, Could you please tell me why your here?",
                              "It's a pleasure to meet you {0}, What brings you here today?"],

    r'What (.*)': ["What do you think about this?",
                   "Maybe you can google it?"],

    r'How to (.*)': ["How does {} makes you feel?", "Oh, Does {} do anything?"],
    #Regex that goes until the first punctation
    r'Why (can|can\'?t) ([^.!?]+)': ["Please explain why {0} {1}.",
                                     "Could you think of a reason why {} {}?"],
    #These regex look for any combination of here|seeking) (for|looking) with the | operator
    r"I am (here|seeking) (for|looking) (.*)": ["Please tell me more on why you need {2}?",
                                            "Tell me more about {2}."],

    r"I am a (.*) major": ["Oh cool, please tell me more about {} major?",
                         "Can you explain more of {}?",
                         ],

    r"(I am)(.*)": ["Why do you think {0} {1}?",
                         "Can you explain more of why {0} {1}?",
                         ],
    r'.*favorite thing about (.*)': ["Can you explain more of {}?",
                                     "That's very interesting. Please go on about {}."],
    r'It gives (.*)': ["Why does {}?",
                       "Explain more of {}?"],

    r'I like (.*)': ["Please explain why you like {}.",
                     "Is there anything you like about {}?"],
    r'I just told (.*)' : ["PLease explain why you just {}?",
                      "I see. Explain more about it."],
    r'I can\'?t (.*)': ["Maybe soon you can {}.",
                        "How soon you think you can {}?",
                        "Do you believe you can {}?"],

    r'I need (.*)': ["Why do you need {}?",
                     "Do you really think you need {}?"],

    r'I want to become a (.*)': ["Whats stopping you from being a {}?",
                     "Do you really think you need to be a {}?"],

    r'I want to (.*)': ["Whats stopping you from {}?",
                     "Do you really think you need {}?"],

    r'I think (.*)': ["Why do you think {}?",
                      "Does thinking this affect you?",
                      "How often do you think of {}?"],

    r'.*I thought about (.*)' :["Why do you think about {}?",
                              "How do you feel about {}?"],

    r'.*I never thought about (.*)' :["Why do you think you never thought about {}?",
                                    "How does not thinking about {} affect you??"],

    r'I graduate in the (.*)' : ["How do you feel about graduating in the {}?",
                                 "You can't wait to graduate in the {}?"],
    #Regex that goes until the first punctation
    r'My major is ([^.!?]+)': ["{} is very interesting. Could you tell me more about it?",
                               "Is there a reason why you choose {}?",
                               "What's your favorite thing about {}?"],
    #Regex that have 3 options to be the pattern
    r'The major I (picked|chose|choose) is ([^.!?]+)': ["{1} is very interesting. Could you tell me more about it?",
                                                        "Is there a reason why you choose {1}?",
                                                        "What's your favorite thing about {1}?"],

    r'(.*)major(.*)': ["That's very interesting, ",
                       "Tell me more about your major?",
                       "How does the major make you feel?"
                       ],

    r"I don't know(.*)": ["What don't you know about {}?",
                          "Could you elaborate what you don't know about {}?",
                          "Please tell me what don't you know about {}."],

    r"(.*)I don't(.*)": ["Why don't you {1}?",
                        "How do you feel about not {1}?"],

    r'because I (.*)'   :["Why would you {}?",
                          "Is there a reason why you say {}?"],

    r'(.*)student' : ["How do you feel about your study?",
                      "Please tell me more about being a student."],

    r'(.*)college(.*)' : ["How do you feel about your college?",
                      "Getting college done is important for you."],
    #Regex that have 3 options to be the pattern
    r'(.*)(jobs|applying|job)(.*)': ["Why don't you tell me about jobs?",
                                "What do you mean by jobs?",
                                "You should start looking at jobs!"],

    r'(.*)resume(.*)': ["Could you tell me what's a resume?",
                        "What about your resume?",
                        "A resume is very important to have. Have you made yours?"],

    r'(.*)career(.*)': ["What about your career?",
                        "A career is important in life. What career are you thinking of?",
                        "We can talk about your career in due time."],

    r'(.*)living(.*)': ["Where are you living now?",
                       "Living is important. So how do you live?",
                       "How does money affect you?"],

    r'(.*)money(.*)': ["Money is essential to live. You should get some.",
                       "What do you think about money?",
                       "How would you get money?"],

    r'(.*)debt(.*)': ["How would you pay off your debt?",
                      "How does the debt make you feel?"
                      ],
    r'(.*)vent(.*)' : ["Its okay, keep going that's why I'm here.",
                       "I'm listening, please go on.",
                       "No matter what I want you to know that you are loved."],

    r'Not yet.*' : ["Maybe soon you could?",
                    "I know you can do it. Any other questions?"],

    r'(.*)sorry(.*)' : ["Why are you sorry?",
                        "It's going to be alright, lets continue the session."],


    r'yes(.*)' : ["I see. Is there anything else?"],
    #These regex needs to be an exact match
    r'^yes+$' : ["Please explain why you say yes?"],
    r'^okay+$' : ["Any other questions?"],
    r'^no+$' : ["Please explain why you say no?"],

    r'(.*)':
        ["Please continue. I am intrigued.",
         "I see. Is there anything else?",
         "{}?",
         "Could you elaborate?",
         "Do you want to talk about this?",
         "Are you on track to graduate?",
         "Do you have a job lined up?",
         "What are your finances?",
         "How much debt do you have?",
         "Tell me more.",
         "Is your resume updated?"
         ],
}

# Dictionary for changing words
a_elizaReflectDict = {
    "am": "are",
    "are": "am",
    "my": "your",
    "you": "me",
    "your": "my",
    "me": "you",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "was": "were",
    "myself": "yourself",
    #"I": "you",
    "You" :"me",
}

"""
    elizaGibDet

    Description:
    This function will take the userMessage(String) and calculate 
    the entropy. 
    The function will take put the userMessage 
    If the entropy number is higher then a certain amount then
    return True(boolean) that the user's message is gibberish

    @:param String userMessage
    @:return boolean
"""


def elizaGibDet(userMessage):
    elizaGibResponse = ["I do not understand. Could you explain again?",
                        "What now? I do not understand.",
                        "That is gibberish. Please try again."]
    # Seperates the userMessage into single words
    userMessage2 = userMessage
    userSplitMessage = userMessage2.split()
    # Takes the words into a loop and check for each word of the type of characters they are
    for currentString in userSplitMessage:
        # Length of the single word
        stringLength = len(currentString)
        temp = currentString
        numCharSet = 0

        # Checkers for characters types
        #The \s\S with +$ makes anything inside the groups to be exact
        if re.match('\s\S[0-9]+$', temp):
            numCharSet = 10
        elif re.match('\s\S[a-z]+$', temp):
            numCharSet = 26
        elif re.match('\s\S[A-Z]+$', temp):
            numCharSet = 26
        elif re.match('\s\S[A-Za-z]+$', temp):
            numCharSet = 26 + 26
        elif re.match('\s\S[A-Za-z0-9]+$', temp):
            numCharSet = 26 + 26 + 10
        elif re.match('\s\S[A-Z0-9]+$', temp):
            numCharSet = 26 + 10
        elif re.match('\s\S[a-z0-9]+$', temp):
            numCharSet = 26 + 10
        else:
            numCharSet = 26 + 26 + 10 + 33

        # Entrophy forumla
        entrophyNumber = math.log2(numCharSet ** stringLength)

        #Entrophy limit if exceeds then print out a response that its gibberish
        if entrophyNumber > 75:
            #print(entrophyNumber)
            elizaPrint(random.choice(elizaGibResponse))
            return True
        else:

            return False
"""
    elizaReflection
    
    Description:    
    This function will take the userMessage(String) and switch the words out
    from the a_elizaReflectDict dictionary. 
    Rejoins the strings back together.

    @:param userMessage
    @:return String userOut
"""


def elizaReflection(userMessage):
    userOut = []
    # Takes the userMessage and split and lower all the words
    # The reason is because the dictionary will look through and help
    userSplitMessage = userMessage.lower().split()
    for currentString in userSplitMessage:
        if currentString in a_elizaReflectDict:
            userOut.append(a_elizaReflectDict[currentString])
        else:
            userOut.append(currentString)
    return ' '.join(userOut)


"""
    elizaRespond

    Description:
    This function will take the userMessage(String) and runs through the 
    dictionary for a regex pattern. 
    Then uses the dictionary in the program to find a regex match and get a random response.
    Then uses the user's input and switch the words with the elizaReflectDict dictionary.
    Then inserts the words into the capture groups fo the response.
    Prints out the response.

    @:param String userMessage
    @:return 0

"""


def elizaRespond(userMessage):
    # Runs through the list of keywords
    if not (elizaGibDet(userMessage)):
        for i in a_elizaDict:
            # If found a match from the list return True
            if re.match(i, userMessage, re.I):
                messageMatch = re.match(i, userMessage, re.I)
                # Gets a random response from the dictionary list of the pattern
                elizaRep = random.choice(a_elizaDict[i])

                # Will look through for groups from the regex and if found run it into the reflection and insert them into the random response
                elizaOutput = elizaRep.format(*[elizaReflection(groupNumber) for groupNumber in messageMatch.groups()])

                # Handles miss punctation
                if elizaOutput[-2:] == "?.":
                    elizaOutput = elizaOutput[:-2] + "."

                if elizaOutput[-2:] == "!.":
                    elizaOutput = elizaOutput[:-2] + "."

                if elizaOutput[-2:] == "..":
                    elizaOutput = elizaOutput[:-2] + "."

                if elizaOutput[-2:] == "??":
                    elizaOutput = elizaOutput[:-2] + "?"

                if elizaOutput[-2:] == "!?":
                    elizaOutput = elizaOutput[:-2] + "?"

                if elizaOutput[-2:] == ".?":
                    elizaOutput = elizaOutput[:-2] + "?"

                # Output
                elizaPrint(elizaOutput)
                break
    return 0


"""
    elizaPrint

    Description:
    This function will take the statement(string) and add
    a little [eliza] box with the statement following. 
    Used for styling for the user to know which response is theirs and eliza\

    @:param String statement
    @:return 0
"""


def elizaPrint(statement):
    print("[eliza] " + statement)


"""
    main()

    Description:
    This function will take the userMessage(String) and switch the words out
    from the a_elizaReflectDict dictionary. Will exit if the user enters bye or goodbye

    @:param none
    @:return none
"""
if __name__ == "__main__":
    elizaPrint("Hi, I'm Eliza the Career Counselor. I'm a chatbot written by Henry Trinh.")
    elizaPrint("What is your name?")
    while (True):
        userInput = input("[user ] ")
        # Exit condition
        if userInput == "bye" or userInput == "goodbye":
            elizaPrint("Have a wonderful day!")
            break
        elif len(userInput) > 0:
            elizaRespond(userInput)
        else:
            elizaPrint("Why are you quiet? I don't bite.")
