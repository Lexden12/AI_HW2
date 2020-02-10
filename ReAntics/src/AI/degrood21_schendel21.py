from AIPlayerUtils import *
from GameState import *
from Move import Move
from Ant import UNIT_STATS
from Construction import CONSTR_STATS
from Constants import *
from Player import *
import random
import sys
sys.path.append("..")  # so other modules can be found in parent dir


##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    #   cpy           - whether the player is a copy (when playing itself)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer, self).__init__(inputPlayerId, "Search")

    ##
    #getPlacement
    #
    #Description: called during setup phase for each Construction that
    #   must be placed by the player.  These items are: 1 Anthill on
    #   the player's side; 1 tunnel on player's side; 9 grass on the
    #   player's side; and 2 food on the enemy's side.
    #
    #Parameters:
    #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    #Return: The coordinates of where the construction is to be placed
    ##
    def getPlacement(self, currentState):
        numToPlace = 0
        #implemented by students to return their next move
        if currentState.phase == SETUP_PHASE_1:  # stuff on my side
            numToPlace = 11
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on your side of the board
                    y = random.randint(0, 3)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        elif currentState.phase == SETUP_PHASE_2:  # stuff on foe's side
            numToPlace = 2
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on enemy side of the board
                    y = random.randint(6, 9)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        else:
            return [(0, 0)]

    ##
    #getMove
    #Description: Gets the next move from the Player.
    #
    #Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    #Return: The Move to be made
    ##
    def getMove(self, currentState):
        frontierNodes = []
        expandedNodes = []
        steps = self.heuristicStepsToGoal(currentState)
        root = Node(None, currentState, 0, 0, None)
        frontierNodes.append(root)

        for x in range(3):
          frontierNodes.sort(key=self.sortAttr)
          leastNode = root
          leastNode = self.bestMove(frontierNodes)
          # for node in frontierNodes:
          #   if node.steps < leastNode.steps:
          #     leastNode = node
          frontierNodes.remove(leastNode)
          if len(frontierNodes) >= 50:
            frontierNodes = frontierNodes[:50]
          frontierNodes.extend(self.expandNode(leastNode))
          root = frontierNodes[0]

        while not leastNode.depth == 1:
          leastNode = leastNode.parent
        return leastNode.move

        # leastNode = None
        # leastScore = 0
        # oldLeast = 0
        # count = 0
        # while True:
        #   frontierNodes.sort(key=self.sortAttr)
        #   leastNode = self.bestMove(frontierNodes)
        #   oldLeast = leastScore
        #   leastScore = leastNode.steps
        #   if oldLeast == leastScore or oldLeast < leastScore:
        #     count += 1
        #   else:
        #     count = 0
        #   #print(leastScore)
        #   if leastScore == 0 or count == 5:
        #     break
        #   frontierNodes.remove(leastNode)
        #   expandedNodes.append(leastNode)
        #   # if len(frontierNodes) >= 50:
        #   #   frontierNodes = frontierNodes[:50]
        #   frontierNodes.extend(self.expandNode(leastNode))
        # while not leastNode.depth == 1:
        #   #print(leastNode)
        #   leastNode = leastNode.parent
        # return leastNode.move

    ##
    #bestMove
    #Description: Gets the best move from the list of possible moves
    #
    #Parameters:
    #   nodes - List of nodes which contain the possible moves from this location and their rank
    #           Used to find the best move
    #
    #Return: Best node from the evalutaion in each node
    ##
    def bestMove(self, nodes):
      # bestEval = nodes[0].steps
      # bestNode = nodes[0]
      # for node in nodes:
      #   if node.steps < bestEval:
      #     bestEval = node.steps
      #     bestNode = node
      return nodes[0]

    def expandNode(self, node):
      moves = listAllLegalMoves(node.state)
      nodes = []
      for move in moves:
        nextState = getNextState(node.state, move)
        steps = self.heuristicStepsToGoal(nextState)
        newDepth = node.depth + 1
        newNode = Node(move, nextState, newDepth, steps, node)
        nodes.append(newNode)
      return nodes

    ##
    #getAttack
    #Description: Gets the attack to be made from the Player
    #
    #Parameters:
    #   currentState - A clone of the current state (GameState)
    #   attackingAnt - The ant currently making the attack (Ant)
    #   enemyLocation - The Locations of the Enemies that can be attacked (Location[])
    ##

    def getAttack(self, currentState, attackingAnt, enemyLocations):
        #Attack a random enemy.
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]

    ##
    #registerWin
    #
    # This agent doens't learn
    #
    def registerWin(self, hasWon):
        #method templaste, not implemented
        pass

    def sortAttr(self, node):
      return node.steps

    ##
    #heuristicStepsToGoal
    #Description: Gets the number of moves to get to a winning state from the current state
    #
    #Parameters:
    #   currentState - A clone of the current state (GameState)
    #                 This will assumed to be a fast clone of the state
    #                 i.e. the board will not be needed/used
    ##
    def heuristicStepsToGoal(self, currentState):
      myState = currentState.fastclone()
      me = myState.whoseTurn
      enemy = abs(me - 1)
      myInv = getCurrPlayerInventory(myState)
      myFood = myInv.foodCount
      enemyInv = getEnemyInv(self, myState)
      tunnels = getConstrList(myState, types=(TUNNEL,))
      myTunnel = tunnels[1] if (tunnels[0].coords[1] > 5) else tunnels[0]
      enemyTunnel = tunnels[0] if (myTunnel is tunnels[1]) else tunnels[1]
      hills = getConstrList(myState, types=(ANTHILL,))
      myHill = hills[1] if (hills[0].coords[1] > 5) else hills[0]
      enemyHill = hills[1] if (myHill is hills[0]) else hills[0]
      enemyQueen = enemyInv.getQueen()

      foods = getConstrList(myState, None, (FOOD,))

      myWorkers = getAntList(myState, me, (WORKER,))
      myOffense = getAntList(myState, me, (SOLDIER,))
      enemyWorkers = getAntList(myState, enemy, (WORKER,))

      occupyWin = 0

      if len(myOffense) < 1:
        occupyWin += 20
      elif len(myOffense) <= 2:
        occupyWin += 30

      if myFood < 1:
        occupyWin += 20

      if len(myWorkers) < 1:
        occupyWin += 100
      if len(myWorkers) > 1:
        occupyWin += 100

      if enemyQueen == None:
        occupyWin -= 1000

      dist = 100
      for ant in myOffense:
        if len(enemyWorkers) == 0:
          if not enemyQueen == None:
            dist = stepsToReach(myState, ant.coords, enemyHill.coords)
        else:
          dist = stepsToReach(myState, ant.coords, enemyWorkers[0].coords)
          if len(enemyWorkers) > 1 or dist > 1:
            dist += 10

      occupyWin += (dist) + (enemyHill.captureHealth)

      foodWin = occupyWin
      if not len(myOffense) > 0:
        foodNeeded = 11 - myFood
        for w in myWorkers:
          distanceToTunnel = stepsToReach(myState, w.coords, myTunnel.coords)
          distanceToHill = stepsToReach(myState, w.coords, myHill.coords)
          distanceToFood = 9999
          for food in foods:
            if stepsToReach(myState, w.coords, food.coords) < distanceToFood:
              distanceToFood = stepsToReach(myState, w.coords, food.coords)
          if w.carrying:
            #if min(distanceToHill, distanceToTunnel) > 1:
            foodWin += min(distanceToHill, distanceToTunnel) - 9.5
            if w.coords == myHill.coords or w.coords == myTunnel.coords:
              foodWin += 1.5
            if not len(myOffense) == 0:
              foodWin -= 1
          else:
            #if distanceToFood >= 0:
            if w.coords == foods[0].coords or w.coords == foods[1].coords:
              foodWin += 1.2
              break
            foodWin += distanceToFood/3 - 1.5
            if not len(myOffense) == 0:
              foodWin -= 1
        occupyWin += foodWin * (foodNeeded)

      # if myFood > 1:
      #   occupyWin -= 4

      # food_time = 30
      # isTunnel = False
      # for w in myWorkers:
      #   if w.carrying:
      #     #We must check every worker and the distance between the anthill and the tunnel.
      #     #in order to decide which one is quicker to go to.
      #     distanceToTunnel = stepsToReach(myState, w.coords, myTunnel.coords)
      #     distanceToHill = stepsToReach(myState, w.coords, myHill.coords)
      #     isTunnel = True if distanceToTunnel < distanceToHill else False
      #     min_dist = min(distanceToTunnel, distanceToHill)
      #     food_time = min_dist

      #   #Otherwise, we want to move toward the food
      #   else:
      #     distanceToFood = []
      #     for f in foods:
      #       distanceToFood.append(stepsToReach(myState, w.coords, f.coords))
      #     min_food = 1000
      #     idx = 0
      #     for i in range(len(distanceToFood)):
      #       if distanceToFood[i] < min_food:
      #         min_food = distanceToFood[i]
      #         idx = i
      #     distanceToTunnel = stepsToReach(
      #         myState, foods[idx].coords, myTunnel.coords)
      #     distanceToHill = stepsToReach(
      #         myState, foods[idx].coords, myHill.coords)
      #     min_dist = min(distanceToTunnel, distanceToHill) + min_food
      #     food_time = min_dist

      # food_time2 = 0
      # times = []
      # if len(myWorkers) > 0:
      #   for food in foods:
      #     if myWorkers[0].carrying:
      #       times.append(stepsToReach(myState, food.coords,
      #                                 myTunnel.coords if isTunnel else myHill.coords))
      #     else:
      #       distanceToTunnel = stepsToReach(
      #           myState, food.coords, myTunnel.coords)
      #       distanceToHill = stepsToReach(myState, food.coords, myHill.coords)
      #       times.append(min(distanceToTunnel, distanceToHill))
      #   food_time2 = 2 * min(times)

      # foodWin = 0
      # foodNeeded = 11 - myFood
      # while foodNeeded > 0:
      #   if food_time != -1:
      #     foodWin += food_time
      #   else:
      #     foodWin += food_time2
      #   food_time = -1
      #   foodNeeded -= 1
      if not enemyQueen == None:
        if enemyQueen.coords == enemyHill.coords:
          occupyWin += 20
      steps = occupyWin

      # if len(myOffense) > 0:
      #   if myOffense[0].coords == enemyHill.coords:
      #     steps = 0
      #steps += 0 if myFood > 2 else 10
      #steps += 0 if len(myWorkers) == 1 else 10
      return steps


class Node:
  def __init__(self, move, state, depth, steps, parent):
    self.move = move
    self.state = state
    self.depth = depth
    self.steps = steps + self.depth
    self.parent = parent
