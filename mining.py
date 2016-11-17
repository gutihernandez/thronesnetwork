# -*- coding: utf-8 -*-

from collections import deque
import json

index = 0
char_int_to_str = {}
char_str_to_int = {}

with open('characters.txt','r') as charactersPath:
    for line in charactersPath:
        for word in line.split():
            char_str_to_int[word] = index
            char_int_to_str[index] = word
            index += 1



Matrix = [[0 for x in range(char_int_to_str.__len__())] for y in range(char_int_to_str.__len__())]

counterQueue = deque([])
characterQueue = deque([])


with open('book2.txt','r') as f:
    for line in f:
        line = line.replace('’', ' ').replace(',', ' ').replace('“', ' ').replace('”', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ')
        for word in line.split():
            word = word.lower()
            for index in range(0, counterQueue.__len__()):
                if(counterQueue.__len__() > index):
                    counterQueue[index] = counterQueue[index] + 1
                    if counterQueue[index] == 50:
                        counterQueue.popleft()
                        characterQueue.popleft()

            if(word in char_str_to_int):
                counterQueue.append(0)
                characterQueue.append(word)
                for character in characterQueue:
                    if(word != character):
                        print('Relation found between ' + word + ' and ' + character)
                        Matrix[char_str_to_int[character]][char_str_to_int[word]] += 1
                        #Matrix[char_str_to_int[word]][char_str_to_int[character]] += 1


print(Matrix)

for characterRow in range(Matrix.__len__()):
    for character in range(Matrix.__len__() - (characterRow+1)):
        print(char_int_to_str[characterRow] + ', ' + char_int_to_str[character + (characterRow+1)] + ' --> ' + (str)(Matrix[characterRow][character + (characterRow+1)]))



nodes = []
links = []
nodeScores = {}
for characterRow in range(Matrix.__len__()):
    sum = 0
    for character in range(Matrix.__len__()):
        sum = sum + Matrix[characterRow][character]
    nodeScores[char_int_to_str[characterRow]] = sum

for characterRow in range(Matrix.__len__()):
    characterInfo = {}
    characterInfo["id"] = char_int_to_str[characterRow]
    characterInfo["group"] = 1
    characterInfo["weight"] = nodeScores[char_int_to_str[characterRow]]
    nodes.append(characterInfo)

for characterRow in range(Matrix.__len__()):
    for character in range(Matrix.__len__() - (characterRow+1)):
        if Matrix[characterRow][character + (characterRow+1)] > 5:
            linkInfo = {}
            linkInfo["source"] = char_int_to_str[characterRow]
            linkInfo["target"] = char_int_to_str[character + (characterRow+1)]
            linkInfo["value"] = Matrix[characterRow][character + (characterRow+1)]
            links.append(linkInfo)

data = {}
data["nodes"] = nodes
data["links"] = links



with open('gameofthrones.json', 'w') as outfile:
    json.dump(data, outfile)