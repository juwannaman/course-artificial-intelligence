# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

from util import manhattanDistance
from game import Directions
import numpy as np
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # pacman position
        currentPos = currentGameState.getPacmanPosition()
        newPos = successorGameState.getPacmanPosition()

        # food position
        # newFood = zip(*list(successorGameState.getFood()))
       	newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        numOfGhost = successorGameState.getNumAgents()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # distance to food
        newFoodPos = zip(*np.where(newFood))
        newDistToFood = [(manhattanDistance(newPos, food), food) for food in newFoodPos]
        if len(newDistToFood) != 0: 
        	newNearestFood, nearestIndex = min(newDistToFood)
        else:
        	newNearestFood = 0
        	nearestIndex = successorGameState.getPacmanPosition()

        # currentDistToFood = sum([(manhattanDistance(currentPos, food) for food in currentGameState])

        # ghost distance to that food
        ghostToFood = 0
        for ghost in newGhostStates:
        	ghostToFood += manhattanDistance(ghost.getPosition(), nearestIndex)

        "*** YOUR CODE HERE ***"
        score = 0
        # if next step is winning
        if successorGameState.isWin(): score += 9999
        if successorGameState.isLose(): score -= 9999

        # dist to nearest and ghost dist to nearest
        if newNearestFood < ghostToFood : score += 500

        # if next step is food
        if currentGameState.hasFood(newPos[0], newPos[1]): score += 800 #500

        # if next step is capsule
        if newPos in currentGameState.getCapsules(): score += 9999

        # num of food
        numOfFood = successorGameState.getNumFood()

        # distance to ghost
        i = 0
        for ghost in newGhostStates:
            if manhattanDistance(newPos, ghost.getPosition()) < 2:
                # cannot eat ghost
                if(newScaredTimes[i] == 0):
                    score -= 1000 #1000
                else:
                    score += 100
            else:
                if (newScaredTimes[i] == 1):
                    score += manhattanDistance(newPos, ghost.getPosition())*50
                else:
                    score -= manhattanDistance(newPos, ghost.getPosition())*30
            i += 1
        

        return score
		

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    agent = 0
    adversarial = 1

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        depth = 0
        action, value = self.maxValue(gameState, depth)
        return action

    def maxValue(self, gameState, depth):
        nextAction = None
        # terminal-test
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return (nextAction, self.evaluationFunction(gameState))
            
        # negative infinity
        vmax = -99999

        # for each a in actions
        for a in gameState.getLegalActions(self.agent):
        	# get next state
            nextState = gameState.generateSuccessor(self.agent, a)
            # minValue of next state
            act, value = self.minValue(nextState, depth, self.adversarial)
            (nextAction, vmax) = max((a, value), (nextAction, vmax), key=lambda x: x[1])

        return (nextAction, vmax)

    def minValue(self, gameState, depth, currentAgent):
        nextAction = None
        lastGhost = gameState.getNumAgents() - 1  # ghost number 
        # terminal-state
        if gameState.isWin() or gameState.isLose():
            return (nextAction, self.evaluationFunction(gameState))

        # positive infinity
        vmin = 99999

        # for each a in actions
        for a in gameState.getLegalActions(currentAgent):
            # get next state
            nextState = gameState.generateSuccessor(currentAgent, a)

            # if it is the last Ghost in the tree
            # if True , layer + 1, go into the Maximizer or return terminal
            # if False, go to the next Minimizer (next ghost)
            if currentAgent == lastGhost: 
                act, value = self.maxValue(nextState, depth + 1)
            else:
                act, value = self.minValue(nextState, depth, currentAgent + 1)
            (nextAction, vmin) = min((a, value), (nextAction, vmin), key=lambda x: x[1])

        return (nextAction, vmin)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    agent = 0
    adversarial = 1

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        depth = 0
        alpha = -999999
        beta = 999999
        action, value = self.maxValue(gameState, depth, alpha, beta)
        return action

    def maxValue(self, gameState, depth, alpha, beta):
        nextAction = None
        # terminal-test
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return (nextAction, self.evaluationFunction(gameState))
            
        # negative infinity
        vmax = -99999

        # for each a in actions
        for a in gameState.getLegalActions(self.agent):
        	# get next state
            nextState = gameState.generateSuccessor(self.agent, a)
            # minValue of next state
            act, value = self.minValue(nextState, depth, self.adversarial, alpha, beta)
            (nextAction, vmax) = max((a, value), (nextAction, vmax), key=lambda x: x[1])
            if vmax > beta: return (nextAction, vmax)
            alpha = max(alpha, vmax)
        return (nextAction, vmax)

    def minValue(self, gameState, depth, currentAgent, alpha, beta):
        nextAction = None
        lastGhost = gameState.getNumAgents() - 1  # ghost number 
        # terminal-state
        if gameState.isWin() or gameState.isLose():
            return (nextAction, self.evaluationFunction(gameState))

        # positive infinity
        vmin = 99999

        # for each a in actions
        for a in gameState.getLegalActions(currentAgent):
            # get next state
            nextState = gameState.generateSuccessor(currentAgent, a)

            # if it is the last Ghost in the tree
            # if True , layer + 1, go into the Maximizer or return terminal
            # if False, go to the next Minimizer (next ghost)
            if currentAgent == lastGhost: 
                act, value = self.maxValue(nextState, depth + 1, alpha, beta)
            else:
                act, value = self.minValue(nextState, depth, currentAgent + 1, alpha, beta)
            (nextAction, vmin) = min((a, value), (nextAction, vmin), key=lambda x: x[1])
            if vmin < alpha: return (nextAction, vmin)
            beta = min(beta, vmin)
        return (nextAction, vmin)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    agent = 0
    adversarial = 1

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        depth = 0
        action, value = self.maxValue(gameState, depth)
        return action


    def maxValue(self, gameState, depth):
        nextAction = None
        # terminal-test
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return (nextAction, self.evaluationFunction(gameState))
            
        # negative infinity
        vmax = -99999

        # for each a in actions
        for a in gameState.getLegalActions(self.agent):
        	# get next state
            nextState = gameState.generateSuccessor(self.agent, a)
            # minValue of next state
            act, value = self.expectValue(nextState, depth, self.adversarial)
            (nextAction, vmax) = max((a, value), (nextAction, vmax), key=lambda x: x[1])
        return (nextAction, vmax)

    def expectValue(self, gameState, depth, currentAgent):
        nextAction = None
        lastGhost = gameState.getNumAgents() - 1  # ghost number 
        # terminal-state
        if gameState.isWin() or gameState.isLose():
            return (nextAction, self.evaluationFunction(gameState))

        # positive infinity
        vmin = 99999
        numOfActions = len(gameState.getLegalActions(currentAgent))
        sumOfValue = 0

        # for each a in actions
        for a in gameState.getLegalActions(currentAgent):
            # get next state
            nextState = gameState.generateSuccessor(currentAgent, a)

            # if it is the last Ghost in the tree
            # if True , layer + 1, go into the Maximizer or return terminal
            # if False, go to the next Minimizer (next ghost)
            if currentAgent == lastGhost: 
                act, value = self.maxValue(nextState, depth + 1)
            else:
                act, value = self.expectValue(nextState, depth, currentAgent + 1)
            sumOfValue += value
        return (nextAction, sumOfValue/numOfActions)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()

    # is terminated?
    if currentGameState.isWin(): score += 99999
    if currentGameState.isLose(): score -= 99999

    # to food
    newFood = currentGameState.getFood()
    foodPos = newFood.asList()
    foodDist = [(manhattanDistance(food, currentGameState.getPacmanPosition()), food) for food in foodPos]
    if len(foodDist) > 0:
    	nearestFood, index = min(foodDist)
    else: 
    	nearestFood = 0
    	index = currentGameState.getPacmanPosition()

    # to ghost
    numOfGhost = currentGameState.getNumAgents() - 1
    distToGhost = []
    for i in range(1, numOfGhost + 1):
    	distToGhost.append(manhattanDistance(currentGameState.getPacmanPosition(), currentGameState.getGhostPosition(i)))
    nearestGhost = min(distToGhost)

    # ghost to food 
    ghostToFood = []
    for i in range(1, numOfGhost + 1):
    	ghostToFood.append(manhattanDistance(index, currentGameState.getGhostPosition(i)))
    nearestGToFood = min(ghostToFood)


    numOfFood = len(foodPos)
    numOfCapsule = len(currentGameState.getCapsules())


    if (nearestFood < nearestGToFood): score += 800
    if (nearestGhost < 3): score -= 200
    if (nearestFood < nearestGhost): score += 500
    score -= 5*numOfFood
    score -= 100*numOfCapsule

    return score

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

