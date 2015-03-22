# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

# from game import *
#from learningAgents import ReinforcementAgent
#from featureExtractors import *
from collections import Counter
from Mastermind import Game
import random, math


class QLearningAgent:
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

    def __init__(self, actionFn=None, numTraining=100, epsilon=0.5, alpha=0.5, gamma=1):
        """
    actionFn: Function which takes a state and returns the list of legal actions

    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
        if actionFn == None:
            actionFn = lambda state: state.getLegalActions()
        self.actionFn = actionFn
        self.episodesSoFar = 0
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
        self.numTraining = int(numTraining)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)

    def getQValue(self, state, action):
        """
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
    """
        return self.values[(state, action)]

    def getValue(self, state):
        """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
        bestAct = self.getPolicy(state)

        if not bestAct:
            return 0.0

        else:
            return self.getQValue(state, bestAct)

    def getPolicy(self, state):
        """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
        legalActions = self.getLegalActions(state)
        bestAct = None
        bestVal = -float('inf')

        if legalActions:
            for action in legalActions:

                val = self.getQValue(state, action)

                if val == bestVal:
                    bestAct.append(action)

                elif val > bestVal:
                    bestVal = val
                    bestAct = [action]

            return random.choice(bestAct)

        else:
            return bestAct

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
        legalActions = self.getLegalActions(state)
        action = None

        if legalActions:
            if util.flipCoin(self.epsilon):
                return random.choice(legalActions)

            else:
                return self.getPolicy(state)

        return action

    def update(self, state, action, nextState, reward):
        """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
    """

        self.values[(state, action)] += self.alpha * (
            reward + self.discount * self.getValue(nextState) - self.getQValue(state, action))


class ApproximateQAgent(QLearningAgent):
    """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
    """

    def __init__(self, **args):
        self.featExtractor = util.lookup(extractor, globals())()
        QLearningAgent.__init__(self, **args)
        self.w = Counter()

    def getQValue(self, state, action):
        """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
        res = 0
        f_vals = self.featExtractor.getFeatures(state, action)
        for key in f_vals:
            res += self.w[key] * f_vals[key]

        return res


    def update(self, state, action, nextState, reward):
        """
       Should update your weights based on transition
    """
        correction = (reward + self.discount * self.getValue(nextState)) - self.getQValue(state, action)
        f_vals = self.featExtractor.getFeatures(state, action)
        for key in f_vals:
            self.w[key] += self.alpha * correction * f_vals[key]


    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
