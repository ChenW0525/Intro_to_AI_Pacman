# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"

        # print("newPos: ", newPos)
        # print("newFood: ", newFood)
        # print("newFood list: ", newFood.asList())
        # print("newGhostStates: ", newGhostStates)
        # print("newScaredTimes: ", newScaredTimes)

        min_dis = 999999
        food_list = newFood.asList()
        food_num = len(food_list)
        if food_num == 0:
            min_dis = 0
        for i in range(food_num):
            # eating food matters more than the distance itself.
            food_dis = manhattanDistance(newPos, food_list[i]) + food_num * 100
            if food_dis < min_dis:
                min_dis = food_dis
        score = -min_dis
        for i in range(len(newGhostStates)):
            ghost_pos = successorGameState.getGhostPosition(i + 1)
            if manhattanDistance(newPos, ghost_pos) < 1:
                score = -999999
        # print("newPos: ", newPos)
        # print("min dis: ", min_dis)
        # print("score: ", score)
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


def removeStop(action_list):
    """
    If pacman gets a chance to move, it should never stop, which is a waste of time.
    """
    return [x for x in action_list if x != 'Stop']


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def miniMax(state, iterCount):
            if iterCount >= self.depth * agent_num or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            agent_index = iterCount % agent_num
            if agent_index != 0:  # ghosts turn, the min agent
                result = 9999
                for action in removeStop(state.getLegalActions(agent_index)):
                    child_state = state.generateSuccessor(agent_index, action)
                    result = min(result, miniMax(child_state, iterCount + 1))
                return result
            else:  # pacman turn, the max agent
                result = -9999
                for action in removeStop(state.getLegalActions(agent_index)):
                    child_state = state.generateSuccessor(agent_index, action)
                    result = max(result, miniMax(child_state, iterCount + 1))
                    if iterCount == 0:
                        action_score.append(result)
                return result
        agent_num = gameState.getNumAgents()
        action_score = []
        miniMax(gameState, 0)
        return removeStop(gameState.getLegalActions(0))[action_score.index(max(action_score))]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def alphaBeta(state, iter_count, alpha, beta):
            if iter_count >= self.depth * agent_num or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            agent_index = iter_count % agent_num
            if agent_index != 0:  # ghosts turn, the min agent
                result = 9999
                for action in removeStop(state.getLegalActions(agent_index)):
                    child_state = state.generateSuccessor(agent_index, action)
                    result = min(result, alphaBeta(child_state, iter_count + 1, alpha, beta))
                    beta = min(beta, result)
                    if beta < alpha:
                        break
                return result
            else:  # pacman turn, the max agent
                result = -9999
                for action in removeStop(state.getLegalActions(agent_index)):
                    child_state = state.generateSuccessor(agent_index, action)
                    result = max(result, alphaBeta(child_state, iter_count + 1, alpha, beta))
                    alpha = max(alpha, result)
                    if iter_count == 0:
                        action_score.append(result)
                    if beta < alpha:
                        break
                return result

        agent_num = gameState.getNumAgents()
        action_score = []
        alphaBeta(gameState, 0, -9999, 9999)
        return removeStop(gameState.getLegalActions(0))[action_score.index(max(action_score))]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def expectiMax(state, iter_count):
            if iter_count >= self.depth * agent_num or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            agent_index = iter_count % agent_num
            if agent_index != 0:  # ghosts turn, the min agent
                result = 9999
                successor_score = []
                for action in removeStop(state.getLegalActions(agent_index)):
                    child_state = state.generateSuccessor(agent_index, action)
                    result = expectiMax(child_state, iter_count + 1)
                    successor_score.append(result)
                average_score = sum([float(x) / len(successor_score) for x in successor_score])
                return average_score
            else:  # pacman turn, the max agent
                result = -9999
                for action in removeStop(state.getLegalActions(agent_index)):
                    child_state = state.generateSuccessor(agent_index, action)
                    result = max(result, expectiMax(child_state, iter_count + 1))
                    if iter_count == 0:
                        action_score.append(result)
                return result

        agent_num = gameState.getNumAgents()
        action_score = []
        expectiMax(gameState, 0)
        return removeStop(gameState.getLegalActions(0))[action_score.index(max(action_score))]


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:
    ghost_score returns the score measured by the distance between ghost and pacman.
    If the ghost is not scared, score will be subtracted from the measurement.
    If the ghost is scared, pacman can earn score by eating it. So score will be added from the measurement.

    food_score and capsule_score are similar. Both of them will return the score of food and capsule.
    What is needed to be noticed is that, capsule_weight and food weight measure the preference of the pacman.
    The bigger capsule_weight is, the stronger willing pacman will have to eat the capsule in remove place
    rather than the food nearby.

    """
    "*** YOUR CODE HERE ***"

    def ghost_score(gameState):
        score = 0
        for ghost in gameState.getGhostStates():
            ghost_dis = manhattanDistance(gameState.getPacmanPosition(), ghost.getPosition())
            scared_scope = 7  # means the scope pacman will hunt the scared ghost
            ghost_scope = 6  # means the scope pacman will escape the ghost
            if ghost.scaredTimer > 0:
                score += pow(max(scared_scope - ghost_dis, 0), 2)
            else:
                score -= pow(max(ghost_scope - ghost_dis, 0), 2)
        return score

    def food_score(gameState):
        score = 0
        for food in gameState.getFood().asList():
            food_weight = 1.0
            score = max(score, food_weight / manhattanDistance(gameState.getPacmanPosition(), food))
        return score

    def capsule_score(gameState):
        score = 0
        for cap in gameState.getCapsules():
            capsule_weight = 50.0
            score = max(score, capsule_weight / manhattanDistance(gameState.getPacmanPosition(), cap))
        return score

    current_score = currentGameState.getScore()
    ghosts_score = ghost_score(currentGameState)
    foods_score = food_score(currentGameState)
    capsules_score = capsule_score(currentGameState)
    # print(current_score, ghosts_score, foods_score, capsules_score)
    return current_score + ghosts_score + foods_score + capsules_score


# Abbreviation
better = betterEvaluationFunction
