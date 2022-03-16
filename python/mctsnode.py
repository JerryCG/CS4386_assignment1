import numpy as np
import copy
from collections import defaultdict
from game import alignement
from game import empty_cells
import python.AIPlayerMCTS

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
    if self_score >= opponent_score:
        python.AIPlayerMCTS.self_score = 0
        python.AIPlayerMCTS.opponent_score = 0
        return 1
    else:
        python.AIPlayerMCTS.self_score = 0
        python.AIPlayerMCTS.opponent_score = 0
        return -1
    

def move(state, action):
    new_state = copy.copy(state)
    new_state[action[0]][action[1]] = 1
    return new_state

class MCTSNode(object):
    def __init__(self, state, parent=None):
        self._number_of_visits = 0.
        self._results = defaultdict(int)
        self._results[1] = 0.
        self._results[-1] = 0.
        self.state = copy.copy(state)
        self.parent = parent
        self.children = []
        self._untried_actions = None
        self._untried_actions = empty_cells(self.state)

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        next_state = move(self.state, action)
        score = alignement(next_state, action[0], action[1])
        if python.AIPlayerMCTS.turn == 0:
            python.AIPlayerMCTS.self_score+=score
        else:
            python.AIPlayerMCTS.opponent_score+=score
        child_node = MCTSNode(next_state, parent=self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return is_game_over(self.state)

    def rollout(self):
        current_rollout_state = copy.copy(self.state)
        rollout_turn = 1 - python.AIPlayerMCTS.turn
        while not is_game_over(current_rollout_state):
            possible_moves = empty_cells(current_rollout_state)
            action = self.rollout_policy(possible_moves)
            current_rollout_state = move(current_rollout_state, action)
            score = alignement(current_rollout_state, action[0], action[1])
            if rollout_turn == 0:
                python.AIPlayerMCTS.self_score+=score
                rollout_turn = 1 - rollout_turn
            else:
                python.AIPlayerMCTS.opponent_score+=score
                rollout_turn = 1 - rollout_turn
        return game_result(python.AIPlayerMCTS.self_score, python.AIPlayerMCTS.opponent_score)

    def backpropagate(self, result):
        self._number_of_visits += 1.
        if python.AIPlayerMCTS.turn == 0:
            self._results[result] += 1.
        else:
            self._results[-result] += 1.
        python.AIPlayerMCTS.turn = 1 - python.AIPlayerMCTS.turn
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            (c.q() / (c.n())) + c_param * np.sqrt((2 * np.log(self.n()) / (c.n())))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]