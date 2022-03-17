import copy
import python.AIPlayerMCTS
from game import alignement

class MCTS:
    def __init__(self, root):
        self.root = root

    def best_action(self, simulations_number):
        for _ in range(0, simulations_number):
            python.AIPlayerMCTS.turn = 0
            python.AIPlayerMCTS.self_score = 0
            python.AIPlayerMCTS.opponent_score = 0
            python.AIPlayerMCTS.depth = 0
            v = self.tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        # exploitation only
        return self.root.best_child()

    def tree_policy(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                for i in range(6):
                    for j in range(6):
                        if current_node.state[i][j] != current_node.best_child().state[i][j]:
                            action = [i,j]
                            break
                score = alignement(current_node.best_child().state, action[0], action[1])
                if python.AIPlayerMCTS.turn == 0:
                    python.AIPlayerMCTS.self_score+=score
                    python.AIPlayerMCTS.turn = 1 - python.AIPlayerMCTS.turn
                    python.AIPlayerMCTS.depth += 1
                else:
                    python.AIPlayerMCTS.opponent_score+=score
                    python.AIPlayerMCTS.turn = 1 - python.AIPlayerMCTS.turn
                    python.AIPlayerMCTS.depth += 1
                current_node = current_node.best_child()
                if current_node.is_terminal_node():
                    python.AIPlayerMCTS.turn = 1 - python.AIPlayerMCTS.turn
                    python.AIPlayerMCTS.depth += 1
        return current_node