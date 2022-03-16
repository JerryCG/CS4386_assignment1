from python.AIPlayerRandom import AIPlayerRandom
import numpy as np
from game import alignement

results = []
p1_scores = []
p2_scores = []

p1 = AIPlayerRandom('p1', 'X', isAI=True)
p2 = AIPlayerRandom('p2', 'O', isAI=True)

for i in range(10000):
    state = np.full((6,6), None)
    p1_score = 0
    p2_score = 0
    turn = 0
    for j in range(36):
        if turn == 0:
            p1_action = p1.get_move(state=state, player='X')
            state[p1_action[0]][p1_action[1]] = 'X'
            score = alignement(state, p1_action[0], p1_action[1])
            p1_score+=score
            turn = 1 - turn
        else:
            p2_action = p2.get_move(state=state, player='O')
            state[p2_action[0]][p2_action[1]] = 'O'
            score = alignement(state, p2_action[0], p2_action[1])
            p2_score+=score
            turn = 1 - turn
    p1_scores.append(p1_score)
    p2_scores.append(p2_score)
    if p1_score > p2_score:
        results.append(1)
    elif p1_score < p2_score:
        results.append(-1)
    else:
        results.append(0)

print('p1 wins:', results.count(1), results.count(1)/10000)
print('p2 wins:', results.count(-1), results.count(-1)/10000)
print('draws:  ', results.count(0), results.count(0)/10000)
print('--------------------------------------------------')
print('p1_score mean:', sum(p1_scores)/10000)
print('p2_score mean:', sum(p2_scores)/10000)
