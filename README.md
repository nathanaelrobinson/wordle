# Wordle Solver
This is my attempt to build a Wordle solver. I've made a ton of changes since I first built this but I'm pretty happy with this version.
When you initiate a WordleSolver object it needs an initial `weights` matrix that gives it intelligence on how it chooses words when there
are multiple options. This is the _intelligent_ part of the program. It none are passed it will initalize with randomized weights.

The solving function goes through a few steps:
 - first it multiplies it's `clues_matrix` of known or green squares * it's `options_matrix` of non-eliminated letters. If this produces a full matrix we have a solution
 - next it uses set operations to eliminate all prior guesses and eliminated words from it's available options to reduce iteration cycles and comp time
 - lastly it multiplies the `options_matrix` * `weights` matrix and calulates the value of the matrix. The matrix with the highest value will be it's guess

It will continue this iterative guess and check process until it delivers the correct solution. I find that on average with a randomized weights matrix this
will solve the puzzle in ~5.5 guesses.

The next step is to "train" our weights matrix in an unsupervised manner. I do this via a genetic algorithm. I initiate a number of WordleSolver objects
with random weights and have them solve a varying number of times. The 2 solvers that perform the best are saved and used to populate the next generation.
This is done by taking a randomized portion of each matrix for each of their "children" and then randomly replacing values according to a "mutation" factor.
The goal is to use natural selection to derive the best possible starting weights matrix to solve wordle. I have found that the random matrix performs
better than a weights matrix made up of the probable likelihood of each letter in each position.

an example
```python
from wordle import WordleSolver
# initiate an object with a random weights matrix
a = WordleSolver()
# solve today's puzzle
a.solve('abbey')
a.print_results()
abask 🟩🟩🟨⬛️⬛️ 1/4
abmho 🟩🟩⬛️⬛️⬛️ 2/4
abnet 🟩🟩⬛️🟩⬛️ 3/4
abbey 🟩🟩🟩🟩🟩 4/4
```
You can test the genetic algorithm yourself and play with the results by tuning the number of solvers in the population, mutation factor, generations, and trial size

```python
from worldle import *
# set w to our final solver
w = genetic_simulation(pop_size=10, mutation_alpha=0.9, generations=5, trials=10)
Generation 0: Best Solver Score 6.0
Generation 1: Best Solver Score 6.0
Generation 2: Best Solver Score 5.333333333333333
Generation 3: Best Solver Score 5.0
Generation 4: Best Solver Score 4.5
```

Some interesting notes -- I found that I ran into bugs when using list comprehension to exclude previous guesses, that combined with really slow computation times, up to 30 seconds per solved made testing any type of genetic algo pretty hard. This led to the set operations to exclude guesses. One result of this is that we enforce that a guessed word must be a possible answer based on the available letters that haven't been eliminated. This means that the algorithm quickly reduces the numbers of items it has to iterate through and runs faster, but also may mean that it has less flexibility to guess. In any case when I did this thesolve times droped to < 3 seconds and typically < 6 guesses rather than 12-15. Before this there were some starting conditions that led to up to 100 guesses on some words.

The other interesting thing I want to investigate is how the weights matrix can change, or possibly be different in different guess stages. In early guesses it may want to optimize to a more random/broad approach to learn as much as possible before guessing, while later on it may want to attempt to choose the best words. I'll have to figure out a way to let that change between guess cycles.

It might also be worth wrapping the genetic algo into a multi-threaded script so that I can get the solvers running in parallel, I'm currently setting a very large popluation/sample size to test overnight since it takes a while to kick off any reasonable sized set and the results haven't converged very much.
