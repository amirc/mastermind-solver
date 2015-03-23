import random


class Agent:
    def __init__(self, game_config, get_available_actions, alpha, epsilon, discount, feature_extractor,
                 learned_data=None):
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
