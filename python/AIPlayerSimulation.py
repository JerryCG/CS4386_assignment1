import copy
from python.simulation import Simulation
from math import inf as infinity
class AIPlayerSimulation(object):
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
    
    def get_move(self,state,player):
        root = Simulation(state=state, symbol=player)
        selected_move = root.simulation(100)
        return selected_move
