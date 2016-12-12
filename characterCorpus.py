# -*- coding: utf-8 -*-

from collections import deque
import json
import pickle
from math import log

import community
import operator
import networkx as nx


index = 0
char_int_to_str = {}
char_str_to_int = {}

'''
reads the characters (with their nicknames) which are in characters.txt and puts them into dicts.
To be able to give another name to the character you should put space and write the other name in the same line in characters.txt
'''


result = {}

with open('testCharacters.txt','r') as charactersPath:
    for line in charactersPath:
        nicknames = []
        for word in line.split():
            nicknames.append(word)
            char_str_to_int[word] = index
        char_int_to_str[index] = nicknames
        index += 1


Matrix = [[0 for x in range(char_int_to_str.__len__())] for y in range(char_int_to_str.__len__())]
'''
counter queue is for in which range the '''
counterQueue = deque([])
characterQueue = deque([])

encounteredWords = deque([])
characterCorpus = {}

allBooks = ['book1.txt', 'book2.txt', 'book3.txt', 'book4.txt', 'book5.txt']
book = ['test.txt']
for book in book:
    with open(book,'r') as f:
        for line in f:
            line = line.replace('’', ' ').replace(',', ' ').replace('“', ' ').replace('”', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ')
            for word in line.split():
                word = word.lower()
                if len(encounteredWords) == 3:
                    encounteredWords.popleft()

                for character in char_str_to_int:
                    if character in encounteredWords:
                        characterCorpus[char_int_to_str[char_str_to_int[character]][0]].append(word)

                encounteredWords.append(word)

                if(word in char_str_to_int):
                    if characterCorpus.has_key(word):
                        for wordInQueue in encounteredWords:
                            characterCorpus[char_int_to_str[char_str_to_int[word]][0]].append(wordInQueue)
                    else:
                        corpusOfCharacter = []
                        characterCorpus[word] = corpusOfCharacter
                        for wordInQueue in encounteredWords:
                            characterCorpus[char_int_to_str[char_str_to_int[word]][0]].append(wordInQueue)
print characterCorpus


for characterData in characterCorpus:
    if len(characterCorpus[characterData]) > 0:
        filename = "characterCorpus/" + characterData + ".txt"
        with open(filename, 'wb') as fp:
            for word in characterCorpus[characterData]:
                if(len(word) > 0):
                    fp.write("%s\n" % word)


def termFrequency(term, document):
    content = ""
    with open(document,'r') as f:
        for line in f:
            line = line.replace('’', ' ').replace(',', ' ').replace('“', ' ').replace('”', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ')
            for word in line.split():
                content = content + " " + word
    normalizeDocument = content.lower().split()
    return normalizeDocument.count(term.lower()) / float(len(normalizeDocument))


def inverseDocumentFrequency(term, allDocuments):
    numDocumentsWithThisTerm = 0
    for doc in allDocuments:
        if term.lower() in allDocuments[doc].lower().split():
            numDocumentsWithThisTerm = numDocumentsWithThisTerm + 1

    if numDocumentsWithThisTerm > 0:
        return 1.0 + log(float(len(allDocuments)) / numDocumentsWithThisTerm)
    else:
        return 1.0
