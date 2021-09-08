from bs4 import BeautifulSoup as BS
import requests
from urllib import request
import re

# TODO add exception handling to deal with socket abortions

# TODO add functionality to allow these to be successfully changed from CLT
unStressedChar = "0"
stressedChar = "1"



def markAsStressed(charSequence):
    numStresses = len(charSequence.split("-"))
    return stressedChar*numStresses



def mergeStresses(inputParts):
    wordList = [""]
    beatList = [""]
    bold = False

    def addToOutputLists(word, isBold):
        wordList[-1] = wordList[-1] + word
        if isBold:
            beatList[-1] = beatList[-1] + markAsStressed(word)
        else:
            beatList[-1] = beatList[-1] + word

    for part in inputParts: # TODO need to make it deal with "and", "of", and "almond"
        part = re.sub(" ", "", part)


        # need to check if it has bold or if it just span / other span class
        if (part=='spanclass="bold"'):
            bold = True
        elif (part=='/span'):
            bold = False

        if "," in part:
            subPartList = part.split(",")
            addToOutputLists(subPartList[0], bold)
            for subPart in subPartList[1:]:
                wordList.append(subPart)
                if bold:
                    beatList.append(markAsStressed(subPart))
                else:
                    beatList.append(subPart)
        else:
            # check if word or beat to add
            if not (('/span' in part) or ('spanclass' in part)):
                addToOutputLists(part, bold)

    return wordList, beatList



def replaceUnstressedWithCharacter(unstressedList):
    finalStressesList = []
    for word in unstressedList: # TODO split up words with semi colon
        finalStressesList.append(re.sub("[a-z]+", unStressedChar, word)) # TODO add something which ensures this isnt one of the stressed characters (chosen by user)

    return finalStressesList



def removeMalformedWords(almostFinalWordList, almostFinalBeatList):
    wordsOutputList = []
    beatsOutputList = []

    # checls for valid words (i.e. -mul should not be included in final)
    for i in range(len(almostFinalWordList)):
        word = almostFinalWordList[i]
        if not ((word.startswith("-")) or (word.endswith("-"))):
            wordsOutputList.append(word)
            beatsOutputList.append(almostFinalBeatList[i])

    return wordsOutputList, beatsOutputList



def getStressPattern(word):
    #print(word)
    r = requests.get("https://www.dictionary.com/browse/" + word)
    htmlFile = r.content
    soup = BS(htmlFile, "html.parser")
    pronounciationContent = soup.find("span", class_="pron-spell-content css-7iphl0 evh0tcl1")
    pronounciationContent = str(pronounciationContent)
    pronounciationContent = re.sub("([^.]*\[) | (\][^.]*)", "", pronounciationContent) # remove stuff outside square brackets
    pronounciationContent = list(filter(None, re.split("<|>", pronounciationContent)))
    wordsOutputList, beatsOutputList = mergeStresses(pronounciationContent)

    wordsOutputList, beatsOutputList = removeMalformedWords(wordsOutputList, beatsOutputList)
    beatsOutputList = replaceUnstressedWithCharacter(beatsOutputList)

    return wordsOutputList, beatsOutputList



def evaluateSentance(sentance):
    sentanceWordList = []
    sentanceBeatList = []
    # for each word remove punctuation and then find corresponding stresses
    for word in sentance:
        wordInfo, beatInfo = getStressPattern(word)
        sentanceWordList.append(wordInfo)
        sentanceBeatList.append(beatInfo)

    print(sentanceWordList)
    print(sentanceBeatList)
