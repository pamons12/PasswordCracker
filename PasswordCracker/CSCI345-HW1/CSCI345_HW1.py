import hashlib
import math
from multiprocessing import Pool
from functools import partial
import time


class user:
    def __init__(self,username,encryption,otherstuff,password):
        self.username = username
        self.encryption = encryption
        self.otherStuff = otherstuff
        self.password = password

    def __init__(self):
        self.username = ""
        self.encryption = ""
        self.otherStuff = ""
        self.password = ""

    def __str__(self):
        return("Username: {}\nEncyrption: {}\nOther stuff: {}\nPassword: {}\n".format(self.username,self.encryption,self.otherStuff,self.password))

def rule1(wordFile,user):
           for word in wordFile:
            if (len(word) == 8):
                word = word[:7].capitalize()
                for i in range(10):
                    cWord = word
                    cWord+=str(i)
                    hashedWord = hashlib.sha256(cWord.encode()).hexdigest()
                    if(user.encryption == hashedWord):
                        user.password = cWord
                        print("Rule 1")
                        print(user)
                        return True
def rule2(user,char,i):
           cWord = char + ('{:d}'.format(i).zfill(6))
           hashedWord = hashlib.sha256(cWord.encode()).hexdigest()
           if(user.encryption == hashedWord):
                user.password = cWord
                print("Rule 2")
                print(user)

def main():
    passwordFile = open("passwordFile.txt")
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
        print(newUser)

        userList.append(newUser)
    
    print("***********************************")
    wordFile = open("words.txt")
    passwordGuessed = False

    for userVar in userList:
        passwordGuessed = False
        wordFile = open("words.txt")
        
        #Rule 1
        #Using function call
        startTime=time.time()
        rule1(wordFile,userVar)
        print("Rule 1 Function call: {}".format(time.time()-startTime))

        #Not using function call
        wordFile=open("words.txt")
        startTime=time.time()
        for word in wordFile:
            if (len(word) == 8):
                word = word[:7].capitalize()
                for i in range(10):
                    cWord = word
                    cWord+=str(i)
                    hashedWord = hashlib.sha256(cWord.encode()).hexdigest()
                    if(userVar.encryption == hashedWord):
                        userVar.password = cWord
                        print("Rule 1")
                        print(userVar)
                        passwordGuessed = True
        print("Rule 1 No Function call: {}".format(time.time()-startTime))

        #Rule 2
        if(passwordGuessed == False):
            specialCharsList = ["*","~","!","#"]

            #Using Pool
            startTime=time.time()
            for char in specialCharsList:
                p = Pool()
                func = partial(rule2,userVar,char)
                p.map(func,range(999999))
                p.close()
                p.join()
            print("Rule 2 Using Pool: {}".format(time.time()-startTime))

            #Not using pool
            startTime=time.time()
            for char in specialCharsList:
                for i in range(999999):
                    cWord = char + ('{:d}'.format(i).zfill(6))
                    hashedWord = hashlib.sha256(cWord.encode()).hexdigest()
                    if(userVar.encryption == hashedWord):
                        userVar.password = cWord
                        print("Rule 2")
                        print(userVar)
                        passwordGuessed = True
            print("Rule 2 Not using Pool: {}".format(time.time()-startTime))

        #Rule 3
        if(passwordGuessed == False):
            startTime=time.time()
            wordFile = open("words.txt")
            for word in wordFile:
                cWord = word[:-1]
                if (len(cWord) == 5 and (cWord.find("a") >= 0 or cWord.find("l") >= 0)):
                    cWord = cWord.replace("a","@")
                    cWord = cWord.replace("l","1")
                    hashedWord = hashlib.sha256(cWord.encode()).hexdigest()
                    if(userVar.encryption == hashedWord):
                        userVar.password = cWord
                        print("Rule 3")
                        print(userVar)
                        passwordGuessed = True
            print("Rule 3: {}".format(time.time()-startTime))

        #Rule 4
        if(passwordGuessed==False):
            startTime=time.time()
            counter=0
            for i in range(9999999):
                hashedWord = hashlib.sha256(str(i).encode()).hexdigest()
                if(userVar.encryption == hashedWord):
                    userVar.password = str(i)
                    print("Rule 4")
                    print(userVar)
                    passwordGuessed = True

            for i in range(7):
                counter=0
                for j in range(int(math.pow(10,i+1))):
                    cWord = '{:d}'.format(counter).zfill(i+2)
                    hashedWord = hashlib.sha256(str(cWord).encode()).hexdigest()
                    if(userVar.encryption == hashedWord):
                        userVar.password = str(cWord)
                        print("Rule 4")
                        print(userVar)
                        passwordGuessed = True
                        i=6
                        break
                    counter+=1
            print("Rule 4: {}".format(time.time()-startTime))
        #Rule 5
        if(passwordGuessed==False):
            startTime=time.time()
            wordFile = open("words.txt")
            for word in wordFile:
                cWord = word[:-1]
                hashedWord = hashlib.sha256(cWord.encode()).hexdigest()
                if(userVar.encryption == hashedWord):
                    userVar.password = cWord
                    print("Rule 5")
                    print(userVar)
                    passwordGuessed = True
            print("Rule 5: {}".format(time.time()-startTime))

    print("Done")                

if __name__ == "__main__":
    main()