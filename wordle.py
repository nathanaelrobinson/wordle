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
        elif w in target:
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

def get_random_word():
    options = []
    with open('eligible_words.txt','r') as f:
        for word in f:
            options.append(word.strip())
    return random.choice(options)

class WordleSolver:
    def __init__(self, optional_weights=None):
        self.clues_array = np.zeros((26,5), dtype=int)
        self.options_array = np.ones((26,5), dtype=int)
        self.guesses_matrix = []
        self.guesses_text = []
        self.results = []
        options_list = []
        with open('eligible_words.txt', 'r') as f:
            for word in f:
                options_list.append(word.strip())
        # shuffle our list so it's not alphabetical
        random.shuffle(options_list)
        self.options = set(options_list)
        self.exclusion_set = set()
        
        # some old scoring stuff
        self.score = 0
        self.solved = False

        # initialize weights array, this is the intelligent part of the program
        # and will be updated by our ML model
        if optional_weights is not None:
            self.weights = optional_weights
        else:
            self.randomize_weights()
            # self.weights = np.load('base_weights.npy')

    def select_best_guess(self):
        # if we know everything -- use that
        truth_array = np.array([1, 1, 1, 1, 1])
        if np.array_equal(sum(self.clues_array * self.options_array), truth_array):
            best_guess = self.clues_array * self.options_array
            return best_guess

        updated_weights = self.weights * self.options_array
        best_val = 0
        available_options = self.options.difference(set(self.guesses_text))
        available_options = available_options.difference(self.exclusion_set)
        for option in available_options:
            # trying to reduce computation time, if we've already guessed
            # or the answer is infeasible add it to our exclusionary sets
            feasibility = sum(sum(self.options_array * text_to_matrix(option)))
            value = sum(sum(text_to_matrix(option) * updated_weights))
            # all letters have to be possible solutions
            if feasibility <  5:
                    self.exclusion_set.add(option)
            # finally determine it's weighted match value for a guess
            elif value > best_val:
                best_guess = text_to_matrix(option)
                best_val = value
        return best_guess
    
    def guess(self):
        # need a function to select our best guess
        # for now this is random, seen above
        guess_matrix = self.select_best_guess()
        guess_text = matrix_to_text(guess_matrix) 
        self.guesses_matrix.append(guess_matrix)
        self.guesses_text.append(guess_text)
        return guess_text

    def update_priors(self, guess_text, guess_result):
        for i, letter, result in zip(np.arange(0,6, dtype=int), guess_text, guess_result):
            if result == 'green':
                # first zero out all old yellow options
                # self.clues_array[LETTERS[letter], :] = 0
                # then mark known values as green
                self.clues_array[LETTERS[letter], i] = 1
                # finally zero out the options array for this position
                self.options_array[:, i] = 0
                self.options_array[LETTERS[letter], i] = 1
            elif result == 'yellow':
                # we simply set this value to existing all rows bc it may duplicate
                # and we'll just exclude it from it's current location
                self.clues_array[LETTERS[letter], :] = 1
                self.clues_array[LETTERS[letter], i] = 0
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
            print('%s %s %s/%s' %(guess_word, result_to_emojis(result), guess_num, total))
        return

    def guess_and_check(self, target):
        guess = self.guess()
        result = eval_guess(guess, target)
        self.results.append(result)
        self.update_priors(guess, result)
        self.score += score_guess(result)
        if score_guess(result) == 500:
            self.solved = True
        return

    def assess_performance(self):
        return len(self.guesses_text)
   
    def solve(self, target):
        while not self.solved:
            self.guess_and_check(target)
        # self.print_results()
        return 
    
    def reset(self):
        self.__init__(self.weights)
        return
    
    def randomize_weights(self):
        self.weights = np.random.rand(26,5)
        return

def initiate_starting_population(size):
    population = []
    for i in range(size):
        a = WordleSolver()
        population.append(a)
    return population

def simulate_wordles_n(population, n):
    results = []
    for a in population:
        scores = []
        for n in range(n):
            target = get_random_word()
            a.solve(target)
            scores.append(a.assess_performance())
            a.reset()
        result = {
                'weights' : a.weights,
                'avg_score' : sum(scores)/len(scores)
        }
        results.append(result)
    results_sorted = sorted(results, key = lambda i: i['avg_score'])
    return results_sorted

def make_next_generation(results, alpha):
    population_size = len(results)
    # select our top two performing from the population
    specimen_a = results[0]['weights']
    specimen_b = results[1]['weights']
    next_generation = []
    for i in range(population_size):
        # first randomly generate a weights matrix that is made up of A/B
        # will contribute the first n random rows, b the last (26-n)
        mix_factor = random.choice(np.arange(1,25, dtype=int))
        part_a = specimen_a[:mix_factor, :]
        part_b = specimen_a[mix_factor:, :]
        child = np.concatenate((part_a, part_b), axis=0)
        for i in range(26):
            for j in range(5):
                mutation = random.random()
                if mutation > alpha:
                    new_value = random.random()
                    child[i,j] = new_value
        a = WordleSolver(child)
        next_generation.append(a)
    return next_generation
    
def genetic_simulation(pop_size, mutation_alpha, generations, trials):
    pop = initiate_starting_population(pop_size)
    for i in range(generations):
        results = simulate_wordles_n(pop, trials)
        # create new population from fittest
        new_pop = make_next_generation(results, mutation_alpha)
        pop = new_pop
        print('Generation %s: Best Solver Score %s' %(i, results[0]['avg_score']))
    return WordleSolver(results[0]['weights'])

