from config import *
from tree import TreeNode
import numpy as np
import time
import json

def load_words():
    fans = open(answers_path, "r")
    fall = open(allowed_words_path, "r")
    answers = (fans.read().splitlines())
    allowed = np.concatenate((answers, fall.read().splitlines()))
    fans.close()
    fall.close()
    return allowed, answers

def build_tree(allowed, answers):
    best_tree = None
    for i in range(0, len(allowed)):
        word = allowed[i]
        start = time.time()
        current_tree = TreeNode(word, allowed, answers)
        if best_tree is None or current_tree.weigh() < best_tree.weigh():
            best_tree = current_tree
        print(i + 1, "/", len(allowed), "time:", time.time() - start, "seconds")
    
    return best_tree

def run():
    allowed, answers = load_words()
    start = time.time()
    tree = build_tree(allowed, answers).serialize()
    print("TOTAL COMPUTATION TIME:", time.time() - start, "seconds")
    save_tree = open(tree_path, "w")
    save_tree.write(json.dumps(tree))
    save_tree.close()