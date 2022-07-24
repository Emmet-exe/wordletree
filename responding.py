import numpy as np
import itertools 
from config import *

def parse_colors(feedback):
    for color in color_symbols:
        feedback.replace(color, color_symbols[color])
    return feedback

def respond(guess, answer):
    feedback = ""
    for i in range(0, len(guess)):
        if guess[i] == answer[i]:
            feedback += symbols[2]
        elif guess[i] in answer:
            feedback += symbols[1]
        else:
            feedback += symbols[0]
    return feedback