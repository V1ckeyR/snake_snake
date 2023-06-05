import asyncio
import random

from .snake import Snake
from .constants import *


class Field:
    def __init__(self, size=FIELD_SIZE):
        self.size = size
        self.divider = '-' * size * 3
        self.entry_points = EntryPoint(size)
        self.players = {}
        self.dead_players = []
        self.field = [['.' for _ in range(size)] for _ in range(size)]
        self.apple = None

    def print(self):
        print(*[' '.join(i) for i in self.field], sep='\n')

    def clear(self):
        self.players = {}
        self.dead_players = []
        self.field = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.apple = None

    def get_score(self, uid):
        if uid not in self.players.keys():
            print('This user has no score')
            return
        return self.players[uid].score

    def get_color(self, uid):
        if uid not in self.players.keys():
            print('This user has no score')
            return
        return self.players[uid].color

    def get_status(self, uid):
        return uid in self.players.keys()

    def add_player(self, uid, color='g'):
        if uid in self.players.keys():
            print('This user already in game!')
            return

        if len(self.players) >= len(list(self.entry_points.points)):
            raise NoMorePlayers

        self.players[uid] = Snake(entry_point=list(self.entry_points.points)[len(self.players)], color=color)
        print(f'Player {uid} --> {self.players[uid]}')  # TODO: print --> logging

        if not self.apple:
            self._generate_apple()

        self._draw_field()

    def remove_player(self, uid):
        if uid not in self.players.keys():
            print('This user not in game')
            return

        print(f'User {uid} ({self.players[uid]}) is dead')
        self.players.pop(uid)
        self.dead_players.append(uid)

        if not self.players.keys():
            raise GameOverLose

        self._draw_field()

    async def move_snakes(self, keys: dict):
        async with asyncio.TaskGroup() as tg:
            for uid, snake in self.players.items():
                tg.create_task(snake.go(keys.get(uid), self.apple, self.size))

        self.dead_players = []
        self._check_survivors()  # check survivors
        self._snake_fight()  # check snake-vs-snake
        self._check_survivors()  # check survivors
        self._draw_field()

        if not self._free_cells():
            print('Game over! Players won!')
            raise GameOverWin

    def _draw_apple(self):
        if self.apple:
            x, y = self.apple
            self.field[x][y] = 'A'

    def _draw_snakes(self):
        for snake in self.players.values():
            for x, y in snake.body():
                self.field[x][y] = snake.color.upper() if (x, y) == snake.head else snake.color

    def _draw_field(self):
        self.field = [['.' for _ in range(self.size)] for _ in range(self.size)]
        if self.apple in [snake.head for snake in list(self.players.values())]:
            self._generate_apple()
        else:
            self._draw_apple()
        self._draw_snakes()
        self.print()

    def _free_cells(self):
        return [(x, y) for x in range(self.size) for y in range(self.size) if self.field[x][y] == '.']

    def _generate_apple(self):
        if not self._free_cells():
            return

        self.apple = random.choice(self._free_cells())
        self._draw_apple()
        print(f'Generated apple {self.apple}')

    def _check_survivors(self):
        users = set()
        for snake in self.players.values():
            if not snake.alive:
                users.add(list(self.players.keys())[list(self.players.values()).index(snake)])

        [self.remove_player(user) for user in users]

    def _snake_fight(self):
        if len(self.players) < 2:
            return

        snake_ball = set()
        for snake in self.players.values():
            other_snakes = list(self.players.values())
            other_snakes.remove(snake)
            for another_snake in other_snakes:
                if snake.head in another_snake.body():
                    snake_ball.update((snake, another_snake))

        min_length = min([len(snake.body()) for snake in snake_ball], default=0)
        print(f'Ready to fight: {snake_ball} -> Smallest: {min_length}' if len(snake_ball) else 'No fight')
        for snake in snake_ball:
            if len(snake.body()) > min_length:
                snake.tail = snake.tail[:min_length]
            else:
                snake.alive = False
