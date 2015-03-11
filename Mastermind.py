import random
from collections import Counter


class Game:
    def __init__(self, slots, options, code=None):
        self._slots = slots
        self._options = options
        self.guesses = set()
        self._num_guess = 0

        if code:
            self._code = code
        else:
            self._code = list()
            for i in range(slots):
                self._code.append(random.randint(0, options - 1))

        self._code_count = Counter(self._code)

    def check_guess(self, guess):

        digit_count = Counter(guess)

        correct_digits = 0
        for digit in digit_count:
            if digit_count[digit] > self._code_count[digit]:
                correct_digits += self._code_count[digit]
            else:
                correct_digits += digit_count[digit]

        correct_slots = 0
        for i in range(self._slots):
            if self._code[i] == guess[i]:
                correct_slots += 1

        self.guesses.add((tuple(guess), correct_slots, correct_digits - correct_slots))
        self._num_guess += 1

        return (tuple(guess), correct_slots, correct_digits - correct_slots)
