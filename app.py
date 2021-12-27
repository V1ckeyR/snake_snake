from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import eventlet
from game.field import Field


app = Flask(__name__, template_folder="templates", static_folder="static")
eventlet.monkey_patch(thread=False)
socket_io = SocketIO(app, async_mode='eventlet')

game = Field()
available = ['r', 'o', 'y', 'g', 'c', 'b', 'v']
clients = {}
movements = {}


@app.route('/')
def hello_snake():
    return render_template('index.html', size=range(game.size))


@socket_io.on('message')
def handle_message(data):
    print('Message: ' + data)


@socket_io.on('start game')
def handle_start_game():
    try:
        player = available.pop(0)
        clients[request.sid] = player
        game.add_player(player)
        emit('field', game.field, broadcast=True)
        emit('personal data', player)
    except IndexError:
        emit('limit')  # TODO


@socket_io.on('game')
def handle_game(key):
    player = clients[request.sid]
    if player not in movements.keys():
        movements[player] = key

    results = game.move_snakes(movements)
    emit('personal score', results[player][1])
    if results['game over']:
        emit('win', broadcast=True)  # TODO
        game.clear()

    if not results[player][0]:
        clients.pop(request.sid)
        available.append(player)
        emit('dead')

    movements.clear()
    game.show()
    emit('field', game.field, broadcast=True)


@socket_io.on('connect')
def connect():
    print('Client connected')
    emit('field', game.field)


@socket_io.on('disconnect')
def disconnect():
    print('Client disconnected')
    snake = clients[request.sid]
    game.remove_player(snake)
    available.append(snake)
    clients.pop(request.sid)
    emit('field', game.field, broadcast=True)
