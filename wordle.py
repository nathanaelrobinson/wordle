import numpy as np
import pandas as pd

LETTERS = {
    'a' : 0,
    'b' : 1,
    'c' : 2,
    'd' : 3,
    'e' : 4,
    'f' : 5,
    'g' : 6,
    'h' : 7,
    'i' : 8,
    'j' : 9,
    'k' : 10,
    'l' : 11,
    'm' : 12,
    'n' : 13,
    'o' : 14,
    'p' : 15,
    'q' : 16,
    'r' : 17,
    's' : 18,
    't' : 19,
    'u' : 20,
    'v' : 21,
    'w' : 22,
    'x' : 23,
    'y' : 24,
    'z' : 25
}

# HELPER FUNCTIONS TO RETRIEVE WORDS
# words = []
# with open("words_alpha.txt", "r") as f:
#    for word in f:
#        word_clean = word.strip()
#        if len(word_clean) == 5:
#             words.append(word_clean)

def turn_word_into_matrix(word):
    matrix = np.zeros((5,26), dtype=int)
    for i in range(0,5):
        column = LETTERS[word[i]]
        matrix[i][column] = 1
    return matrix

def turn_matrix_into_word(matrix):
    letter_vector = np.arange(0,26,1, dtype=int)
    positions_reversed = {key: value for (value, key) in LETTERS.items()}
    word = []
    for i in range(0,5):
        vector = matrix[i]
        position = np.sum(vector*letter_vector)
        word.append(positions_reversed[position])
    return "".join(word)

def score_guess(word, target):
    # first check if we guessed correctly to reduce comp time
    if word == target:
        return ['green', 'green', 'green', 'green', 'green']
    result = []
    for w, t in zip(word, target):
        if w == t:
            value = 'green'
        elif w in target:
            value = 'yellow'
        else:
            value = 'red'
        result.append(value)
    return result
        
def convert_guess_to_arrays(word, result_vector):
    # some code here need to figure out format
