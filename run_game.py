from CSP import CSP
from Mastermind import Game
import statistics
from collections import Counter
from time import time
import sys


def main(args):
    try:
        slots = int(args[0])
        options = int(args[1])
        games = int(args[2])
        assert (slots > 0 and options > 0 and games > 0)

    except:
        print(
            "Usage: Please input three positive integers for the number of slots, the number of options and number of games.")
        sys.exit(2)

    codes = []
    scores = []

    begin = time()
    for i in range(games):
        game = Game(slots, options)
        csp = CSP(slots, options)
        while True:
            guess = csp.generate_guess()
            result = game.check_guess(guess)
            if result[1] == game._slots:
                break
            csp.insert_guess(result[0], result[1], result[2])
        scores.append(game._num_guess)
        codes.append(game.guesses)

    end = time()

    print("Mean: ", statistics.mean(scores))
    print("Variance: ", statistics.variance(scores))
    print("Counter: ", Counter(scores))
    worst_i = max(range(games), key=lambda i: scores[i])
    best_i = min(range(games), key=lambda i: scores[i])
    print("Worst: ", codes[worst_i], scores[worst_i])
    print("Best: ", codes[best_i], scores[best_i])
    print("Average time (in seconds) per game: ", (end - begin) / games)
    print("Average time (in seconds) per guess: ", (end - begin) / sum(scores))


if __name__ == '__main__':
    main(sys.argv[1:])