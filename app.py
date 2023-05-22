import asyncio

from eventlet.green import time
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import eventlet
from core.game import Field
from core.game.constants import *
from security import *
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder="templates", static_folder="static")
eventlet.monkey_patch(thread=False)
socket_io = SocketIO(app, async_mode='eventlet')
app.config['SECRET_KEY'] = secret_key

""" DB SETTINGS """
uri = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{NAME}'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

game = Field(size=11)
available = ['r', 'y', 'c', 'v']
movements = {}


@app.route('/')
def hello_snake():
    return render_template('index.html', size=range(game.size))


@app.route('/store')
def skins_store():
    return render_template('store.html', items=range(20))


@socket_io.on('message')
def handle_message(data):
    print('Message: ' + data)


@socket_io.on('start game')
def handle_start_game():
    try:
        color = available.pop(0)
        game.add_player(request.sid, color)
        emit('field', game.field, broadcast=True)
        emit('personal data', color)
    except IndexError:
        emit('limit')  # TODO


def check_dead():
    print('dead_players', game.dead_players)
    for dead in game.dead_players:
        available.append(game.get_color(dead))
        emit('dead', to=dead)

def handle_game():
    color = game.get_color(request.sid)
    try:
        asyncio.run(game.move_snakes(movements))
    except GameOverLose:
        check_dead()
        game.clear()
        pass
        # emit('lose', broadcast=True)  # TODO
    except GameOverWin:
        check_dead()
        game.clear()
        pass
        # emit('win', broadcast=True)  # TODO
    else:
        check_dead()
        if game.get_status(request.sid):
            emit('personal score', game.get_score(request.sid))
    finally:
        emit('field', game.field, broadcast=True)

    movements.clear()
    emit('field', game.field, broadcast=True)

@socket_io.on('game')
def set_key(key):
    if request.sid not in movements.keys():
        movements[request.sid] = key

    while game.players:
        time.sleep(1)
        handle_game()

@socket_io.on('connect')
def connect():
    print('Client connected')
    emit('field', game.field)


@socket_io.on('disconnect')
def disconnect():
    print('Client disconnected')

    color = game.get_color(request.sid)
    available.append(color)

    try:
        game.remove_player(request.sid)
    except GameOverLose:
        game.clear()
        pass
        # emit('lose', broadcast=True)

    emit('field', game.field, broadcast=True)


if __name__ == '__main__':
    socket_io.run(app, debug=True)
