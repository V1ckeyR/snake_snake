import random
from core.game._snake import _Snake


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
        if player not in self.snakes:
            snake = _Snake(player)
            self.snakes.append(snake)
            snake.head = self.entry_point
            self.field[self.entry_point[0]][self.entry_point[1]] = snake.color.upper()

    def remove_player(self, player):
        if player in self.snakes:
            self.remove_snake(self.snakes[self.snakes.index(player)])

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

    def move_snake(self, snake, direction):
        """:returns snake status and True if game goal has reached"""
        self.remove_snake(snake)  # kill snake
        snake_alive = False
        if snake.move(direction, self.size, self.apple) and self.snake_vs_snake(snake):  # True if snake survived
            self.add_snake(snake)  # resurrect snake if so
            snake_alive = True
            if snake.head == self.apple:  # check if we need new apple
                return snake_alive, not self.generate_apple()
        return snake_alive, False

    def move_snakes(self, players):
        results = {"game over": False}
        for player in players.keys():
            if player not in self.snakes:
                results[player] = False
            else:
                snake = self.snakes[self.snakes.index(player)]
                snake_status, game_status = self.move_snake(snake, direction=players[player])
                results[player] = (snake_status, snake.score)
                if game_status:
                    results["game over"] = game_status  # change only if True
        return results

    def free_cells(self):
        cells = []
        for y in range(self.size):
            for x in range(self.size):
                if self.field[x][y] == '.':
                    cells.append((x, y))
        return cells

    def generate_apple(self):
        """:returns True if apple was generated"""
        try:
            self.apple = random.choice(self.free_cells())
        except IndexError:
            return False

        for y in range(self.size):
            for x in range(self.size):
                if (x, y) == self.apple:
                    self.field[x][y] = 'A'
        return True

    def get_player_score(self, player):
        return self.snakes[player].score

    def snake_vs_snake(self, attacker):
        """ :returns True if attacker stay alive"""
        for snake in self.snakes:
            if snake != attacker:
                if attacker.head in [snake.head] + snake.body:
                    attacker_alive, defender_alive = attacker.attack(snake)
                    self.remove_snake(snake)
                    if defender_alive:
                        self.add_snake(snake)
                    if attacker_alive:
                        return True
                    return False
        return True

    def generate_field_from_template(self, field):
        self.field = field
        for y in range(self.size):
            for x in range(self.size):
                cell = field[x][y]
                if cell == '.':
                    continue
                if cell == 'A':
                    self.apple = (x, y)
                    continue

                snake_name = cell.lower()
                if snake_name not in self.snakes:
                    snake = _Snake(snake_name)
                    self.snakes.append(snake)
                else:
                    snake = self.snakes[self.snakes.index(snake_name)]
                if snake_name == cell:
                    snake.body.append((x, y))
                else:
                    snake.head = (x, y)
