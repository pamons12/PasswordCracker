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

def rule1(user,wordFile):
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
    return False

def rule2Helper(user,char,i):
           cWord = char + ('{:d}'.format(i).zfill(5))
           hashedWord = hashlib.sha256(cWord.encode()).hexdigest()
           if(user.encryption == hashedWord):
                user.password = cWord
                print("Rule 2")
                print(user)
                return True
           else:
                return False

def rule2(user):
    specialCharsList = ["*","~","!","#"]
    for char in specialCharsList:
        p = Pool()
        func = partial(rule2Helper,user,char)
        results=p.map(func,range(100000))
        p.close()
        p.join()
    return compressLogic(results)

def rule3(user,wordFile):
    for word in wordFile:
        cWord = word[:-1]
        if (len(cWord) == 5 and (cWord.find("a") >= 0 or cWord.find("l") >= 0)):
            cWord = cWord.replace("a","@")
            cWord = cWord.replace("l","1")
            hashedWord = hashlib.sha256(cWord.encode()).hexdigest()
            if(user.encryption == hashedWord):
                user.password = cWord
                print("Rule 3")
                print(user)
                return True
    return False

def rule4(user):
    counter=0
    p = Pool()
    func = partial(rule4Helper,user)
    results=p.map(func,range(9999999))
    p.close()
    p.join()
    for i in range(7):
                counter=0
                for j in range(int(math.pow(10,i+1))):
                    cWord = '{:d}'.format(counter).zfill(i+2)
                    hashedWord = hashlib.sha256(str(cWord).encode()).hexdigest()
                    if(user.encryption == hashedWord):
                        user.password = str(cWord)
                        print("Rule 4")
                        print(user)
                        return True
                    counter+=1
    return False

def rule4Helper(user,i):
    hashedWord = hashlib.sha256(str(i).encode()).hexdigest()
    if(user.encryption == hashedWord):
        user.password = str(i)
        print("Rule 4")
        print(user)
        return True
    else:
        return False

def compressLogic(list):
     result=False
     for thing in list:
         result=result or thing
     return result

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
        
        #Rule 1
        startTime=time.time()
        wordFile = open("words.txt")
        passwordGuessed=rule1(userVar,wordFile)
        print("Rule 1 took: {}".format(time.time()-startTime))

        #Rule 2
        if(passwordGuessed == False):
            startTime=time.time()
            passwordGuessed=rule2(userVar)
            print("Rule 2 took: {}".format(time.time()-startTime))

        #Rule 3
        if(passwordGuessed == False):
            startTime=time.time()
            wordFile = open("words.txt")
            passwordGuessed=rule3(userVar,wordFile)
            print("Rule 3 took: {}".format(time.time()-startTime))

        #Rule 4
        if(passwordGuessed==False):
            startTime=time.time()
            passwordGuessed=rule4(userVar)
            #counter=0
            #for i in range(9999999):
            #    hashedWord = hashlib.sha256(str(i).encode()).hexdigest()
            #    if(userVar.encryption == hashedWord):
            #        userVar.password = str(i)
            #        print("Rule 4")
            #        print(userVar)
            #        passwordGuessed = True

            #for i in range(7):
            #    counter=0
            #    for j in range(int(math.pow(10,i+1))):
            #        cWord = '{:d}'.format(counter).zfill(i+2)
            #        hashedWord = hashlib.sha256(str(cWord).encode()).hexdigest()
            #        if(userVar.encryption == hashedWord):
            #            userVar.password = str(cWord)
            #            print("Rule 4")
            #            print(userVar)
            #            passwordGuessed = True
            #            i=6
            #            break
            #        counter+=1
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