import sys
import os
import string
import re


def index_text_file(txt_filename, idx_filename, delimiter_chars=",.;:!?"):
    txt_fil = open(txt_filename, "r")

    word_occurrences = {}
    pos = 0

    for lin in txt_fil:
        lin = lin.lower()
        words = re.findall(r'\b\w[\w-]*\b', lin.lower())

        for word in words:
                pos += lin.find(word)
                
                if word in word_occurrences:
                    word_occurrences[word].append(pos)
                else:
                    word_occurrences[word] = [ pos ]
        pos += len(lin) - 1
    
    word_keys = word_occurrences.keys()
    print ("{} unique words.".format(len(word_keys)))

    word_keys = word_occurrences.keys()
    word_keys = sorted(word_keys)

    idx_fil = open(idx_filename, "w")

    for word in word_keys:
        line_nums = word_occurrences[word]
        idx_fil.write(word + " ")

        for line_num in line_nums:
            idx_fil.write(str(line_num) + " ")

        idx_fil.write("\n")
    
    txt_fil.close()
    idx_fil.close()

index_text_file("/Users/jaganmohan/Python/IR_Assignments/TFIDF/files/jerusalem.txt", "jerusalem_index.idx")