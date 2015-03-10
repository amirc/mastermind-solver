import random
from collections import Counter

class game:
    def __init__(self, slots, options):
        self.slots = slots
        self.options = options
        self.guesses = set()
        self.numGuess = 0
        self.code = []
        for i in range(slots):
            self.code.append(random.randint(0, options-1))
        self.codeCount = Counter(self.code)
            
    def checkGuess(self, guess):
        winStatus = 0
        digitCount = Counter(guess)
        
        correctDigits = 0
        for digit in digitCount:
            if digitCount[digit] > self.codeCount[digit]:
                correctDigits += self.codeCount[digit]
            else:
                correctDigits += digitCount[digit]
                
        correctSlots = 0
        for i in range(self.slots):
            if(self.code[i] == guess[i]):
                correctSlots += 1
                
        self.guesses.add((tuple(guess), correctSlots, correctDigits-correctSlots))
        self.numGuess += 1

        if correctSlots == self.slots:
            winStatus = 1

        return winStatus
