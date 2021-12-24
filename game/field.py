import random
from game._snake import _Snake


class Field:
    def __init__(self, size=15):
        self.size = size
        self.field = [['.' for _ in range(size)] for _ in range(size)]
        self.snakes = []
        self.entry_point = (len(self.field) - 1, len(self.field) // 2)
        self.apple = tuple()
        self.generate_apple()

    def show(self):
        print('--' * self.size)
        for row in self.field:
            print(' '.join(row))
        print('--' * self.size)

    def clear(self):
        self.field = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.snakes = []
        self.generate_apple()

    def add_player(self, player):
        snake = _Snake(player)
        self.snakes.append(snake)
        snake.head = self.entry_point
        self.field[self.entry_point[0]][self.entry_point[1]] = snake.color.upper()

    def add_snake(self, snake):
        self.snakes.append(snake)
        for y in range(self.size):
            for x in range(self.size):
                if (x, y) == snake.head:
                    self.field[x][y] = snake.color.upper()
                if (x, y) in snake.body:
                    self.field[x][y] = snake.color

    def remove_snake(self, snake):
        self.snakes.remove(snake)
        for y in range(self.size):
            for x in range(self.size):
                if (x, y) in snake.body or (x, y) == snake.head:
                    self.field[x][y] = '.'

    def move_snakes(self, players):
        for player in players.keys():
            for snake in self.snakes:
                if snake == player:
                    self.remove_snake(snake)
                    if snake.move(players[player], self.size, self.apple):
                        self.add_snake(snake)
                        if snake.head == self.apple:
                            self.apple = ()
                            self.generate_apple()
                    break
        return self.field

    def free_cells(self):
        cells = []
        for y in range(self.size):
            for x in range(self.size):
                if self.field[x][y] == '.':
                    cells.append((x, y))
        return cells

    def generate_apple(self):
        self.apple = random.choice(self.free_cells())
        for y in range(self.size):
            for x in range(self.size):
                if (x, y) == self.apple:
                    self.field[x][y] = 'A'
