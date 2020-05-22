from math import *
import random
import copy
from generatornTicTacToeEndState import generatorTictacToeEndState

import time
import argparse

# Do not edit follow config variables
# player const value
USER_AI = 2
USER_PLAYER = 1

STATE_VALUE_EMPTY = 0

STATE_GO = 0
STATE_DRAW = -1
STATE_END = [USER_PLAYER, USER_AI]

RESULT_VALUE_DRAW = 0.5
RESULT_VALUE_WIN = 1
RESULT_VALUE_NONE = 0
# end config variables

# game config
DEFAULT_BOARD_SIZE = 3
DEFAULT_VS_AI = True
DEFAULT_START_PLAYER = "Player"

# Value for MCTS
CHECK_END_CASE_POSITION = []

## End "do not edit"
C = 2

def getNextTurnUser(user):
    if user == USER_PLAYER:
        return USER_AI
    return USER_PLAYER 

class Game:
    def __init__(self, startUser, boardSize):
        self.state = []
        self.boardSize = boardSize
        for i in range(boardSize*boardSize):
            self.state.append(STATE_VALUE_EMPTY)

        self.userToPlay = startUser

    def getMovablePosition(self):
        if self.checkEnd() != STATE_GO:
            return []
        else:
            moves = []
            for i in range(len(self.state)):
                if self.state[i] == STATE_VALUE_EMPTY:
                    moves.append(i)
                    
            return moves

    def getResult(self, player):
        result = self.checkEnd()

        if result == STATE_DRAW:
            return RESULT_VALUE_DRAW
        
        elif result == player:
            return RESULT_VALUE_WIN
        else:
            return RESULT_VALUE_NONE

    def checkEnd(self):
        
        # result = -5 # for check process for using tuple

        # slow than fixed board size
        for tup in CHECK_END_CASE_POSITION:
            first_value = self.state[tup[0]]
            all_same = True
            for pos in tup[1:]:
                all_same = all_same and first_value == self.state[pos]
                
            if all_same is True and first_value != STATE_VALUE_EMPTY:
                return first_value

        # for (x,y,z) in CHECK_END_CASE_POSITION:
        #     if self.state[x] == self.state[y] == self.state[z]:
        #         if self.state[x] != STATE_VALUE_EMPTY:
        #             # assert result == self.state[x]
        #             return self.state[x]
                
        if STATE_VALUE_EMPTY not in self.state:
            return STATE_DRAW

        return STATE_GO

    # input
    #   self.userToPlay: just before play user
    #   moveCase: moving position for next play user
    # return
    #   play or not
    def doMove(self, movePosition): 
        if len(self.state) > movePosition and movePosition >= 0 and self.state[movePosition] == STATE_VALUE_EMPTY:
            self.userToPlay = getNextTurnUser(self.userToPlay)
            self.state[movePosition] = self.userToPlay
            return True
        return False
            
    def copy(self):
        game = Game(startUser=self.userToPlay, boardSize=self.boardSize)
        game.state = self.state[:]
        return game

    def __repr__(self):
        s = ""
        for i in range(len(self.state)):
            s += ".0X"[self.state[i]]+" "
            if i % self.boardSize == self.boardSize-1:
                s += "\n"
        return s

class Node(object):
    def __init__(self, movePosition=0, parent=None, game=None):
        self.parent = parent
        self.movePosition = movePosition      # case of moving
        self.wins = 0       # winning count after ith moving
        self.visits = 0    # simulation count after ith moving
        self.child = []
        self.game = game
    
        if game != None:
            self.untriedMovePositions = game.getMovablePosition()
            self.userToPlay = game.userToPlay
        else:
            self.untriedMovePositions = []
            self.userToPlay = None

    # ascending
    def selectChild(self):
        s = sorted(self.child, key = lambda c: c.wins/c.visits + sqrt(C * log(self.visits) / c.visits))
        return s[-1]

    def addChild(self, movePosition ,game):
        node = Node(movePosition = movePosition, parent = self, game = copy.deepcopy(game))
        self.untriedMovePositions.remove(movePosition)
        self.child.append(node)
        return node

    def update(self, win):
        self.visits += 1
        self.wins += win
        
    def __repr__(self):
        return "[M {0:2.0f}".format(self.movePosition+1) + " W/V {0:5.0f} /{1:5.0f} = {2:0.5f}".format(self.wins, self.visits, self.wins/self.visits)+" U" + str(self.untriedMovePositions) + "]"

    def childToString(self):
        s =""
        for c in self.child:
            s += str(c) + "\n"
        return s

