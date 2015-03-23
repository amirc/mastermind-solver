from collections import Counter
from copy import copy
from pprint import pprint
import random
import statistics
from sys import argv
from CSP import CSP
from Mastermind import Game


class Agent:
    def __init__(self, game_config, get_available_actions, alpha, epsilon, discount, feature_extractor, learned_data=None):
        self._feature_extractor = feature_extractor
        self._alpha = alpha
        self._epsilon = epsilon
        self._get_actions = get_available_actions
        self._game_config = game_config
        self._discount = discount
        self._weights = learned_data or dict()

    def generate_action(self, state):
        if random.random() < self._epsilon:
            return random.choice(self._get_actions(state))
        else:
            return self.get_policy(state)

    def get_policy(self, state):
        best_act = []
        best_val = -float('inf')

        for action in self._get_actions(state):

            val = self._get_qvalue(state, action)

            if val == best_val:
                best_act.append(action)

            elif val > best_val:
                best_val = val
                best_act = [action]

        return random.choice(best_act)

    def _get_qvalue(self, state, action):
        res = 0
        f_vals = self._feature_extractor(self._game_config, state, action)
        for key in f_vals:
            if key in self._weights:
                res += self._weights[key] * f_vals[key]

        return res

    def get_value(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        best_act = self.get_policy(state)
        return self._get_qvalue(state, best_act)

    def update(self, state, action, next_state, reward):
        """
            Should update your weights based on transition
        """
        correction = (reward + self._discount * self.get_value(next_state)) - self._get_qvalue(state, action)
        f_vals = self._feature_extractor(self._game_config, state, action)
        for key in f_vals:
            if key not in self._weights:
                self._weights[key] = 0
            self._weights[key] += self._alpha * correction * f_vals[key]

    @property
    def weights(self):
        return self._weights


class GameConfig:
    def __init__(self, slots, options):
        self._options = options
        self._slots = slots

    @property
    def options(self):
        return self._options

    @property
    def slots(self):
        return self._slots


class Trainer:
    def __init__(self, game_config, feature_extractor, alpha, epsilon, gamma, actions, learned_data=None):
        self._game_config = game_config
        self._agent = Agent(self._game_config, actions, alpha, epsilon, gamma, feature_extractor, learned_data)

    def train(self, num_of_games, max_tries, action_counter=None):
        scores = []
        reward_max = (self._game_config.slots + self._game_config.slots) / 2
        over_max_games = 0
        for i in range(num_of_games):
            game = Game(self._game_config.slots, self._game_config.options)
            try_i = 0
            while not game.is_won():
                try_i += 1
                if try_i > max_tries:
                    over_max_games += 1
                    break
                cur_state = copy(game.get_state())
                action = self._agent.generate_action(cur_state)

                if action_counter is not None:
                    action_counter.update([action.__name__])

                game.check_guess(action(self._game_config, game.guesses))

                # TODO: play with reward
                if game.is_won():
                    reward = reward_max - game.num_guess
                else:
                    reward = 0

                next_state = copy(game.get_state())

                self._agent.update(cur_state, action, next_state, reward)

            scores.append(game.num_guess)
        return scores, over_max_games

    def get_learn_data(self):
        return self._agent.weights


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


all_diff_counter = 0


def all_different_guess(game_config, state):
    all_diff_counter += 1
    numbers = list(range(game_config.options))
    res = list()
    for i in range(game_config.slots):
        tmp = random.choice(numbers)
        res.append(tmp)
        numbers.remove(tmp)

    return res


def max_valid_guess(game_config, state):
    csp = CSP(game_config.slots, game_config.options)
    for guess, bulls, cows in state:
        csp.insert_guess(guess, bulls, cows)

    return csp.generate_guess()


def valid_guess(game_config, state):
    csp = CSP(game_config.slots, game_config.options)
    for guess, bulls, cows in state:
        csp.insert_guess(guess, bulls, cows)

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


def get_actions(state):
    default = [
        all_different_guess,
        random_guess,
        #max_guess,
        new_guess,
        valid_guess,
        #max_valid_guess,
        #min_guess
    ]
    if len(state) > 1:
        default += [guesses_combination_guess]
    return default


def simple_extract(game_config, state, action):
    csp = CSP(game_config.slots, game_config.options)
    for guess, bulls, cows in state:
        csp.insert_guess(guess, bulls, cows)

    def positive_normalize(val, steps):
        return min(val, steps) / steps

    res = dict()

    # var on slots domain len
    # var_domain = statistics.variance([len(domain) for domain in csp._domains])

    # mean on slots domain len
    mean_domain = statistics.mean([len(domain) for domain in csp._domains])

    # mean on how many different vals in bull counter
    mean_bulls = statistics.mean([len(set(bull_slot.values())) for bull_slot in csp._bull_count])

    # var on how many different vals in bull counter
    var_bulls = statistics.variance([len(set(bull_slot.values())) for bull_slot in csp._bull_count])

    # mean on how many different vals in cow counter
    mean_cows = statistics.mean([len(set(cow_slot.values())) for cow_slot in csp._cow_count])

    # mean on how many different vals in cow counter
    var_cows = statistics.variance([len(set(cow_slot.values())) for cow_slot in csp._cow_count])

    guessed_times = Counter()
    for guess, bulls, cows in state:
        guessed_times.subtract(guess)

    unused_keys = len(set(range(game_config.options)).difference(set(guessed_times)))

    res[(action.__name__, 'unused_keys')] = positive_normalize(unused_keys, game_config.options)

    res[(action.__name__, 'mean_domain')] = positive_normalize(mean_domain, game_config.slots)
    res[(action.__name__, 'mean_bulls')] = positive_normalize(mean_bulls, game_config.options)
    res[(action.__name__, 'var_bulls')] = positive_normalize(var_bulls, game_config.options)
    res[(action.__name__, 'mean_cows')] = positive_normalize(mean_cows, game_config.options)
    res[(action.__name__, 'var_cows')] = positive_normalize(var_cows, game_config.options)
    if state:
        res[(action.__name__, 'bulls_last_turn')] = positive_normalize(state[-1][1], game_config.options)
        res[(action.__name__, 'cows_last_turn')] = positive_normalize(state[-1][2], game_config.options)

    res[(action.__name__, 'bias')] = 1

    return res

if __name__ == '__main__':
    _slots = int(argv[1])
    _options = int(argv[2])
    _alpha = float(argv[3])
    _epsilon = float(argv[4])
    _gamma = float(argv[5])
    game_conf = GameConfig(_slots, _options)
    training = Trainer(game_conf, simple_extract, _alpha, _epsilon, _gamma, get_actions)
    for i in range(20):
        print("After ", i * 1000, " games")
        scores, fails = training.train(1000, 20)
        print("Mean: ", statistics.mean(scores))
        print("Variance: ", statistics.variance(scores))
        print("failed in ", fails)
    pprint(training.get_learn_data())

    winning = Trainer(game_conf, simple_extract, 0, 0, 0, get_actions, training.get_learn_data())
    actions_counter = Counter()
    scores, fails = winning.train(2000, 20, actions_counter)
    print("Mean: ", statistics.mean(scores))
    print("Variance: ", statistics.variance(scores))
    print("failed in ", fails)
    pprint(actions_counter)