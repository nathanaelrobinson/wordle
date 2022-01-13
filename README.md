# Wordle Solver
This is my attempt to build a Wordle solver. Currently there is very minimal functionality.
If you run the simpulation in the worldle object against a target word, the model will begin by
randomly chosing words from the list of english 5-letter words. Using the information it gathers
from it's guesses it will attempt to solve the puzzle. After it solves it will display it's answer
and how long it took to solve

an example
```python
$ from wordle import WordleSolver
$ a = WordleSolver()
$ a.run_sim()
Input a five letter word: favor
# I will use today's puzzle word as an example
1/19 gipsy ⬛️⬛️⬛️⬛️⬛️
2/19 arrah 🟨🟨🟨🟨⬛️
3/19 dazed ⬛️🟩⬛️⬛️⬛️
4/19 quest ⬛️⬛️⬛️⬛️⬛️
5/19 pined ⬛️⬛️⬛️⬛️⬛️
6/19 ontal 🟨⬛️⬛️🟨⬛️
7/19 kapur ⬛️🟩⬛️⬛️🟩
8/19 dumbs ⬛️⬛️⬛️⬛️⬛️
9/19 groin ⬛️🟨🟨⬛️⬛️
10/19 khass ⬛️⬛️🟨⬛️⬛️
11/19 junky ⬛️⬛️⬛️⬛️⬛️
12/19 hurls ⬛️⬛️🟨⬛️⬛️
13/19 fauna 🟩🟩⬛️⬛️🟨
14/19 nyala ⬛️⬛️🟨⬛️🟨
15/19 meach ⬛️⬛️🟨⬛️⬛️
16/19 agora 🟨⬛️🟨🟨🟨
17/19 vegas 🟨⬛️⬛️🟨⬛️
18/19 juror ⬛️⬛️🟨🟩🟩
19/19 favor 🟩🟩🟩🟩🟩
```

Included in the world object is a scoring mechanism and weight matrix. The next step will be to use a genetic algorithm to update the weight
function so that it "learns" what are the best guesses and how to most effectively guess the words.

