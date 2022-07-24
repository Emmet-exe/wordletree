from wordtree import load_words
import string
from itertools import combinations
from config import word_length
import json

def is_match(combo, word):
    word = ''.join(sorted(set(word)))
    for i in range(0, len(combo)):
        try:
            if combo[i] != word[i] and combo[i].islower():
                return False
        except:
            if combo[i].islower():
                return False
    return True


allowed, answers = load_words()
alphabet = string.ascii_lowercase + string.ascii_uppercase
combos = combinations(alphabet, word_length)
cdict = {''.join(c): [] for c in combos}
for c in cdict:
    print(c)
    for word in answers:
        if is_match(c, word):
            cdict[c].append(word)


with open('combination_dict.json', 'w') as convert_file:
     convert_file.write(json.dumps(cdict))