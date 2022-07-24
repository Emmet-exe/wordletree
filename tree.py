from re import A
import numpy as np
from responding import *
from config import *

class TreeNode:
    def __init__(self, word, allowed_dict, answer_dict, depth=1, best_alt_remaining=-1):
        self.word = word
        self.words_left = len(answer_dict)
        self.children = {}
        self.depth = depth
        self.total_remaining = 0
        if best_alt_remaining != -1 and self.words_left >= best_alt_remaining * word_tolerance:
            self.weight = max_guesses + 1
        elif self.words_left == 1 or depth == max_guesses:
            self.weight = 1
        else:
            if self.words_left > 1 and depth < max_guesses:
                allowed_dict = np.delete(allowed_dict, np.where(allowed_dict == word))
                answer_dict = np.delete(answer_dict, np.where(answer_dict == word))
                self.gen_subtrees(allowed_dict, answer_dict)
                self.weight = 1 + sum([child.weigh() for child in self.children.values()]) / float(len(self.children))
    
    def gen_subtrees(self, allowed_dict, answer_dict):
        for answer in answer_dict:
            feedback = respond(self.word, answer)
            abridged_dict = self.shrink_dict(answer_dict, self.word, feedback)
            self.total_remaining += len(abridged_dict)
            if len(abridged_dict) == 1:
                if abridged_dict[0] != self.word:
                    self.children[feedback] = TreeNode(abridged_dict[0], abridged_dict, abridged_dict, self.depth + 1)
            else:
                for guess in allowed_dict:
                    try:
                        alt = self.children[feedback].get_total_remaining()
                    except:
                        alt = -1
                    potential_child = TreeNode(guess, allowed_dict, abridged_dict, self.depth + 1, alt)
                    if (not feedback in self.children) or potential_child.weigh() < self.children[feedback].weigh():
                        self.children[feedback] = potential_child

    @staticmethod
    def shrink_dict(pw, guess, feedback):
        for i in range(len(pw)-1, -1, -1):
            delete = False
            word = pw[i]
            for j in range(0, len(word)):
                # contains grey letter
                if feedback[j] == symbols[0] and word.find(guess[j]) >= 0:
                    delete = True
                elif feedback[j] == symbols[1]:
                    # has yellow letter in original location or does not have it at all
                    if guess[j] == word[j] or not word.find(guess[j]) >= 0:
                        delete = True
                elif feedback[j] == symbols[2] and not guess[j] == word[j]:
                    delete = True
                if delete:
                    pw = np.delete(pw, i)
                    break
        return pw

    def weigh(self):
        return self.weight
    
    def get_total_remaining(self):
        return self.total_remaining

    def next_guess(self, feedback):
        return self.children[feedback]
    
    def serialize(self):
        return {self.word: {child: self.children[child].serialize() for child in self.children}}

    def as_text(self):
        return "--> (" + self.self.word + ",", self.words_left, "remaining)"

