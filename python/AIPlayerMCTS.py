import copy
from math import inf as infinity
from turtle import TurtleScreen

from numpy import deprecate_with_doc
from python.mcts import MCTS
from python.mctsnode import MCTSNode

class AIPlayerMCTS(object):
    def __init__(self, name, symbole, isAI=False):
        self.name = name
        self.symbole = symbole
        self.isAI = isAI
        self.score=0

    def stat(self):
        return self.name + " won " + str(self.won_games) + " games, " + str(self.draw_games) + " draw."

    def __str__(self):
        return self.name
    def get_isAI(self):
        return self.isAI
    def get_symbole(self):
        return self.symbole
    def get_score(self):
        return self.score
    def add_score(self,score):
    	self.score+=score
    
    def empty_cells(self,state):
        cells = []

        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if cell is None:
                    cells.append([x, y])
        return cells
    
    def get_move(self,state, player):
        state_copy = copy.copy(state)
        for i in range(6):
            for j in range(6):
                if not state_copy[i][j] is None:
                    state_copy[i][j] = 1
        global self_score
        self_score = 0
        global opponent_score
        opponent_score = 0
        global turn
        turn = 0
        global depth
        depth = 0
        root = MCTSNode(state=state_copy)
        mcts = MCTS(root)
        best_node = mcts.best_action(1000)
        best_state = best_node.state
        best_move = [0,0]
        for i in range(6):
            for j in range(6):
                if state_copy[i][j] != best_state[i][j]:
                    best_move = [i,j]
                    break
        return best_move