from flask import Flask, g
from shogi import Player, Board
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

player_board = None
enemy_board = None

@app.before_first_request
def set_players():
    global player_board, enemy_board
    player_board = Board()
    enemy_board = Board()


@app.route('/')
def start():
    global player_board
    return player_board.board_to_string()

@app.route('/reset')
def reset():
    global player_board, enemy_board
    player_board = Board()
    enemy_board = Board()
    return player_board.board_to_string()

@app.route('/player_board')
def player_board():
    global player_board
    return player_board.board_to_string()

@app.route('/enemy_board')
def enemy_board():
    global enemy_board
    return enemy_board.board_to_string()

@app.route('/player_move/<command>')
def player_move(command):
    if len(command) == 4: #add in int conversion check
        global player_board, enemy_board
        player_board.move_piece(int(command[0]), int(command[1]), int(command[2]), int(command[3]))
        enemy_board.set_board(player_board.flip_board())
        return player_board.board_to_string()
    else:
        return "input is not 4 digits"

@app.route('/enemy_move/<command>')
def enemy_move(command):
    if len(command) == 4: #add in int conversion check
        global player_board, enemy_board
        enemy_board.move_piece(int(command[0]), int(command[1]), int(command[2]), int(command[3]))
        player_board.set_board(enemy_board.flip_board())
        return enemy_board.board_to_string()
    else:
        return "input is not 4 digits"

if __name__ == '__main__':
    app.run()