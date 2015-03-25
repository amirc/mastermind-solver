from collections import Counter
from copy import copy
from math import factorial
import random
from CSP import CSP


def random_guess(game_config, state):
    def new_rnd():
        ret_val = list()
        for i in range(game_config.slots):
            ret_val.append(random.randint(0, game_config.options - 1))
        return ret_val

    res = new_rnd()

    while res in map(lambda attempt: attempt[0], state):
        res = new_rnd()

    return res


def min_guess(game_config, state):
    csp = CSP(game_config.slots, game_config.options)
    for guess, bulls, cows in state:
        csp.insert_guess(guess, bulls, cows)

    res = list()
    min_index = [-1] * game_config.slots

    for i in range(game_config.slots):
        res.append(csp._order_val(i)[min_index[i]])

    while res in map(lambda attempt: attempt[0], state):
        min_index[random.choice(game_config.slots)] -= 1
        for i in range(game_config.slots):
            res.append(csp._order_val(i)[min_index[i]])

    return res


def new_guess(game_config, state):
    guessed_times = Counter()
    for guess, bulls, cows in state:
        guessed_times.subtract(guess)

    available_keys = set(range(game_config.options)).difference(set(guessed_times))
    missing_args = game_config.slots - len(available_keys)
    available_keys.update(set([k for k, v in guessed_times.most_common(missing_args)]))

    available_keys = list(available_keys)

    def generate_res():
        tmp_res = list()
        for i in range(game_config.slots):
            tmp_res.append(random.choice(available_keys))
        return tmp_res

    res = generate_res()
    while res in map(lambda attempt: attempt[0], state):
        res = generate_res()

    return res


def max_guess(game_config, state):
    csp = CSP(game_config.slots, game_config.options)
    for guess, bulls, cows in state:
        csp.insert_guess(guess, bulls, cows)

    res = list()
    max_index = [0] * game_config.slots

    for i in range(game_config.slots):
        res.append(csp._order_val(i)[max_index[i]])

    while res in map(lambda attempt: attempt[0], state):
        max_index[random.choice(game_config.slots)] += 1
        for i in range(game_config.slots):
            res.append(csp._order_val(i)[max_index[i]])

    return res


def all_different_guess(game_config, state):
    numbers = list(range(game_config.options))
    res = list()
    for i in range(game_config.slots):
        tmp = random.choice(numbers)
        res.append(tmp)
        numbers.remove(tmp)

    return res


def max_valid_guess(game_config, state):
    csp = CSP(game_config.slots, game_config.options, 2)
    for guess, bulls, cows in state:
        csp.insert_guess(guess, bulls, cows)

    return csp.generate_guess()


def valid_guess(game_config, state):
    csp = CSP(game_config.slots, game_config.options, 1)
    for guess, bulls, cows in state:
        csp.insert_guess(guess, bulls, cows)

    return csp.generate_guess()
    '''
    def recursive_valid_guess(slot, cur_res=list()):
        if slot == game_config.slots:
            return cur_res
        options = list(range(game_config.options))
        random.shuffle(options)
        for i in options:
            tmp_res = copy(cur_res)
            tmp_res += [[slot, i]]
            if csp._is_sol_valid(dict(tmp_res)):
                tmp_res = recursive_valid_guess(slot + 1, tmp_res)
                if tmp_res:
                    return tmp_res

        return False

    def to_ans(arr):
        ans = [0] * game_config.slots
        for k, v in arr:
            ans[k] = v
        return ans

    return to_ans(recursive_valid_guess(0))
    '''

def guesses_combination_guess(game_config, state):
    def new_rnd():
        tmp = list()
        for i in range(game_config.slots):
            tmp.append(random.choice([guess[i] for guess, bulls, cows in state]))
        return tmp

    res = new_rnd()

    while res in map(lambda attempt: attempt[0], state):
        res = new_rnd()

    return res


class Action(object):
    def __init__(self, game_config):
        self._game_config = game_config

    def valid(self, state):
        return True


class AllDifferentGuess(Action):
    def __init__(self, game_config):
        super().__init__(game_config)
        self._counter = 0
        self._options = factorial(game_config.options) / factorial(game_config.options - game_config.slots)
        self.action = self.all_diff_guess

    def all_diff_guess(self, game_config, state):
        self._counter += 1
        return all_different_guess(game_config, state)

    def valid(self, state):
        return self._counter < self._options


class RandomGuess(Action):
    def __init__(self, game_config):
        super().__init__(game_config)
        self.action = random_guess


class MaxGuess(Action):
    def __init__(self, game_config):
        super().__init__(game_config)
        self.action = max_guess


class NewGuess(Action):
    def __init__(self, game_config):
        super().__init__(game_config)
        self.action = new_guess


class ValidGuess(Action):
    def __init__(self, game_config):
        super().__init__(game_config)
        self.action = valid_guess


class MaxValidGuess(Action):
    def __init__(self, game_config):
        super().__init__(game_config)
        self.action = max_valid_guess


class MinGuess(Action):
    def __init__(self, game_config):
        super().__init__(game_config)
        self.action = min_guess


class GuessesCombinationGuess(Action):
    def __init__(self, game_config):
        super().__init__(game_config)
        self.action = guesses_combination_guess

    def valid(self, state):
        return len(state) > 1


def generate_actions_func(game_config):
    all_actions = [
        AllDifferentGuess(game_config),
        RandomGuess(game_config),
        MaxGuess(game_config),
        NewGuess(game_config),
        ValidGuess(game_config),
        MaxValidGuess(game_config),
        MinGuess(game_config),
        GuessesCombinationGuess(game_config)
    ]

    def get_actions(state):
        res = list()
        for action in all_actions:
            if action.valid(state):
                res.append(action.action)
        return res

    return get_actions