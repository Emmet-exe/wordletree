import numpy
import string
import random

alphabet_string = string.ascii_lowercase
def alphabet_dict():
    return [{char:0 for char in alphabet_string}]*5

def best_word(word_list, possible_words, guessed_words, yellow_memory, green_memory):
    if len(possible_words) == 1:
        return possible_words[0]

    adict = alphabet_dict()
    for word in possible_words:
        already = False
        for i in range(0, len(word)):
            l = word[i]
            for letter in adict[i].keys():
                if letter == l:
                    if already:
                        adict[i][letter] += 0.25
                    else:
                        adict[i][letter] += 1
                        already = True

    max_score = 0
    best_word = possible_words[0]
    for word in word_list:
        score = 0

        for i in range(0, len(word)):
            letter = word[i]
            if not letter in yellow_memory[i]:
                if letter in word[:i]:
                    score += get_letter_value(adict, letter, i, len(possible_words)) * 0.1
                else:
                    score += get_letter_value(adict, letter, i, len(possible_words))
            if letter in green_memory[i]:
                if len(possible_words) <= 3:
                    score += 5 * get_letter_value(adict, letter, i, len(possible_words)) / len(possible_words)
                else:
                    score += get_letter_value(adict, letter, i, len(possible_words))
        if score > max_score and word not in guessed_words:
            max_score = score
            best_word = word

    return best_word

def get_letter_value(adict, letter, position, words_left):
    return 1.25 * adict[position][letter] + sum((adict[i][letter] for i in range(0, len(adict))))
    #return adict[position][letter]//float(words_left) + -1*((sum((adict[i][letter] for i in range(0, len(adict))))/float(words_left))-.5)**2 + .25

def clean(guess, info, possible_words, yellow_memory, green_memory):
    not_in_word = []
    correct_slot = {}
    incorrect_slot = {}
    valid = False
    possible_words = numpy.delete(possible_words, numpy.where(possible_words == guess))
    while not valid:
        if info == None:
            info = input("Please input guess results (ex. bbgby): ")
        if len(info) != 5:
            print("Please enter a string 5 characters long!")
            continue
        valid = True
        for i in range(0, len(guess)):
            result = info[i]
            if result  == "b":
                not_in_word.append(guess[i])
            elif result == "g":
                correct_slot[i] = guess[i]
                green_memory[i] += guess[i]
            elif result == "y":
                incorrect_slot[i] = guess[i]
                yellow_memory[i] += guess[i]
            else:
                info = None
                valid = False

    i = 0
    cap = len(possible_words)
    while i < cap:
        delete = False
        word = possible_words[i]
        for j in range(0, len(word)):
            letter = word[j]
            if j in correct_slot.keys() and letter != correct_slot[j]:
                delete = True
            elif j in incorrect_slot.keys() and letter == incorrect_slot[j]:
                delete = True
            if letter in not_in_word:
                delete = True
            if delete:
                possible_words = numpy.delete(possible_words, i)
                cap -= 1
                break
        if not delete:
            for letter in incorrect_slot.values():
                if not letter in word:
                    delete = True
                    possible_words = numpy.delete(possible_words, i)
                    cap -= 1
                    break
        if not delete:
            i += 1
    return possible_words

def get_feedback(guess, answer):
    feedback = ""
    for i in range(0, len(guess)):
        if guess[i] == answer[i]:
            feedback += "g"
        elif guess[i] in answer:
            feedback += "y"
        else:
            feedback += "b"
    return feedback

def load_words():
    fans = open("answers.txt", "r")
    fall = open("allowed.txt", "r")
    word_list = numpy.concatenate((fans.read().splitlines(), fall.read().splitlines()))
    fans.close()
    fall.close()
    return word_list

def solve_auto(answer):
    word_list = load_words()
    possible_words = numpy.copy(word_list)

    print("Answer in advance:", answer)
    guessed_words = []
    yellow_memory = {i:"" for i in range(0, len(answer))}
    green_memory = {i:"" for i in range(0, len(answer))}
    while len(guessed_words) == 0 or guessed_words[-1] != answer:
        guess = best_word(word_list, possible_words, guessed_words, yellow_memory, green_memory)
        guessed_words.append(guess)
        print("Guessing", guess.upper() + "...")
        feedback = get_feedback(guess, answer)
        print("Feedback:", feedback, "(" + str(len(possible_words)) + " possibilities)")
        possible_words = clean(guess, feedback, possible_words, yellow_memory, green_memory)
        print("Successfully narrowed search to", len(possible_words), "words.")
    print("The word is", answer, "(" + str(len(guessed_words)) + " guesses)", "\n--------------------------")
    return len(guessed_words)

def solve_manual():
    word_list = load_words()
    possible_words = numpy.copy(word_list)
    length = 5

    guessed_words = []
    yellow_memory = {i:"" for i in range(0, length)}
    green_memory = {i:"" for i in range(0, length)}
    while len(possible_words) > 1:
        guess = best_word(word_list, possible_words, guessed_words, yellow_memory, green_memory)
        guessed_words.append(guess)
        print("Guessing", guess.upper() + "...")
        possible_words = clean(guess, None, possible_words, yellow_memory, green_memory)
    if (len(possible_words)) == 1:
        print(possible_words)[0]
def gen_test_set():
    fans = open("answers.txt", "r")
    randos = random.sample(fans.read().splitlines(), 100)
    fans.close()
    return randos

def run_test_set():
    ftest = open("testset.txt", "r")
    test_set = ftest.read().splitlines()
    total = 0
    for word in test_set:
        total += solve_auto(word)
    avg = total / float(len(test_set))
    print(avg)


run_test_set()
solve_manual()
# solve_auto("crane")