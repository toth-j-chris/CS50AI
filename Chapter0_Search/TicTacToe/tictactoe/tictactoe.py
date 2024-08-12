"""
Tic Tac Toe Player
"""

import math
import sys

from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


class InvalidMoveException(Exception):
    pass


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # store number of Xs and Os on the board
    num_x = 0
    num_o = 0

    # count number of Xs and Os
    for row in board:
        for cell in row:
            if cell == X:
                num_x += 1
            elif cell == O:
                num_o += 1

    if num_x > num_o:
        return O

    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    action_set = set()

    # if a cell is empty, add it to the set of actions
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is EMPTY:
                action_set.add((i, j))

    return action_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # raise exception if the move is invalid
    if action not in actions(board):
        raise InvalidMoveException

    # deep copy to avoid changing the board state
    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    winner = None

    # check for horizontal winner
    for row in board:
        if (row[0] == row[1] == row[2]) and row[0]:
            winner = row[0]

    # check for vertical winner
    for i in range(len(board[1])):
        if (board[1][i] == board[0][i] == board[2][i]) and board[1][i]:
            winner = board[1][i]

    # check diagonals
    if (board[1][1] == board[0][0] == board[2][2]) and board[1][1]:
        winner = board[1][1]

    if (board[1][1] == board[0][2] == board[2][0]) and board[1][1]:
        winner = board[1][1]

    return winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # if there is a winner or the board is full, return True
    if winner(board) or (len(actions(board)) == 0):
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    game_winner = winner(board)

    if game_winner == X:
        return 1

    if game_winner == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if board is terminal, return None
    if terminal(board):
        return None

    # get the current player
    curr_player = player(board)

    # get set of actions for current state
    action_set = actions(board)
    best_action = None

    # if player is X, start best_score low
    # if player is O, start best_score high
    if curr_player == X:
        best_score = -math.inf
    elif curr_player == O:
        best_score = math.inf

    # find the action that optimizes the score for the current player
    for action in action_set:
        if curr_player == X:
            action_score = min_value(result(board, action))
            if action_score > best_score:
                best_score = action_score
                best_action = action
        elif curr_player == O:
            action_score = max_value(result(board, action))
            if action_score < best_score:
                best_score = action_score
                best_action = action

    return best_action


def max_value(board):
    # if we reached a terminal state, return its value
    if terminal(board):
        return utility(board)

    # if not a terminal state, find the action with the highest min_value()
    action_set = actions(board)

    # start best_score at lowest possible value
    best_score = -math.inf

    for action in action_set:
        action_score = min_value(result(board, action))
        if action_score > best_score:
            best_score = action_score

    return best_score


def min_value(board):
    # if we reached a terminal state, return its value
    if terminal(board):
        return utility(board)

    # if not a terminal state, find the action with the highest max_value()
    action_set = actions(board)

    # start best_score at highest possible value
    best_score = math.inf

    for action in action_set:
        action_score = max_value(result(board, action))
        if action_score < best_score:
            best_score = action_score

    return best_score
