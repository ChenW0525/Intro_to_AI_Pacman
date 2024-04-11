# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import searchAgents


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    fringe = util.Stack()
    closed = []
    fringe.push((problem.getStartState(), []))
    while fringe:
        if fringe.isEmpty():
            return False
        node, actions = fringe.pop()
        if problem.isGoalState(node):
            return actions
        if node not in closed:
            closed.append(node)
            children = problem.getSuccessors(node)
            for child, action, _ in children:
                if child not in closed:
                    fringe.push((child, actions + [action]))
    return []

    # # first attempt code
    # fringe = util.Stack()
    # path = util.Stack()
    # closed = set()
    # actions = []
    # fringe.push(problem.getStartState())
    # childrenDic = {}  # to avoid re-expanding nodes
    # while fringe:
    #     if fringe.isEmpty():
    #         return False
    #     node = fringe.pop()
    #     path.push(node)
    #     closed.add(node)
    #     if problem.isGoalState(node):
    #         return actions
    #     while True:
    #         if childrenDic.get(node):
    #             children = childrenDic.get(node)
    #         else:
    #             children = problem.getSuccessors(node)
    #             childrenDic.setdefault(node, children)
    #         count = 0
    #         for child in children:
    #             if child[0] in closed:
    #                 count += 1
    #         if count == len(children) or children == []:
    #             path.pop()
    #             node = path.pop()
    #             path.push(node)
    #             actions.pop()
    #             continue
    #         for child in children:
    #             if child[0] not in closed:
    #                 fringe.push(child[0])
    #                 actions.append(child[1])
    #                 break
    #         break
    # return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    fringe = util.Queue()
    closed = []
    fringe.push((problem.getStartState(), []))
    while fringe:
        if fringe.isEmpty():
            return False
        node, actions = fringe.pop()
        if problem.isGoalState(node):
            return actions
        if node not in closed:
            closed.append(node)
            children = problem.getSuccessors(node)
            for child, action, _ in children:
                fringe.push((child, actions + [action]))

        # # part of first attempt code:
        # if childrenDic.get(node):
        #     children = childrenDic.get(node)
        # else:
        #     children = problem.getSuccessors(node)
        #     childrenDic.setdefault(node, children)
        # for child in children:
        #     if child[0] not in closed:
        #         closed.add(child[0])
        #         fringe.push(child[0])
        #         if not actionDic.get(node):
        #             actionDic[child[0]] = [child[1]]
        #         else:
        #             temAction = actionDic[node].copy()
        #             temAction.append(child[1])
        #             actionDic.setdefault(child[0], temAction)
    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    fringe = util.PriorityQueue()
    closed = []
    # each item is consisted by node, path, and cost. Priority is the same to cost.
    fringe.push((problem.getStartState(), [], 0), 0)
    while not fringe.isEmpty():
        if fringe.isEmpty():
            return False
        node, actions, cost = fringe.pop()
        if node in closed:
            continue
        closed.append(node)
        if problem.isGoalState(node):
            return actions
        children = problem.getSuccessors(node)
        for child in children:
            cNode, cAction, cCost = child
            totalCost = cost + cCost
            fringe.push((cNode, actions + [cAction], totalCost), totalCost)
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    fringe = util.PriorityQueue()
    closed = []
    start = problem.getStartState()
    h = heuristic(start, problem)
    fringe.push((start, [], 0), h)  # Priority is cost + heuristic.
    while not fringe.isEmpty():
        if fringe.isEmpty():
            return False
        node, actions, cost = fringe.pop()
        if node in closed:
            continue
        closed.append(node)
        if problem.isGoalState(node):
            return actions
        children = problem.getSuccessors(node)
        for child in children:
            cNode, cAction, cCost = child
            h = heuristic(cNode, problem)
            totalCost = cost + cCost
            fringe.push((cNode, actions + [cAction], totalCost), totalCost + h)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
