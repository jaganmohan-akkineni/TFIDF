import sys
import os
import string
import csv
import string
import re
import pandas as pd
import math
from collections import defaultdict


DATA_PATH = "/Users/jaganmohan/Python/IR_Assignments/TFIDF/files/"

textdirs = os.listdir(DATA_PATH)

delimiter_chars=",.;:!?"

word_occurrences = {}
nfwords = defaultdict(int)

for file in textdirs:

    filename = os.path.join(DATA_PATH, file)
    txt_fil = open(filename, "r")

    pos = 0
    nwords = 0
    
    for lin in txt_fil:
        lin = lin.lower()
        words = re.findall(r'\b\w[\w-]*\b', lin.lower())

        for word in words: 
            if word.isalpha():
                pos += lin.find(word)
               
                if word in word_occurrences.keys():
                    if file in word_occurrences[word].keys():
                        word_occurrences[word][file].append(pos)
                    else:
                        word_occurrences[word][file] = [pos]
                else:
                    word_occurrences[word] = { file : [pos] }
           
            nwords += 1
        pos += len(lin) - 1
    
    nfwords[file] = nwords 

    word_keys = word_occurrences.keys()

word_keys = word_occurrences.keys()

word_keys = sorted(word_keys)
        
txt_fil.close()

#Word Frequencies
counts = defaultdict(int)
n_words = 0
docs = {}
for file in word_occurrences[word].keys():
    relativefreqs = {}

    for word in word_occurrences.keys():
        counts[word] = len(word_occurrences[word])

        relativefreqs[word] = counts[word] / nfwords[file]

    docs[file] = relativefreqs

df = pd.DataFrame(docs)
df = df.fillna(0)
df.to_csv('Frequencies.csv', encoding="utf-8") # write out to CSV


#Inverse Frequencies
idf = {}

with open('Frequencies.csv', encoding="utf-8", newline='') as csvfile:
    wordsreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    total_documents = len(next(wordsreader, None)) - 1

    for row in wordsreader:
        docsContainingWord = 0
        iterrow = iter(row)
        next(iterrow)
        for entry in iterrow:
            if (entry != '0.0') and (entry != '0'):
                docsContainingWord += 1
        idf[row[0]] = math.log(total_documents / (1 + docsContainingWord))
        
df = pd.DataFrame(idf, index=['Inverse Document Frequency'])
df2 = df.transpose()
df2.to_csv('InverseFrequency.csv', encoding="utf-8")

#TFIDF
file1reader = csv.reader(open('Frequencies.csv', encoding="utf-8"), delimiter=",")
file2reader = csv.reader(open('InverseFrequency.csv', encoding="utf-8"), delimiter=",")

header1 = next(file1reader) 
header2 = next(file2reader) 
with open('tfidf.csv', 'w', encoding="utf-8", newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header1)
    for row1, row2 in zip(file1reader, file2reader):
        rowOut = []
        iterrow1 = iter(row1)
        rowOut.append(next(iterrow1))
        for entry in iterrow1:
            entry = float(entry) * float(row2[1])
            rowOut.append(entry)
        writer.writerow(rowOut)
    




