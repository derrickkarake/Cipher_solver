import pprint, os, copy, pyperclip, re, sys, random, pprint


def GwordPattern(word):
    word = word.upper()
    nextNum = 0
    letterNums = {}
    wordPattern = []
    
    for letter in word:
        if letter not in letterNums:
            letterNums[letter] = str(nextNum)
            nextNum += 1
        wordPattern.append(letterNums[letter])
    return '.'.join(wordPattern)

def main():
    
    global allPatterns
    allPatterns = {}

    wordList = open('dictonary.txt').read().split('\n')
    
    for word in wordList:
    
        pattern = GwordPattern(word)
    
        if pattern not in allPatterns:
            allPatterns[pattern] = [word]
        else:
            allPatterns[pattern].append(word)
    
   # print(pprint.pformat(allPatterns))

    



LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nonLettersOrSpacePattern = re.compile('[^A-Z\s]')

def main1():
    message = 'VMKJ WCRBVDPCXL MXJ ID JDYQVKDI'


    letterMapping = hackSimpleSub(message)
    pprint.pprint(letterMapping)
    print()

    print('Crypto Gram:')
    print(message)
    print()

    print('Copying hacked message')
    hackedMessage = decryptWithCipherletterMapping(message, letterMapping)
    print(hackedMessage)

def getBlankCipherletterMapping():

    return{'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [],
            'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [], 'O': [], 'P':
            [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [],
            'Y': [], 'Z': []}

def addLettersToMapping(letterMapping, cipherword, candidate):

    letterMapping = copy.deepcopy(letterMapping)
    for i in range(len(cipherword)):
        if candidate[i] not in letterMapping[cipherword[i]]:

            letterMapping[cipherword[i]].append(candidate[i])

    return letterMapping 


def intersectMappings(mapA, mapB):

    intersectedMapping = getBlankCipherletterMapping()

    for letter in LETTERS:
    
        if mapA[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapB[letter])
        elif mapB[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapA[letter])
        else:
            for mappedLetter in mapA[letter]:
                if mappedLetter in mapB[letter]:
                    intersectedMapping[letter].append(mappedLetter)

    return intersectedMapping
            
def removeSolvedLettersFromMapping(letterMapping):

   
    letterMapping = copy.deepcopy(letterMapping)
    loopAgain = True


    while loopAgain:
        loopAgain = False

        solvedLetters = []
        for cipherletter in LETTERS:
            if len(letterMapping[cipherletter]) == 1:
                solvedLetters.append(letterMapping[cipherletter][0])


        for cipherletter in LETTERS:
            for s in solvedLetters:
                if len(letterMapping[cipherletter]) != 1 and s in letterMapping[cipherletter]:
                    letterMapping[cipherletter].remove(s)

                    if len(letterMapping[cipherletter]) == 1:
                        loopAgain = True
    #print(letterMapping)
    return letterMapping



def hackSimpleSub(message):
    intersectedMap = getBlankCipherletterMapping()


    cipherwordList = nonLettersOrSpacePattern.sub('',message.upper()).split()


    for cipherword in cipherwordList:
        newMap = getBlankCipherletterMapping()
        wordPattern = GwordPattern(cipherword)

        if wordPattern not in allPatterns:
            continue

        for candidate in allPatterns[wordPattern]:
            newMap = addLettersToMapping(newMap, cipherword, candidate)
        intersectedMap = intersectMappings(intersectedMap, newMap)

    print(intersectedMap)
    

    return removeSolvedLettersFromMapping(intersectedMap)



def decryptWithCipherletterMapping(ciphertext, letterMapping):

    key = ['x'] * len(LETTERS)

    for cipherletter in LETTERS:
        if len(letterMapping[cipherletter]) == 1:
            keyIndex = LETTERS.find(letterMapping[cipherletter][0])
            key[keyIndex] = cipherletter

        else:
            ciphertext = ciphertext.replace(cipherletter.lower(), '_')
            ciphertext = ciphertext.replace(cipherletter.upper(), '_')

    key = ''.join(key)
    print(key)

    return Try(key, ciphertext)


def Try(myKey, myMessage):
   
    global LETTERS
    myMessage = myMessage
    myKey = myKey
    myMode = 'decrypt'
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    #checkValidKey(myKey)

    if myMode == 'encrypt':
        translated = encryptMessage(myKey, myMessage)

    elif myMode == "decrypt": 
        translated = decryptMessage(myKey, myMessage)

    print('Using key %s' % (myKey))
    print('The %sed message is:' % (myMode))
    print(translated)
    pyperclip.copy(translated)
    print()

def checkValidKey(key):
    keyList = list(key)
    lettersList = list(LETTERS)
    keyList.sort()
    lettersList.sort()
    if keyList != lettersList:
        sys.exit('There is an error in the key or symbol set.')


def encryptMessage(key, message):
    
    return translateMessage(key, message, 'encrypt')

def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')

def translateMessage(key, message, mode):
    translated = ''
    charsA = LETTERS
    charsB = key
    if mode == 'decrypt':
        charsA, charsB = charsB, charsA 


        for symbol in message:
            if symbol.upper() in charsA:
                symIndex = charsA.find(symbol.upper())

                if symbol.isupper():
                    translated += charsB[symIndex].upper()
                else:
                    translated += charsB[symIndex].lower()
            else: 
                translated += symbol

    return translated

def getRandomKey():
    key = list(LETTERS)

    random.shuffle(key)

    return ''.join(key)


main()
#main1() 



letterMappings = getBlankCipherletterMapping()

ciphertext = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isrsxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'
cipherList = nonLettersOrSpacePattern.sub('',ciphertext.upper()).split()

#print(cipherList)


for cipherzord in cipherList:
    newMap = getBlankCipherletterMapping()
    wordPattern = GwordPattern(cipherzord)

    if wordPattern not in allPatterns:
        continue

    for candidate in allPatterns[wordPattern]:
        newMap = addLettersToMapping(newMap, cipherzord, candidate)
    letterMappings = intersectMappings(letterMappings, newMap)





testmapping1 = getBlankCipherletterMapping()

wordPattern = GwordPattern('VMKJ')
candidates = allPatterns[wordPattern]

for candindate1 in candidates:
    testmapping1 = addLettersToMapping(testmapping1,'VMKJ',candindate1)




#print (letterMappings)

test3 = removeSolvedLettersFromMapping(letterMappings)
#print(test3)



#test4 = decryptWithCipherletterMapping(ciphertext,test3)
#print(test4)

#pprint.pprint(letterMappings)


#word = 'JDYQVKDI'

#test3 = GwordPattern(word)

#test4 = allPatterns[test3]

#print(test4)

letterMappings5 = getBlankCipherletterMapping

#for candidate in test4:
#    letterMappings5 =   addLettersToMapping(letterMappings,word,candidate) 

#rint(letterMappings5)



