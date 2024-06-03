import copy
import pickle
import csv

def check_winner(board):

    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  
        (0, 3, 6), (1, 4, 7), (2, 5, 8), 
        (0, 4, 8), (2, 4, 6)             
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != 0:
            return True
    return False


def get_valid_states_memoized():
    initial_state = [0] * 9
    states = []
    get_valid_states(initial_state, states, True)
    return states


def get_valid_states(current_state, states, x_plays):
    states.append(current_state)

    if 0 not in current_state:
        return
    
    if check_winner(current_state):
        return
    
    current_player = 1 if x_plays else -1
    valid_positions = [i for i in range(len(current_state)) if current_state[i] == 0]

    for position in valid_positions:
        new_position = copy.deepcopy(current_state)
        new_position[position] = current_player
        if new_position not in states:
            get_valid_states(new_position, states, not x_plays)

def initialize():
    states = get_valid_states_memoized()
    states_probs = {}
    for state in states:
        if check_winner(state, 1):
            states_probs[tuple(state)] = 0
        elif check_winner(state, -1):
            states_probs[tuple(state)] = 1
        else:
            states_probs[tuple(state)] = 0.5
    pickle.dump(states_probs, open("states_probs.p", "wb"))

def update(current_state, next_state, probs, t):
    probs[current_state] += 0.9**t * (probs[next_state] - probs[current_state])

    
    


if __name__ == '__main__':
    initialize()