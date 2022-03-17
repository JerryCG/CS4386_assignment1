import copy
import python.AIPlayerMCTS
from game import alignement
from math import inf as infinity
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

def makeMove(state, action):
    new_state = copy.copy(state)
    new_state[action[0]][action[1]] = 1
    return new_state

def negamax(board, netScore, maxDepth, currentDepth):
    if is_game_over(board) or currentDepth == maxDepth:
        return netScore, None
    
    bestMove = None
    bestScore = -infinity

    for move in empty_cells(board):
        netscore = netScore
        newBoard = makeMove(board, move)
        score = alignement(board, move[0], move[1])
        netscore += score
        #recursive
        recursedScore, currentMove = negamax(newBoard, -netscore, maxDepth, currentDepth+1)

        currentScore = - recursedScore

        # Update the best score
        if currentScore > bestScore:
            bestScore = currentScore
            bestMove = move
    
    # Return the score and the best move
    return bestScore, bestMove