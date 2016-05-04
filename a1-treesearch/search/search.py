# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    """
    ***     pacman layout   :    mediumMaze
    ***     solution length :    130
    ***     nodes expanded  :    146

    """
    # initialization
    startState = problem.getStartState()    # get the start state at beginning
    explored, actions = [], []              # initialization
    pathRecord = [startState, actions]      # path [current state + actions]
    frontier = util.Stack()                 # start frontier initialized with startState
    frontier.push(pathRecord)

    # while frontier is not empty, keep searching
    while frontier.isEmpty() is not True:
        current = frontier.pop()            # pop the current state

        if problem.isGoalState(current[0]) is True:
            return current[1]

        # if current location is not the GOAL
        # choose one direction to go
        if current[0] not in explored:
            explored.append(current[0])                     # explored node
            successors = problem.getSuccessors(current[0])  # currently available
            for successor in successors:
                actionsList = []

                # old actions
                [actionsList.append(actions) for actions in current[1]]
                actionsList.append(successor[1])

                # new actions
                pathRecord = [successor[0], actionsList]
                frontier.push(pathRecord)     

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"

    """
    ***     pacman layout   :    mediumMaze
    ***     solution length :    68
    ***     nodes expanded  :    269
    """
    startState = problem.getStartState()    # get the start state at beginning
    explored, actions = [], []              # initialization
    pathRecord = [startState, actions]      # path [current state + actions]
    frontier = util.Queue()                 # data structure: queue
    frontier.push(pathRecord)
    # push(( , ), actions)

    # while frontier is not empty, keep searching
    while frontier.isEmpty() is not True:
        current = frontier.pop()             # pop the current state

        if problem.isGoalState(current[0]) is True:
            return current[1]

        # if current location is not the GOAL
        # choose one direction to go
        if current[0] not in explored:
            explored.append(current[0])                     # explored node
            successors = problem.getSuccessors(current[0])  # currently available
            for successor in successors:
                actionsList = []

                # old actions
                [actionsList.append(actions) for actions in current[1]]
                actionsList.append(successor[1])

                # new actions
                pathRecord = [successor[0], actionsList]
                frontier.push(pathRecord)

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()        # get the start state at beginning
    explored, actions, costs = [], [], [0]      # initialization
    pathRecord = [startState, actions, costs]   # path [current state + actions + costs]
    frontier = util.PriorityQueue()             # data structure: priority queue
    frontier.push(pathRecord, costs)

    # while frontier is not empty, keep searching
    while frontier.isEmpty() is not True:
        current = frontier.pop()                # pop the current state

        if problem.isGoalState(current[0]) is True:
            return current[1]

        # if current location is not the GOAL
        # choose one direction to go
        if current[0] not in explored:
            explored.append(current[0])                     # explored node
            successors = problem.getSuccessors(current[0])  # currently available

            for successor in successors:
                actionsList = []
                costsList = []

                # old actions
                [actionsList.append(actions) for actions in current[1]]
                [costsList.append(cost) for cost in current[2]]

                # new actions & cost (backward)
                actionsList.append(successor[1])
                costsList.append(successor[2])
                costs = sum(costsList)

                pathRecord = [successor[0], actionsList, costsList]
                frontier.push(pathRecord, costs)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()        # get the start state at beginning
    explored, actions, costs = [], [], [0]      # initialization
    pathRecord = [startState, actions, costs]   # path [current state + actions + costs]
    frontier = util.PriorityQueue()             # data structure: priority queue
    frontier.push(pathRecord, costs)

    # while frontier is not empty, keep searching
    while frontier.isEmpty() is not True:
        current = frontier.pop()            # pop the current state

        if problem.isGoalState(current[0]) is True:
            return current[1]

        # if current location is not the GOAL
        # choose one direction to go
        if current[0] not in explored:
            explored.append(current[0])                     # explored node
            successors = problem.getSuccessors(current[0])  # currently available

            for successor in successors:
                actionsList = []
                costsList = []

                # old actions
                [actionsList.append(actions) for actions in current[1]]
                [costsList.append(cost) for cost in current[2]]

                # new actions & cost
                actionsList.append(successor[1])
                costsList.append(successor[2])
                costs = sum(costsList) + heuristic(successor[0], problem)

                pathRecord = [successor[0], actionsList, costsList]
                frontier.push(pathRecord, costs)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
