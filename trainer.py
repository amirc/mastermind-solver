from collections import Counter
from copy import copy
from pprint import pprint
import statistics
from sys import argv
from Mastermind import Game
from actions import generate_actions_func
from agent import Agent
from extractors import simple_extract
from game_config import GameConfig


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
                    reward = max([0.5, reward_max - game.num_guess])*100
                else:
                    reward = 0

                next_state = copy(game.get_state())

                self._agent.update(cur_state, action, next_state, reward)

            scores.append(game.num_guess)
        return scores, over_max_games

    def get_learn_data(self):
        return self._agent.weights


if __name__ == '__main__':
    _slots = int(argv[1])
    _options = int(argv[2])
    _alpha = float(argv[3])
    _epsilon = float(argv[4])
    _gamma = float(argv[5])
    _practice_games = 10000
    _games = 1000
    if len(argv) > 6):
        _practice_games = argv[6]
        if _pratice_games < 1000 and _pratice_games:
            print("pratice games must be above 1000 or 0")
            return

    if len(argv) > 7):
        _games = argv[7]

    game_conf = GameConfig(_slots, _options)
    training = Trainer(game_conf, simple_extract, _alpha, _epsilon, _gamma, generate_actions_func(game_conf))
    for i in range(_practice_games//1000):
        print("After ", i * 1000, " games")
        scores, fails = training.train(1000, 20)
        print("Mean: ", statistics.mean(scores))
        print("Variance: ", statistics.variance(scores))
        print("failed in ", fails)
    pprint(training.get_learn_data())

    winning = Trainer(game_conf, simple_extract, 0, 0, 0, generate_actions_func(game_conf), training.get_learn_data())
    actions_counter = Counter()
    scores, fails = winning.train(_games, 20, actions_counter)
    print("Mean: ", statistics.mean(scores))
    print("Variance: ", statistics.variance(scores))
    print("failed in ", fails)
    pprint(actions_counter)
