# -*- coding: utf-8 -*-

from collections import deque
import json
from scipy import spatial
import pickle
from math import log
import time


import community
import operator
import networkx as nx
import os

index = 0
char_int_to_str = {}
char_str_to_int = {}

'''
reads the characters (with their nicknames) which are in characters.txt and puts them into dicts.
To be able to give another name to the character you should put space and write the other name in the same line in characters.txt
'''


result = {}
'''

with open('characters.txt','r') as charactersPath:
    for line in charactersPath:
        nicknames = []
        for word in line.split():
            nicknames.append(word)
            char_str_to_int[word] = index
        char_int_to_str[index] = nicknames
        index += 1

encounteredWords = deque([])
characterCorpus = {}

allBooks = ['book1.txt', 'book2.txt', 'book3.txt', 'book4.txt', 'book5.txt']
book = ['book3.txt']
print("Reading book... STARTED")
for book in book:
    with open(book,'r') as f:
        for line in f:
            line = line.replace('’', ' ').replace(',', ' ').replace('“', ' ').replace('”', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ')
            for word in line.split():
                word = word.lower()
                if len(encounteredWords) == 10:
                    encounteredWords.popleft()

                #if a character has been encountered before(in the encountered list)  and within the range, then add the new word to the characters corpus
                for character in char_str_to_int:
                    if character in encounteredWords:
                        characterCorpus[char_int_to_str[char_str_to_int[character]][0]].append(word)

                #add the new read word to the encountered words
                encounteredWords.append(word)

                #if the new read word is a character, then add all the previous encountered words(within the range) to the characters corpus
                if(word in char_str_to_int):
                    if characterCorpus.has_key(char_int_to_str[char_str_to_int[word]][0]):
                        for wordInQueue in encounteredWords:
                            characterCorpus[char_int_to_str[char_str_to_int[word]][0]].append(wordInQueue)
                    else:
                        corpusOfCharacter = []
                        characterCorpus[char_int_to_str[char_str_to_int[word]][0]] = corpusOfCharacter
                        for wordInQueue in encounteredWords:
                            characterCorpus[char_int_to_str[char_str_to_int[word]][0]].append(wordInQueue)

print("Reading book... FINISHED")

for characterData in characterCorpus:
    if len(characterCorpus[characterData]) > 0:
        output = {}
        filename = "characterCorpus/" + characterData + ".json"
        with open(filename, 'wb') as fp:
            for word in characterCorpus[characterData]:
                if word in output:
                    output[word] += 1
                else:
                    output[word] = 1
            json.dump(output, fp)

'''

def termFrequency(term, document):
    content = ""
    with open(document,'r') as data_file:
        data = json.load(data_file)
        for word in data:
                content = content + " " + word
    normalizeDocument = content.lower().split()
    x = normalizeDocument.count(term.lower()) / float(len(normalizeDocument))
    return x

def inverseDocumentFrequency(term, allDocuments):
    numDocumentsWithThisTerm = 0
    for doc in allDocuments:
        with open("characterCorpus/" + doc) as data_file:
            data = json.load(data_file)
        if term.lower() in data:
            numDocumentsWithThisTerm = numDocumentsWithThisTerm + 1

    if numDocumentsWithThisTerm > 0:
        return 1.0 + log(float(len(allDocuments)) / numDocumentsWithThisTerm)
    else:
        return 1.0

def calculateAllIDF(allDocuments):
    print("Calculating all IDF scores... STARTED")
    wordSet = {}
    for doc in allDocuments:
        print("Calculating IDF scores for this document: " + doc)
        with open("characterCorpus/" + doc) as data_file:
            data = json.load(data_file)
        for word in data:
            valueIDF = inverseDocumentFrequency(word, allDocuments)
            wordSet[word] = valueIDF
        print("Calculating IDF scores for this document: " + doc + " FINISHED")
    with open("characterCorpus/IDFScores.json", 'wb') as fp:
        json.dump(wordSet, fp)
    print("Calculating all IDF scores... FINISHED")

def calculateTFIDF(allDocuments):
    print("Calculating all TFIDF scores... STARTED")
    resultSet = {}
    with open("characterCorpus/IDFScores.json") as data_file:
        idfScores = json.load(data_file)
    documents = allDocuments

    for doc in documents:
        print("Calculating TF-IDF for document: " + doc)
        resultSet[doc] = {}
        for word in idfScores:
            tfidfScore = idfScores[word] * termFrequency(word, "characterCorpus/" +doc)
            resultSet[doc][word] = tfidfScore

    with open("characterCorpus/TFIDFScores.json", 'wb') as fp:
        json.dump(resultSet, fp)
    print("Calculating all TFIDF scores... FINISHED")

def distance(firstCharacter, secondCharacter):
    result = 1 - spatial.distance.cosine(firstCharacter, secondCharacter)
    return result

path = 'characterCorpus'
documents = [f for f in os.listdir(path) if f.endswith('.json')]
documents.remove("TFIDFScores.json")
documents.remove("IDFScores.json")
#print documents

'''
start = time.time()
calculateAllIDF(documents)
calculateTFIDF(documents)
end = time.time()
print("Time elapsed: " + str(end - start))
'''

first = []
second = []

def convertDictToList(dict, characterName):
    resultList = []
    for character in dict:
        if character == characterName:
            for score in dict[character]:
                resultList.append(dict[character][score])
    return resultList

''''''
with open("characterCorpus/TFIDFScores.json") as data_file:
    results = json.load(data_file)
'''
for firstCharacter in documents:
    for secondCharacter in documents:
        first = convertDictToList(results, firstCharacter)
        second = convertDictToList(results, secondCharacter)
        print "Distance between " + firstCharacter + " and " + secondCharacter + " is: " + str(distance(first, second))
'''
