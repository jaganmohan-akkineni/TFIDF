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

with open('masterindex.idx', 'w') as idx_fil:
    for word in word_keys:
        
        files = word_occurrences[word].keys()
        idx_fil.write(str(word) + ":")

        for f in files:
            idx_fil.write(str(f) + ":" )
            idx_fil.write(str(word_occurrences[word][f]) + " ")
        idx_fil.write("\n")
        
txt_fil.close()
idx_fil.close()

