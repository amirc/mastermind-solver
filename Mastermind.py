import random
from collections import Counter


class Game:
    def __init__(self, slots, options):
        self.slots = slots
        self.options = options
        self.guesses = set()
        self.numGuess = 0
        self.code = []
        for i in range(slots):
            self.code.append(random.randint(0, options - 1))
        self.codeCount = Counter(self.code)

    def check_guess(self, guess):
        win_status = 0
        digit_count = Counter(guess)

        correct_digits = 0
        for digit in digit_count:
            if digit_count[digit] > self.codeCount[digit]:
                correct_digits += self.codeCount[digit]
            else:
                correct_digits += digit_count[digit]

        correct_slots = 0
        for i in range(self.slots):
            if self.code[i] == guess[i]:
                correct_slots += 1

        self.guesses.add((tuple(guess), correct_slots, correct_digits - correct_slots))
        self.numGuess += 1

        if correct_slots == self.slots:
            win_status = 1

        return win_status
