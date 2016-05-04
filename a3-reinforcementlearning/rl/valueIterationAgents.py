# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        # dict = { 'state' : value, ...}
        self.values = util.Counter()  # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        allStates = self.mdp.getStates()

        # iteration times
        for i in xrange(self.iterations):
            temp = util.Counter()
            for state in allStates:                 # all states in the grid
                if self.mdp.isTerminal(state):      # if terminal, value = 0
                    self.values[state] = 0.0
                else:
                    # each state has several action selections
                    actions = self.mdp.getPossibleActions(state)
                    qValues = []
                    for action in actions:
                        # each action has several possible outcome
                        q = self.computeQValueFromValues(state, action)
                        qValues.append(q)
                    temp[state] = max(qValues)
            self.values = temp


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # transitions -> [(nextState1, prob1), (nextState2, prob2), ... ]
        transitions = self.mdp.getTransitionStatesAndProbs(state, action)
        qValue = 0.0

        # t[0] = nextState, t[1] = prob
        for t in transitions:
            qValue += t[1] * (self.mdp.getReward(state, action, t[0]) +
                              self.discount * self.getValue(t[0]))
        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        qValue = []
        if self.mdp.isTerminal(state):
            return None
        # possible actions for each state
        actions = self.mdp.getPossibleActions(state)
        # for each action, several possible outcomes
        for action in actions:
            qValue.append(self.computeQValueFromValues(state, action))
        bestAction = actions[qValue.index(max(qValue))]
        return bestAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
