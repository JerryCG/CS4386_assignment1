import numpy as np
import copy
from game import alignement
from game import empty_cells

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

def get_results(self_score,opponent_score):
    if self_score > opponent_score:
        return 1
    elif self_score < opponent_score:
        return -1
    else:
        return 0

class Simulation(object):
    def __init__(self, state, symbol, bad_actions=None):
        self.state = state
        self.self_symbol = symbol
        self.opponent_symbol = 'X' if self.self_symbol == 'O' else 'X'
        self.legal_actions = empty_cells(self.state)
        self.bad_actions = bad_actions
        self.nets = []
        self.ws = []

    def simulation(self,num):
        num = num
        if (not self.bad_actions is None) and (len(self.legal_actions) != len(self.bad_actions)):
            for bad_action in self.bad_actions:
                if bad_action in self.legal_actions:
                    self.legal_actions.remove(bad_action)
        if len(self.legal_actions) != 1:
            for action in self.legal_actions:
                net = 0.
                w = 0.
                state_copy = copy.copy(self.state)
                for i in range(num):
                    turn = 0
                    self_score = 0.
                    opponent_score = 0.
                    state_copy = copy.copy(self.state)
                    game_state = is_game_over(state_copy)
                    state_copy[action[0]][action[1]] = self.self_symbol
                    score = alignement(state_copy, action[0], action[1])
                    game_state = is_game_over(state_copy)
                    self_score+=score
                    turn = 1 - turn
                    while not game_state:
                        legal_moves = empty_cells(state_copy)
                        random_move = legal_moves[np.random.randint(len(legal_moves))]
                        if turn == 0:
                            state_copy[random_move[0]][random_move[1]] = self.self_symbol
                            game_state = is_game_over(state_copy)
                            score = alignement(state_copy, random_move[0], random_move[1])
                            self_score+=score
                        else:
                            state_copy[random_move[0]][random_move[1]] = self.opponent_symbol
                            game_state = is_game_over(state_copy)
                            score = alignement(state_copy, random_move[0], random_move[1])
                            opponent_score+=score
                        turn = 1 - turn
                    net = net + self_score - opponent_score
                    w += get_results(self_score, opponent_score)
                self.nets.append(net)
                self.ws.append(w)
            m = max(self.ws)
            w_best = [self.nets[i] for i, j in enumerate(self.ws) if j == m]
            w_best_index = [i for i, j in enumerate(self.ws) if j == m]
            selected_move = self.legal_actions[w_best_index[np.argmax(w_best)]]
        else:
            selected_move = self.legal_actions[0]
        return selected_move