# -*- coding: utf-8 -*-
import os
from collections import deque
import json
import community
import operator
import networkx as nx

from characterCorpus import convertDictToList, distance

index = 0
char_int_to_str = {}
char_str_to_int = {}

friends = []
friendBase = {}

sizeFriendsBase = len(friends)
for word in friends:
    friendBase[word] = 1.0 / sizeFriendsBase
withFriends = False
if sizeFriendsBase > 0:
    withFriends = True

result = {}

'''
reads the characters (with their nicknames) which are in characters.txt and puts them into dicts.
To be able to give another name to the character you should put space and write the other name in the same line in characters.txt
'''

with open('characters.txt','r') as charactersPath:
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

book = ['book3.txt']
for book in book:
    with open(book,'r') as f:
        for line in f:
            line = line.replace('’', ' ').replace(',', ' ').replace('“', ' ').replace('”', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ')
            for word in line.split():
                word = word.lower()
                for index in range(0, len(counterQueue)):
                    if(counterQueue.__len__() > index):
                        counterQueue[index] = counterQueue[index] + 1
                        if counterQueue[index] == 50:
                            counterQueue.popleft()
                            characterQueue.popleft()

                if(word in char_str_to_int):
                    #start reading 25words---WORD---25words range. extract words within that range to produce output later.
                    counterQueue.append(0)
                    characterQueue.append(word)
                    for character in characterQueue:
                        nicknameList = char_int_to_str[char_str_to_int[character]]
                        if word not in nicknameList:
                            print('Relation found between ' + word + ' and ' + character)
                            Matrix[char_str_to_int[character]][char_str_to_int[word]] += 1
                            Matrix[char_str_to_int[word]][char_str_to_int[character]] += 1

'''for characterRow in range(Matrix.__len__()):
    for character in range(Matrix.__len__() - (characterRow+1)):
        print(char_int_to_str[characterRow] + ', ' + char_int_to_str[character + (characterRow+1)] + ' --> ' + (str)(Matrix[characterRow][character + (characterRow+1)]))
'''

nodes = []
links = []
nodeScores = {}
for characterRow in range(Matrix.__len__()):
    sum = 0
    for character in range(Matrix.__len__()):
        sum = sum + Matrix[characterRow][character]
    nodeScores[char_int_to_str[characterRow][0]] = sum


G = nx.Graph()
for characterRow in range(Matrix.__len__()):
    G.add_node(char_int_to_str[characterRow][0])

for characterRow in range(Matrix.__len__()):
    for character in range(Matrix.__len__() - (characterRow+1)):
        if Matrix[characterRow][character + (characterRow + 1)] > 0:
            G.add_edge(char_int_to_str[characterRow][0], char_int_to_str[character + characterRow+1][0], weight=Matrix[characterRow][character + (characterRow+1)])


for characterRow in range(Matrix.__len__()):
    if (char_int_to_str[characterRow][0]) not in friendBase and withFriends:
        friendBase[(char_int_to_str[characterRow][0])] = 0

if withFriends:
    similarityRanks = nx.pagerank(G, personalization=friendBase)
else:
    similarityRanks = nx.pagerank(G)

pg = nx.pagerank(G)

parts = community.best_partition(G)

for character in pg:
    result[character] = similarityRanks[character] / pg[character]


for characterRow in range(Matrix.__len__()):
    characterInfo = {}
    characterInfo["id"] = char_int_to_str[characterRow][0]
    characterInfo["group"] = parts[char_int_to_str[characterRow][0]]
    if withFriends is True:
        characterInfo["weight"] = result[char_int_to_str[characterRow][0]]
    else:
        characterInfo["weight"] = pg[char_int_to_str[characterRow][0]]
    nodes.append(characterInfo)

for characterRow in range(Matrix.__len__()):
    for character in range(Matrix.__len__() - (characterRow+1)):
        if Matrix[characterRow][character + (characterRow+1)] > 3:
            linkInfo = {}
            linkInfo["source"] = char_int_to_str[characterRow][0]
            linkInfo["target"] = char_int_to_str[character + (characterRow+1)][0]
            linkInfo["value"] = Matrix[characterRow][character + (characterRow+1)]
            links.append(linkInfo)

data = {}
data["nodes"] = nodes
data["links"] = links
data["withFriends"] = False
if withFriends:
    data["withFriends"] = True



sorted_x = sorted(result.items(), key=operator.itemgetter(1), reverse=True)


with open('gameofthrones.json', 'w') as outfile:
    json.dump(data, outfile)


def tfidfVSsimRank(thresholdTFIDF):
    path = 'characterCorpus'
    documents = [f for f in os.listdir(path) if f.endswith('.json')]
    documents.remove("TFIDFScores.json")
    documents.remove("IDFScores.json")
    # print documents

    with open("characterCorpus/TFIDFScores.json") as data_file:
        results = json.load(data_file)

    thresholdSimrank = 0.0
    thresholdTFIDF = thresholdTFIDF

    truePositive = 0
    falsePositive = 0
    for character in char_int_to_str:
        character = char_int_to_str[character][0]
        simrankBase = {}
        for characterRow in range(Matrix.__len__()):
            if (char_int_to_str[characterRow][0]) not in simrankBase :
                xy = (char_int_to_str[characterRow][0])
                simrankBase[xy] = 0
        simrankBase[character] = 1.0
        similarityRanks = nx.pagerank(G, personalization=simrankBase)

        for characterX in pg:
            result[characterX] = similarityRanks[characterX] / pg[characterX]
        sorted_x = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
        index = 0
        print("For character: " + str(char_int_to_str[char_str_to_int[character]][0]) + " most similar characters are below:")
        for characterY in sorted_x:
            if index >= sizeFriendsBase and index < (sizeFriendsBase + 3) and characterY[1] > thresholdSimrank:
                first = convertDictToList(results, (character+".json"))
                second = convertDictToList(results, (characterY[0]+".json"))
                distanceResult =  distance(first, second)
                print "Distance between " + character + " and " + str(characterY[0]) + " is: " + str(distanceResult)
                if distanceResult > thresholdTFIDF:
                    print ("TRUE POSITIVE!!")
                    truePositive += 1
                else:
                    print("FALSE POSITIVE :(")
                    falsePositive += 1
            index += 1

    total = truePositive + falsePositive

    print "Among " + str(total)+ " predictions:"
    print "True positives are: " + str(truePositive)
    print "False positives are: " + str(falsePositive)

def commDetVSsimRank(threshold):
    truePositive = 0
    falsePositive = 0
    for character in char_int_to_str:
        characterToCompare = char_int_to_str[character][0]
        simrankBase = {}
        for characterRow in range(Matrix.__len__()):
            if (char_int_to_str[characterRow][0]) not in simrankBase :
                xy = (char_int_to_str[characterRow][0])
                simrankBase[xy] = 0
        simrankBase[characterToCompare] = 1.0
        similarityRanks = nx.pagerank(G, personalization=simrankBase)

        for characterX in pg:
            result[characterX] = similarityRanks[characterX] / pg[characterX]
        sorted_x = sorted(result.items(), key=operator.itemgetter(1), reverse=True)

        index = 0
        groupNo = parts[characterToCompare]
        groupSize = 0

        for character in parts:
            if parts[character] == groupNo:
                groupSize += 1
        print("-------------------------------------------")
        print("For character: " + characterToCompare + " most " + str(groupSize) + " similar characters are below:")
        for character_tuple in sorted_x:
            if index >= sizeFriendsBase and index < (sizeFriendsBase + groupSize) and character_tuple[1] > threshold:
                print(str(character_tuple) + " has been found as a result of simrank.")
                if parts[character_tuple[0]] == groupNo:
                    truePositive += 1
                    print("TRUE POSITIVE!!")
                else:
                    falsePositive += 1
                    print("FALSE POSITIVE :(")
            index += 1
        print("-------------------------------------------")
    total = truePositive + falsePositive

    print "Among " + str(total) + " predictions:"
    print "True positives are: " + str(truePositive)
    print "False positives are: " + str(falsePositive)

def commDetVStfidf(thresholdTFIDF):
    truePositive = 0
    falsePositive = 0
    path = 'characterCorpus'
    documents = [f for f in os.listdir(path) if f.endswith('.json')]
    if documents.count("TFIDFScores.json") > 0:
        documents.remove("TFIDFScores.json")
    if documents.count("IDFScores.json") > 0:
        documents.remove("IDFScores.json")
    with open("characterCorpus/TFIDFScores.json") as data_file:
        results = json.load(data_file)
    characterXSim = {}
    for firstCharacter in documents:
        for secondCharacter in documents:
            first = convertDictToList(results, firstCharacter)
            second = convertDictToList(results, secondCharacter)
            distanceFirst_Second = distance(first, second)
            if distanceFirst_Second > thresholdTFIDF:
                firstCharacterGroup = parts[firstCharacter.split(".")[0]]
                secondCharacterGroup = parts[secondCharacter.split(".")[0]]
                if firstCharacterGroup == secondCharacterGroup:
                    #characterXSim[firstCharacter][secondCharacter] = distanceFirst_Second
                    truePositive += 1
                else:
                    falsePositive += 1

    total = truePositive + falsePositive

    print "Among " + str(total) + " predictions:"
    print "True positives are: " + str(truePositive)
    print "False positives are: " + str(falsePositive)


#commDetVStfidf(thresholdTFIDF=0.22)
#commDetVSsimRank(threshold=1.1)
#tfidfVSsimRank(thresholdTFIDF=0.17)