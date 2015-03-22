from collections import Counter
from copy import copy
from pprint import pprint
import random
import statistics
from CSP import CSP
from Mastermind import Game


class Agent:
    """
    Q-Learning Agent

    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update

    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discount (discount rate)

    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions
        for a state
    """
  def __init__(self, actions=get_actions() ,alpha=1.0, epsilon=0.05, gamma=0.8, numTraining = 10):
    "You can initialize Q-values here..."
    self.actions = get_actions()
    self.alpha = float(alpha)
    self.epsilon = float(epsilon)
    self.discount = float(gamma)
    self.numTraining = int(numTraining)
    self.values = util.Counter()

  def getQValue(self, state, action):
    """
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
    """
    return self.values[(wrap(state), action)]


  def getValue(self, state):
    """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
    bestAct = self.getPolicy(wrap(state))
    return self.getQValue(wrap(state), bestAct)

  def getPolicy(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    bestAct = []
    bestVal = -float('inf')

    for action in self.actions:

    val = self.getQValue(wrap(state), action)

    if val == bestVal:
        bestAct.append(action)

    elif val > bestVal:
        bestVal = val
        bestAct = [action]

    return random.choice(bestAct)

  def getAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.

      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """
    # Pick Action
    if util.flipCoin(self.epsilon):
        return random.choice(self.actions)

    else:
        return self.getPolicy(state)

  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
    """
    
    self.values[(wrap(state), action)] += self.alpha * (reward + self.discount * self.getValue(wrap(nextState)) - self.getQValue(wrap(state), action))
    
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

                if action_counter:
                    action_counter.update([action.__name__])

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


def wrap(game_config, state, action):

    csp = CSP(game_config.slots, game_config.options)
    for guess, bulls, cows in state:
        csp.insert_guess(guess, bulls, cows)

    threshold = 2 / game_config.options

    domains = []
    bulls = []
    cows = []
    
    for i in range(game_config.slots):
        domains.append(len(csp._domains[i]))
        bulls.append(len(set(csp._bull_count[i].values())))
        cows.append(len(set(csp._cow_count[i].values())))

    return [Counter(domains), Counter(bulls), Counter(cows)]

game_conf = GameConfig(4, 6)
training = Trainer(game_conf, simple_extract, 0.4, 0.5, 0.9, get_actions())
scores, fails = training.train(10000, 100)
print("Mean: ", statistics.mean(scores))
print("Variance: ", statistics.variance(scores))
print("failed in ", fails)
pprint(training.get_learn_data())

winning = Trainer(game_conf, simple_extract, 0, 0, 0, get_actions(), training.get_learn_data())
actions_counter = Counter()
scores, fails = winning.train(1000, 100, actions_counter)
print("Mean: ", statistics.mean(scores))
print("Variance: ", statistics.variance(scores))
print("failed in ", fails)
pprint(actions_counter)