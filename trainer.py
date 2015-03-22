from collections import Counter
from copy import copy
from pprint import pprint
import random
import statistics
from CSP import CSP
from Mastermind import Game


class Agent:
    def __init__(self, game_config, actions, alpha, epsilon, discount, feature_extractor, learned_data=None):
        self._feature_extractor = feature_extractor
        self._alpha = alpha
        self._epsilon = epsilon
        self._actions = actions
        self._game_config = game_config
        self._discount = discount
        self._weights = learned_data or dict()

    def generate_guess(self, state):
        if random.random() < self._epsilon:
            return random.choice(self._actions)
        else:
            return self.get_policy(state)

    def get_policy(self, state):
        best_act = []
        best_val = -float('inf')

        for action in self._actions:

            val = self._get_qvalue(state, action)

            if val == best_val:
                best_act.append(action)

            elif val > best_val:
                best_val = val
                best_act = [action]

        if not best_act:
            print('wtf?')
            print('best_val', best_val)
            print('best_act', best_act)
            print('action1-score', self._get_qvalue(state, self._actions[0]))
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

    def train(self, num_of_games, max_tries):
        scores = []
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
                action = self._agent.generate_guess(cur_state)

                game.check_guess(action(self._game_config, game.guesses))

                # TODO: play with reward
                if game.is_won():
                    reward = 1 / game.num_guess
                else:
                    reward = 0  # - 1 / game.num_guess

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
    """
    guessed_times = Counter()
    for guess, bulls, cows in state:
        guessed_times.update(guess)

    guessed = [num for num in guessed_times.keys()]

    num_remaining = game_config.options - len(guessed)

    to_add = [num[0] for num in guessed_times.most_common(num_remaining)]

    total = to_add + []


    """
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


def max_valid_guess(game_config, state):
    csp = CSP(game_config.slots, game_config.options)
    for guess, bulls, cows in state:
        csp.insert_guess(guess, bulls, cows)

    return csp.generate_guess()


def get_actions():
    return [
        random_guess,
        max_guess,
        new_guess,
        max_valid_guess,
        min_guess
    ]


def simple_extract(game_config, state, action):
    csp = CSP(game_config.slots, game_config.options)
    for guess, bulls, cows in state:
        csp.insert_guess(guess, bulls, cows)

    res = dict()
    if state:
        res[(action.__name__, 'turn')] = 1 / (len(state) + 1)
    else:
        res[(action.__name__, 'turn')] = 1

    # mean on slots domain len
    # mean on how many different vals in bull counter
    # mean on how many different vals in cow counter
    mean_domain = 0
    mean_bulls = 0
    mean_cows = 0
    for i in range(game_config.slots):
        mean_domain += len(csp._domains[i])
        mean_bulls += len(set(csp._bull_count[i].values()))
        mean_cows += len(set(csp._cow_count[i].values()))

    mean_domain /= game_config.slots
    mean_bulls /= game_config.slots
    mean_cows /= game_config.slots

    res[(action.__name__, 'mean_domain')] = 1 / (mean_domain + 1)
    if mean_bulls != 0:
        res[(action.__name__, 'mean_bulls')] = 1 / (mean_bulls + 1)
    else:
        res[(action.__name__, 'mean_bulls')] = 1

    if mean_cows != 0:
        res[(action.__name__, 'mean_cows')] = 1 / (mean_cows + 1)

    else:
        res[(action.__name__, 'mean_cows')] = 1

    return res

game_conf = GameConfig(4, 6)
training = Trainer(game_conf, simple_extract, 0.4, 0.5, 0.9, get_actions())
scores, fails = training.train(10000, 100)
print("Mean: ", statistics.mean(scores))
print("Variance: ", statistics.variance(scores))
print("failed in ", fails)
pprint(training.get_learn_data())

winning = Trainer(game_conf, simple_extract, 0, 0, 0, get_actions(), training.get_learn_data())
scores, fails = winning.train(1000, 100)
print("Mean: ", statistics.mean(scores))
print("Variance: ", statistics.variance(scores))
print("failed in ", fails)