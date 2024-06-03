from flask import Flask, render_template, request, jsonify
import pickle
from model import update
from model import check_winner

app = Flask(__name__)

board = (0,) * 9
current_player = 1 
stats_probs =  pickle.load(open("states_probs.p", "rb"))
t = 0

@app.route('/')
def index():
    return render_template('game.html')

@app.route('/move', methods=['POST'])
def move():
    global current_player, board, t, stats_probs
    data = request.get_json()
    index = int(data['index'])

    if board[index] == 0:
        new_board = board[:index] + (current_player,) + board[index+1:]
        update(board, new_board, stats_probs, t)
        board = new_board
        if check_winner(board):
            pickle.dump(stats_probs, open("states_probs.p", "wb"))
            return jsonify({'board': board, 'winner': current_player})
        if check_tie():
            pickle.dump(stats_probs, open("states_probs.p", "wb"))
            return jsonify({'board': board, 'winner': 'Tie'})
        current_player = -1 

        t+=1 

        computer_move(stats_probs)
        if check_winner(board):
            return jsonify({'board': board, 'winner': current_player})
        if check_tie():
            return jsonify({'board': board, 'winner': 'Tie'})

        current_player = 1  # Switch back to player
        return jsonify({'board': board})
    else:
        return jsonify({'error': 'Invalid move'}), 400

@app.route('/reset', methods=['POST'])
def reset():
    global board, current_player, stats_probs
    board = (0,) * 9
    current_player = 1
    stats_probs =  pickle.load(open("states_probs.p", "rb"))
    return jsonify({'board': board, 'current_player': current_player})

def computer_move(states_probs):
    global current_player, board, t
    empty_cells = [i for i in range(9) if board[i] == 0]
    if empty_cells:
        best_index = -1
        best_prob = -1
        for cell in empty_cells:
            board = board[:cell] + (current_player,) + board[cell+1:]
            prob_win = states_probs[board]
            if prob_win > best_prob:
                best_prob = prob_win
                best_index = cell
            board = board[:cell] + (0,) + board[cell+1:]

        new_board = board[:best_index] + (current_player,) + board[best_index+1:]
        update(board, new_board, states_probs, t)
        board = new_board
        t+=1

def check_tie():
    return all(cell != 0 for cell in board)

if __name__ == '__main__':
    app.run(debug=True)
