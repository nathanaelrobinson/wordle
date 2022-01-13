import numpy as np
import pandas as pd
import random

# HELPER FUNCTIONS TO RETRIEVE WORDS
# words = []
# with open("words_alpha.txt", "r") as f:
#    for word in f:
#        word_clean = word.strip()
#        if len(word_clean) == 5:
#             words.append(word_clean)

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

IMAGES = {
    'green' : '🟩',
    'yellow' : '🟨',
    'black' : '⬛️'
}

# initialize some kind of score keeper for value of a cell
SCORES = {
    'green' : 100,
    'yellow' : 10,
    'black' : 5
}

def result_to_emojis(result):
    emojis = [IMAGES[i] for i in result]
    return "".join(emojis)

def text_to_matrix(word):
    matrix = np.zeros((26,5), dtype=int)
    for column in range(0,5):
        row = LETTERS[word[column]]
        matrix[row, column] = 1
    return matrix

def matrix_to_text(matrix):
    letter_vector = np.arange(0,26,1, dtype=int)
    positions_reversed = {key: value for (value, key) in LETTERS.items()}
    word = []
    for i in range(0,5):
        vector = matrix[:,i]
        position = np.sum(vector*letter_vector)
        word.append(positions_reversed[position])
    return "".join(word)

def eval_guess(word, target):
    # first check if we guessed correctly to reduce comp time
    if word == target:
        return ['green', 'green', 'green', 'green', 'green']
    result = []
    for w, t in zip(word, target):
        if w == t:
            value = 'green'
        elif any(w == i for i in target):
            value = 'yellow'
        else:
            value = 'black'
        result.append(value)
    return result
       
def score_guess(result):
    score = 0
    for color in result:
        score += SCORES[color]
    return score

class WordleSolver:
    def __init__(self):
        self.clues_array = np.zeros((26,5), dtype=int)
        self.options_array = np.ones((26,5), dtype=int)
        # initialize weights array, this is the intelligent part of the program
        # and will be updated by our ML model
        self.weights = np.full((26, 5), 0.2)
        self.guesses_matrix = []
        self.guesses_text = []
        self.results = []
        self.options = np.load('eligible_words.npy')
        self.score = 0

    def select_best_guess(self):
        # if we know everything -- use that
        truth_array = np.array([1, 1, 1, 1, 1])
        if np.array_equal(sum(self.clues_array * self.options_array), truth_array):
            guess_matrix = self.clues_array * self.options_array
        # use a random function to retrieve guess for now
        else:
            random_int = random.randrange(len(self.options))
            guess_matrix = self.options[random_int]
        return guess_matrix
    
    def guess(self):
        # need a function to select our best guess
        # for now this is random, seen above
        guess_matrix = self.select_best_guess()
        guess_text = matrix_to_text(guess_matrix) 
        self.guesses_matrix.append(guess_matrix)
        self.guesses_text.append(guess_text)
        return guess_text

    def update_priors(self, guess_text, guess_result):
        for i, letter, result in zip(range(0,6), guess_text, guess_result):
            if result == 'green':
                # first zero out all old yellow options
                self.clues_array[LETTERS[letter], :] = 0
                # then mark known values as green
                self.clues_array[LETTERS[letter], i] = 1
                # finally zero out the options array for this position
                self.options_array[:, i] = 0
                self.options_array[LETTERS[letter], i] = 1
            elif result == 'yellow':
                # we simply set this value to existing all rows bc it may duplicate
                # and we'll just exclude it from it's current location
                self.clues_array[LETTERS[letter], :] = 1
                # we can still update the options array
                self.options_array[LETTERS[letter], i] = 0
            elif result == 'black':
                # this letters row in the options array is zero
                # it cannot be guessed again
                self.options_array[LETTERS[letter], :] = 0
        return

    def print_results(self):
        total = len(self.guesses_text)
        for guess_num, guess_word, result in zip(range(1, len(self.guesses_text)+1), self.guesses_text, self.results):
            print('%s/%s %s %s' %(guess_num, total, guess_word, result_to_emojis(result)))

    def guess_and_check(self, target):
        guess = self.guess()
        result = eval_guess(guess, target)
        self.results.append(result)
        self.update_priors(guess, result)
        self.score = score_guess(result)
        return

    def run_sim(self):
        target = input('Input a five letter word: ')
        while self.score < 500:
            self.guess_and_check(target)
        self.print_results()
        return
    def reset(self):
        self.__init__()
