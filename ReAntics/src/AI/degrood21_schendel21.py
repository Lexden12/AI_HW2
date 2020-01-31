import random
import sys
sys.path.append("..")  #so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import *
from AIPlayerUtils import *


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
        super(AIPlayer,self).__init__(inputPlayerId, "Random")
    
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
        if currentState.phase == SETUP_PHASE_1:    #stuff on my side
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
        elif currentState.phase == SETUP_PHASE_2:   #stuff on foe's side
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
        print(self.heuristicStepsToGoal(currentState))
        moves = listAllLegalMoves(currentState)
        for move in moves:
          getNextState(currentState, move)

        return selectedMove

    ##
    #bestMove
    #Description: Gets the best move from the list of possible moves
    #
    #Parameters:
    #   nodes - List of nodes which contain the possible moves from this location and their rank
    #           Used to find the best move
    #
    #Return: Best move from the moves in nodes
    ##
    def bestMove(self, nodes):
        
    
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
      tunnels = getConstrList(myState, types = (TUNNEL,))
      myTunnel = tunnels[1] if (tunnels[0].coords[1] > 5) else tunnels[0]
      enemyTunnel = tunnels[0] if (myTunnel is tunnels[1]) else tunnels[1]
      hills = getConstrList(myState, types = (ANTHILL,))
      myHill = hills[1] if (hills[0].coords[1] > 5) else hills[0] 
      enemyHill = hills[1] if (myHill is hills[0]) else hills[0]

      foods = getConstrList(myState, None, (FOOD,))

      myWorkers = getAntList(myState, me, (WORKER,))
      myOffense = getAntList(myState, me, (SOLDIER, R_SOLDIER, DRONE))
      shortest = 1000
      for ant in myOffense:
        dist = stepsToReach(myState, ant.coords, enemyHill.coords)
        if dist < shortest:
          shortest = dist
      occupyWin = shortest + enemyHill.captureHealth

      food_times = []
      for w in myWorkers:
        if w.carrying:
          #We must check every worker and the distance between the anthill and the tunnel.
          #in order to decide which one is quicker to go to. 
          distanceToTunnel = stepsToReach(myState, w.coords, myTunnel.coords)
          distanceToHill = stepsToReach(myState, w.coords, myHill.coords)
          min_dist = min(distanceToTunnel, distanceToHill)
          food_times.append(min_dist)

        #Otherwise, we want to move toward the food
        else:
          distanceToFood = []
          for f in foods:
            distanceToFood.append(stepsToReach(myState, w.coords, f.coords))
          min_food = 1000
          idx = 0
          for i in range(len(distanceToFood)):
            if distanceToFood[i] < min_food:
              min_food = distanceToFood[i]
              idx = i
          distanceToTunnel = stepsToReach(myState, foods[i].coords, myTunnel.coords)
          distanceToHill = stepsToReach(myState, foods[i].coords, myHill.coords)
          min_dist = min(distanceToTunnel, distanceToHill) + min_food
          food_times.append(min_dist)
      
      foodDists = []
      for food in foods:
        distanceToTunnel = stepsToReach(myState, food.coords, myTunnel.coords)
        distanceToHill = stepsToReach(myState, food.coords, myHill.coords)
        foodDists.append(min(distanceToTunnel, distanceToHill))
      foodDist = min(foodDists) * 2
      
      foodWin = 0
      foodNeeded = 11 - myFood
      while foodNeeded > 0:
        if len(food_times) > 0:
          foodWin += min(food_times)
          food_times.remove(min(food_times))
        else:
          foodWin += foodDist
        foodNeeded -= 1
      return min(foodWin, occupyWin)

class Node:
  def __init__(self, move, state, depth, steps, parent):
    self.move = moved
    self.state = state
    self.depth = 0
    self.steps = steps + self.depth
    self.parent = parent
