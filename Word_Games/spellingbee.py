import random
import colorama
from colorama import Fore, Back, Style

with open("wordlist.txt") as f:
    ALL_WORDS = {i.strip() for i in f}

valid_words = {word for word in ALL_WORDS if len(word) >= 4}
constructor_words = {
    word
    for word in ALL_WORDS
    if len(set(word)) == 7 and not ("e" in word and "r" in word) and "s" not in word
}


def construct_puzzle(args=None):
    if args is None:
        constructor = random.choice(tuple(constructor_words))
        constructor_letters = set(constructor)
        middle_letter = random.choice(tuple(constructor_letters))
        args = (constructor, middle_letter)
    constructor_letters = set(args[0])
    solutions = {
        word
        for word in valid_words
        if set(word).issubset(constructor_letters) and args[1] in word
    }
    ordered_letters = constructor_letters.copy()
    ordered_letters.remove(args[1])
    ordered_letters = list(ordered_letters)
    pangrams = {solution for solution in solutions if solution in constructor_words}
    return {
        "letters": constructor_letters,
        "ordered_letters": ordered_letters,
        "middle": args[1],
        "solutions": solutions,
        "pangrams": pangrams,
    }


def display(puzzle, guessed):
    print("---------- GAME ----------")
    print(
        " "
        + Back.WHITE
        + " "
        + puzzle["ordered_letters"][0]
        + "   "
        + puzzle["ordered_letters"][1]
        + " "
        + Back.RESET
    )
    print(
        Back.WHITE
        + " "
        + puzzle["ordered_letters"][2]
        + " "
        + Back.YELLOW
        + " "
        + puzzle["middle"]
        + " "
        + Back.WHITE
        + " "
        + puzzle["ordered_letters"][3]
        + " "
        + Back.RESET
    )
    print(
        " "
        + Back.WHITE
        + " "
        + puzzle["ordered_letters"][4]
        + "   "
        + puzzle["ordered_letters"][5]
        + " "
        + Back.RESET
    )
    print(" ")
    print("GUESSED:", sort_words(guessed))


def guess_word(word, puzzle, guessed):
    if word in puzzle["solutions"] and word not in guessed:
        print("---------- Correct! ----------")
        if word in puzzle["pangrams"]:
            print("---------- Pangram! ----------")
        guessed.add(word)
    elif word in guessed:
        print("--------- Already guessed... ----------")
    else:
        print("---------- Not a valid word. ----------")


def hint(puzzle, guessed):
    left_to_guess = puzzle["solutions"].difference(guessed)
    word_lengths = {}
    for word in left_to_guess:
        word_lengths[len(word)] = word_lengths.setdefault(len(word), 0) + 1
    sorted_keys = sorted(word_lengths.keys())
    print("---------- HINTS ----------")
    for length in sorted_keys:
        print("Length " + str(length) + ": " + str(word_lengths[length]))
    print("Pangrams: " + str(len(puzzle["pangrams"].difference(guessed))))


def sort_words(word_set):
    all_words = []
    word_lengths = {}
    for word in word_set:
        word_lengths[len(word)] = word_lengths.setdefault(len(word), []) + [word]
    sorted_keys = sorted(word_lengths.keys())
    for length in sorted_keys:
        all_words.extend(sorted(word_lengths[length]))
    return all_words


def rearrange(puzzle):
    random.shuffle(puzzle["ordered_letters"])


def repl(verbose=False):
    """
    REPL
    """
    import traceback

    puzzle = None
    guessed = set()
    while True:
        if puzzle:
            display(puzzle, guessed)
        print(" ")
        input_str = input("in> ")
        if not input_str:
            print("---------- Not a valid command! ----------")
            continue
        if input_str == "QUIT":
            return
        if input_str == "RESTART":
            puzzle = None
            guessed = set()
            continue
        inp_command = input_str.split()
        if inp_command[0] == "construct":
            if puzzle:
                print("---------- Already in a game! ----------")
            else:
                if inp_command[0] == "construct":
                    args = inp_command[1:]
                    if not args:
                        puzzle = construct_puzzle()
                    elif len(args) != 2:
                        print("---------- Construct takes 2 arguments! ----------")
                    elif args[0] not in constructor_words:
                        print("---------- Not a valid constructor! ----------")
                    elif args[1] not in args[0]:
                        print(
                            "---------- Middle letter is not in the puzzle! ----------"
                        )
                    else:
                        puzzle = construct_puzzle(args)
        elif inp_command[0] == "guess":
            if not puzzle:
                print("---------- There is no active puzzle! ----------")
            elif len(inp_command[1:]) != 1:
                print("--------- Guess takes one argument! ----------")
            else:
                guess_word(inp_command[1], puzzle, guessed)
                if guessed == puzzle["solutions"]:
                    print("---------- You have solved the puzzle! ----------")
                    print(sort_words(puzzle["solutions"]))
                    puzzle = None
                    guessed = set()
                    continue
        elif inp_command[0] == "hint":
            if not puzzle:
                print("---------- There is no active puzzle! ----------")
            elif len(inp_command) != 1:
                print("---------- Hint takes no arguments! ----------")
            else:
                hint(puzzle, guessed)
        elif inp_command[0] == "shuffle":
            if not puzzle:
                print("---------- There is no active puzzle! ----------")
            elif len(inp_command) != 1:
                print("---------- Shuffle takes no arguments! ----------")
            else:
                rearrange(puzzle)
        elif inp_command[0] == "solve":
            if not puzzle:
                print("---------- There is no active puzzle! ----------")
            elif len(inp_command) != 1:
                print("---------- Shuffle takes no arguments! ----------")
            else:
                print(sort_words(puzzle["solutions"]))
                puzzle = None
                guessed = set()
                continue
        else:
            print("---------- Not a valid command! ----------")

            #         inp_str = input("constructor: ")
            # if inp_str == "QUIT":
            #     return
            # if inp_str == "RESTART":
            #     puzzle = None
            #     constructor = None
            #     middle_letter = None
            #     continue
            # if not inp_str:
            #     break
            # if constructor not in constructor_words:
            #     print("Not a valid constructor!")
            #     continue
            # middle_letter = input("middle: ")
            # if middle_letter == "QUIT":
            #     return
            # if middle_letter == "RESTART":
            #     puzzle = None
            #     continue
            # if not middle_letter:
            #     middle_letter = None
            # if middle_letter not in constructor:
            #     print("Not a valid middle letter!")
            #     continue
            # puzzle = construct_puzzle((constructor, middle_letter))


repl(True)
# construct_puzzle("blocked", "c")
