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
        self.field = [['.' for _ in range(size)] for _ in range(size)]
        self.apple = (0, 0)
        self._generate_apple()

    def print(self):
        print(*[' '.join(i) for i in self.field], sep='\n')

    def add_player(self, uid):
        if uid in self.players.keys():
            print('This user already in game!')
            return

        if len(self.players) >= len(list(self.entry_points.points)):
            raise NoMorePlayers

        self.players[uid] = Snake(list(self.entry_points.points)[len(self.players)])
        print(f'Player {uid} --> {self.players[uid]}')  # TODO: print --> logging

    def remove_player(self, uid):
        if uid not in self.players.keys():
            print('This user not in game')

        self.players.pop(uid)

        if not self.players.keys():
            raise GameOver

        self._draw_field()

    async def move_snakes(self, keys: dict):
        # TODO: compare time
        async with asyncio.TaskGroup() as tg:
            for uid, snake in self.players.items():
                tg.create_task(snake.go(keys[uid], self.apple))

        dead_users = self._dead_snakes()  # check survivors

        self._snake_fight()  # check snake-vs-snake

        dead_users.update(self._dead_snakes())  # check survivors

        self._draw_field()

        if not self._free_cells():
            print('Game over! Players won!')
            raise GameOverWin

        return dead_users

    def generate_field_from_template(self, field):
        pass

    def _draw_apple(self):
        x, y = self.apple
        self.field[x][y] = 'A'

    def _draw_snakes(self):
        for snake in self.players.values():
            for x, y in snake.body():
                self.field[x][y] = snake.name.upper() if (x, y) == snake.head else snake.name

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

    def _dead_snakes(self):
        users = set()
        for snake in self.players.values():
            if not snake.alive:
                uid = list(self.players.keys())[list(self.players.values()).index(snake)]
                users.add(uid)
                self.players.pop(uid)

        if not self.players.keys():
            print('Game over! Players lose!')
            raise GameOverLose

        return users  # TODO: notify user

    def _snake_fight(self):
        snake_ball = set()
        for snake in self.players.values():
            other_snakes = list(self.players.values())
            other_snakes.remove(snake)
            for another_snake in other_snakes:
                if snake.head in another_snake.body():
                    snake_ball.update((snake, another_snake))

        min_length = min([len(snake.body()) for snake in snake_ball], default=0)
        print(f'Ready to fight: {snake_ball} -> Smallest length: {min_length}')
        for snake in snake_ball:
            if len(snake.body) > min_length:
                snake.tail = snake.tail[:min_length]
            else:
                snake.alive = False
