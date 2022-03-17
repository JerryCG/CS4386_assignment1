import copy
from game import alignement
from game import empty_cells
from math import inf as infinity

def is_game_over(state):
    over = True
    for i in range(6):
        for j in range(6):
            if state[i][j] == None:
                over = False
                break
        if over == False:
            break
    return over

def game_result(self_score, opponent_score):
    if(self_score>opponent_score):
        return 1
    elif(self_score<opponent_score):
        return -1
    else:
        return 0

class TwoStepBest(object):
    def __init__(self, state, symbol):
        self.state = state
        self.self_symbol = symbol
        self.opponent_symbol = 'X' if self.self_symbol == 'O' else 'X'
        self.legal_actions = empty_cells(self.state)
        self.best_net_score = 0
        self.best_opponent_score = 0
        self.best_action = None
        self.bad_actions = []

    def twostepbest(self):
        for self_action in self.legal_actions:
            net_score = 0
            state_copy = copy.copy(self.state)
            state_copy[self_action[0]][self_action[1]] = self.self_symbol
            self_score = alignement(state_copy, self_action[0], self_action[1])
            net_score+=self_score
            if not is_game_over(state_copy):
                opponent_legal_actions = empty_cells(state_copy)
                for opponent_action in opponent_legal_actions:
                    new_state_copy = copy.copy(state_copy)
                    new_state_copy[opponent_action[0]][opponent_action[1]] = self.opponent_symbol
                    opponent_score = alignement(new_state_copy, opponent_action[0], opponent_action[1])
                    if opponent_score > self.best_opponent_score:
                        self.best_opponent_score = opponent_score
                net_score-=self.best_opponent_score
                self.best_opponent_score = 0
            if net_score > self.best_net_score:
                self.best_net_score = net_score
                self.best_action = self_action
            if net_score < 0:
                self.bad_actions.append(self_action)
        if self.best_action is None:
            return False, self.bad_actions
        else:
            return True, self.best_action