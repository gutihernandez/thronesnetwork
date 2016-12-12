# -*- coding: utf-8 -*-

from collections import deque
import json
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



friendBase = {}
sizeFriendsBase = 0
with open('friends.txt','r') as charactersPath:
    for line in charactersPath:
        size = len(line.split())
        value = 1.0 / size
        for word in line.split():
            sizeFriendsBase += 1
            friendBase[word] = value

withFriends = False
if sizeFriendsBase > 0:
    withFriends = True

result = {}

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

allBooks = ['book1.txt', 'book2.txt', 'book3.txt', 'book4.txt', 'book5.txt']
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

index = 0
for character in sorted_x:
        if index >= sizeFriendsBase and index < (sizeFriendsBase+3):
            print(character)
        index += 1

with open('gameofthrones.json', 'w') as outfile:
    json.dump(data, outfile)

