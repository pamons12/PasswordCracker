import hashlib
import math
from multiprocessing import Pool
from functools import partial
import time

#Defines the user class 
#Used to keep user information organized
class user:
    #Constructor that takes in information on the user
    def __init__(self,username,encryption,otherstuff,password):
        self.username = username
        self.encryption = encryption
        self.otherStuff = otherstuff
        self.password = password
    
    #Constructor that creates a user object with no info
    def __init__(self):
        self.username = ""
        self.encryption = ""
        self.otherStuff = ""
        self.password = ""
    
    #Sets up how a user object will be printed
    def __str__(self):
        return("Username: {}\nEncyrption: {}\nOther stuff: {}\nPassword: {}".format(self.username,self.encryption,self.otherStuff,self.password))

#The function that executes rule 1
def rule1(user,wordFile):
    for word in wordFile:
        #Checks to see if 7 char word
        #There is an 8 there to exclude the hidden /n at the end of a word
        if (len(word) == 8):
            word = word[:-1].capitalize()

            #Appends one digit to end of word
            for i in range(10):
                cWord = word
                cWord+=str(i)

                #Hashes cWord and compares it to users hash
                hashedWord = hashlib.sha256(cWord.encode()).hexdigest()
                if(user.encryption == hashedWord):
                    user.password = cWord
                    print("Rule 1")
                    print(user)
                    return True
    return False

#The function that executes rule 2 with the help of rule2Helper
def rule2(user):
    specialCharsList = ["*","~","!","#"]
    for char in specialCharsList:
        #Sets up a pool to allow multiproccessing, speeds up process
        p = Pool()
        func = partial(rule2Helper,user,char) 
        #p.map returns a list of booleans in this case
        results=p.map(func,range(100000))
        p.close()
        p.join()
        #Checks to see if the users password has been cracked
        if(compressLogicList(results)):
            return True
    return False

#The helper function to rule2
#user- The user object whos password we are trying to crack
#char- The character to be added to the beginning of the number
#i- The current number the function is on, ex: *00042 in this case i=42
def rule2Helper(user,char,i):
    #Adds the character to begining of number with 5 decimal places
    #Adds zeros if i<10000, ex: 00042 i=42 and added 3 zeros to make it 5 decimal places
    cWord = char + ('{:d}'.format(i).zfill(5))

    #Hashes cWord and compares it to users hash
    hashedWord = hashlib.sha256(cWord.encode()).hexdigest()
    if(user.encryption == hashedWord):
        user.password = cWord
        print("Rule 2")
        print(user)
        return True
    else:
        return False

#The function that executes rule3
def rule3(user,wordFile):
    for word in wordFile:
        cWord = word[:-1]
        #Searches for a word with 5 char word that has an a or l
        if (len(cWord) == 5 and (cWord.find("a") >= 0 or cWord.find("l") >= 0)):
            cWord = cWord.replace("a","@")
            cWord = cWord.replace("l","1")

            #Hashes cWord and compares it to users hash
            hashedWord = hashlib.sha256(cWord.encode()).hexdigest()
            if(user.encryption == hashedWord):
                user.password = cWord
                print("Rule 3")
                print(user)
                return True
    return False

#The function that executes rule4 with help of rule4Helper and rule4Helper2
def rule4(user):
    #Sets up a pool to allow multiproccessing, speeds up process
    #First checks numbers 0-9999999
    p = Pool()
    func = partial(rule4Helper,user)
    #p.map returns a list of booleans in this case
    results=p.map(func,range(10000000))
    p.close()
    p.join()

    result=compressLogicList(results)
    if result:
        return result

    #Checks all other up to 7 digit possibilities
    #ex: when i=2 checks from 000-999, when i=3 checks from 0000-9999
    for j in range(7):
        #Sets up a pool to allow multiproccessing, speeds up process
        p = Pool()
        func = partial(rule4Helper2,user,j)
        #p.map returns a list of booleans in this case
        results=p.map(func,range(int(math.pow(10,j+1))))
        p.close()
        p.join() 
        if(compressLogicList(results)):
            return True
    return False

