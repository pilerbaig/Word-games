import random
import colorama
from colorama import Fore, Back, Style

with open("wordle_guesslist.txt") as f:
    guess_words = {i.strip() for i in f}

with open("wordle_answerlist.txt") as f:
    answer_words = {i.strip() for i in f}


def construct_wordle():
    wordle = random.choice(tuple(answer_words))
    return wordle


def display(wordle, word):
    editing = ""
    letters = word
    for i in range(len(word)):
        if word[i] == wordle[i]:
            editing += Back.GREEN + word[i]
            letters = letters.replace(word[i], "", 1)
        elif word[i] in wordle:
            editing += Back.YELLOW + word[i]
            letters = letters.replace(word[i], "", 1)
        else:
            editing += Back.RESET + word[i]
    return editing + Back.RESET


def repl(verbose=False):
    """
    REPL
    """
    import traceback

    wordle = None
    progress = ""
    count = 0
    while True:
        if not wordle:
            wordle = construct_wordle()
        if wordle:
            if not progress:
                print("---------- New Game ----------")
            else:
                print(progress)
        print(" ")
        input_str = input("in> ")
        if not input_str:
            print("---------- Not a valid command! ----------")
            continue
        if input_str == "QUIT":
            return
        if input_str == "RESTART":
            wordle = None
            progress = ""
            count = 0
            continue
        inp_command = input_str.split()

        if inp_command[0] == "guess":
            if len(inp_command) == 2:
                if inp_command[1] in guess_words:
                    progress += "\n" + display(wordle, inp_command[1])
                    count += 1
                    if inp_command[1] == wordle:
                        print(progress)
                        print("---------- Correct! You win! ----------")
                        wordle = None
                        progress = ""
                        count = 0
                        continue
                    elif count == 6:
                        print(progress)
                        print("---------- Out of guesses! You lose... ----------")
                        print("The correct word was: " + wordle)
                        wordle = None
                        progress = ""
                        count = 0
                        continue
                else:
                    print("---------- Not a valid word! ----------")
            else:
                print("---------- Guess takes in 2 arguments! ----------")
        elif inp_command[0] == "solve":
            if len(inp_command) == 1:
                print("---------- Revealing solution! ----------")
                print("The word was: " + wordle)
                wordle = None
                progress = ""
                count = 0
                continue
            else:
                print("---------- solve takes in no arguments! ----------")
        else:
            print("---------- Not a valid command! ----------")


repl(True)
