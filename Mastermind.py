import random
from collections import Counter


class Game:
    def __init__(self, slots, options):
        self._slots = slots
        self._options = options
        self.guesses = set()
        self._num_guess = 0
        self._code = []
        for i in range(slots):
            self._code.append(random.randint(0, options - 1))
        self._code_count = Counter(self._code)

    def check_guess(self, guess):
        win_status = 0
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

        if correct_slots == self._slots:
            win_status = 1

        return win_status