#The helper function to rule4
#user- The user object whos password we are trying to crack
#i- The current number rule 4 is wanting to be hashed and than compared to the users hash
#In the method i counts from 0-9999999
def rule4Helper(user,i):
    hashedWord = hashlib.sha256(str(i).encode()).hexdigest()
    if(user.encryption == hashedWord):
        user.password = str(i)
        print("Rule 4")
        print(user)
        return True
    return False

#The helper function to rule4
#user- The user object whos password we are trying to crack
#j- Gets 2 added to it than its the number of decimal places i should have, ex: j=4 and i=42 -> 000042
#i- The current number rule 4 is wanting to be hashed and than compared to the users hash
def rule4Helper2(user,j,i):
    #Adds 2 to j to prevent redundant comparisions with function rule2Helper1 
    cWord = '{:d}'.format(i).zfill(j+2)

    #Hashes cWord and compares it to users hash
    hashedWord = hashlib.sha256(str(cWord).encode()).hexdigest()
    if(user.encryption == hashedWord):
        user.password = str(cWord)
        print("Rule 4")
        print(user)
        return True
    return False

#Function that executes rule5
#Hashes than compares every word in word file to see if it matches the users
def rule5(user,wordFile):
    wordFile = open("words.txt")
    for word in wordFile:
        cWord = word[:-1]
        hashedWord = hashlib.sha256(cWord.encode()).hexdigest()
        if(user.encryption == hashedWord):
            user.password = cWord
            print("Rule 5")
            print(user)
            return True
    return False

#Converts a file into a list of user objects
def fileToUsers(passwordFile):
    userList = []
    for line in passwordFile:
        usernameTest = False
        encryptionTest = False
        newUser = user()

        indexOfSearch = line.find(":")
        newUser.username = line[0:indexOfSearch]

        copyOfLine = line[indexOfSearch:]
        indexOfSearch = copyOfLine[1:].find(":")
        newUser.encryption = copyOfLine[1:indexOfSearch + 1]

        copyOfLine = copyOfLine[indexOfSearch + 2:len(copyOfLine) - 1]
        newUser.otherStuff = copyOfLine
        print("\n")
        print(newUser)

        userList.append(newUser)
    return userList

#Performs OR on a list of boolean functions to get one boolean function in end
#Ex: [True,False,True,True] -> True, [False,False,False] -> False
def compressLogicList(list):
    count=list.count(True)
    if(count>0):
        return True
    return False

def main():

    passwordFile = open("passwordFile.txt")
    userList=fileToUsers(passwordFile)
    
    print("***********************************")
    
    #Trys to crack each users password using the 5 differant rules
    #Will stop checking the rules for a user if a password is found
    #Ex: A password is found for a user on rule2, it will not try rule3,rule4, or rule5
    for userVar in userList:
        passwordGuessed = False
        
        #Rule 1
        startTime=time.time()
        wordFile = open("words.txt")
        passwordGuessed=rule1(userVar,wordFile)
        if passwordGuessed:
            finishTime="%.3f" % (time.time()-startTime)
            print("Rule 1 took: {} seconds\n".format(finishTime))

        #Rule 2
        if(passwordGuessed == False):
            startTime=time.time()
            passwordGuessed=rule2(userVar)
            if passwordGuessed:
                finishTime="%.3f" % (time.time()-startTime)
                print("Rule 2 took: {} seconds\n".format(finishTime))

        #Rule 3
        if(passwordGuessed == False):
            startTime=time.time()
            wordFile = open("words.txt")
            passwordGuessed=rule3(userVar,wordFile)
            if passwordGuessed:
                finishTime="%.3f" % (time.time()-startTime)
                print("Rule 3 took: {} seconds\n".format(finishTime))

        #Rule 4
        if(passwordGuessed==False):
            startTime=time.time()
            passwordGuessed=rule4(userVar)
            if passwordGuessed:
                finishTime="%.3f" % (time.time()-startTime)
                print("Rule 4 took: {} seconds\n".format(finishTime))

        #Rule 5
        if(passwordGuessed==False):
            startTime=time.time()
            wordFile=open("words.txt")
            passwordGuessed=rule5(userVar,wordFile)
            if passwordGuessed:
                finishTime="%.3f" % (time.time()-startTime)
                print("Rule 5 took: {} seconds\n".format(finishTime))

    print("Done")                

if __name__ == "__main__":
    main()