def UCT(game, isVsAI, itermax):
    rootnode = Node(game = game)
    
    if isVsAI is True:
        print ("{0}'s turn".format(["AI2", "AI"][game.userToPlay-1]))
    else:
        print ("{0}'s turn".format(["PLAYER", "AI"][game.userToPlay-1]))

    
    for i in range(itermax):
        node = rootnode
        state = copy.deepcopy(game)
        
        #selection
        while len(node.untriedMovePositions) == 0 and len(node.child) != 0:
            node = node.selectChild()
            res = state.doMove(node.movePosition)
            assert res
        
        #Expansion
        if len(node.untriedMovePositions) != 0:
            m = random.choice(node.untriedMovePositions)
            state.doMove(m)
            node = node.addChild(m, state)
        
        #simulation
        while len(state.getMovablePosition()) != 0:
            state.doMove(random.choice(state.getMovablePosition()))
        
        #BackPropagation
        while node != None:
            node.update(state.getResult(node.userToPlay))
            node = node.parent
                
    s = sorted(rootnode.child, key = lambda c: c.wins/c.visits) # ?
    res = sorted(s, key = lambda c: c.visits)
    for i in range(len(res)-1, 0, -1):
        print (str(res[i]))
    return res[-1].movePosition
    
        
def UCTPlayGame(startUser, boardSize, isVsAI):
    game = Game(startUser=startUser, boardSize=boardSize )
    while len(game.getMovablePosition()) != 0:
        print (str(game))
        if game.userToPlay == USER_AI:
            rootstate = copy.deepcopy(game)
            m = UCT(rootstate, isVsAI, itermax = 10000)
            print ("AI best move: " + str(m+1) + "\n")
        else:
            if isVsAI is True:
                rootstate2 = copy.deepcopy(game)
                m = UCT(rootstate2, isVsAI, itermax = 5000)
                print ("AI2 best move: " + str(m+1) + "\n")
            else:
                m = input("which Do you want? {0}: ".format([i+1 for i in game.getMovablePosition()]))
                m = int(m) - 1
                print ("User Move: " + str(m+1) + "\n")
        
        game.doMove(m)
        
    print (str(game)) # display end state

    if game.getResult(game.userToPlay) == RESULT_VALUE_WIN:
        user = "AI"
        if game.userToPlay == USER_AI:
            user = "User"

        print (""+user+" Player Wins!!")
 
    else: print ("Draw!!")
    


def main(parser):

    args = parser.parse_args()
    print("args: ", args)
    print("--- start game ---")

    start_time = time.time()
    
    global CHECK_END_CASE_POSITION
    CHECK_END_CASE_POSITION = generatorTictacToeEndState(args.board_size)
    startUser = USER_PLAYER

    if args.start_user != "Player":
        startUser = USER_AI

    UCTPlayGame(startUser, args.board_size, args.is_AIvsAI)
    print("--- game duration: {0:0.5f} seconds ---".format(time.time() - start_time))


if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument('--board_size', type=int, choices=[DEFAULT_BOARD_SIZE, 4, 5, 6, 7, 8], default=DEFAULT_BOARD_SIZE)
    parser.add_argument('--is_AIvsAI', type=bool, choices=[DEFAULT_VS_AI, False], default=DEFAULT_VS_AI)
    parser.add_argument('--start_user', type=str, choices=[DEFAULT_START_PLAYER, "AI"], default=DEFAULT_START_PLAYER)

    main(parser)


    


