from .constants import Point, OPPOSITE, FIELD_SIZE, OPERATION


class Snake:
    def __init__(self, entry_point: Point, color='g'):
        self.name = entry_point.name
        self.head = entry_point.head
        self.tail = []
        self.move = entry_point.move
        self.color = color
        self.score = 0
        self.alive = True

    def __repr__(self):
        return f'Snake {self.name}'

    def body(self):
        return [self.head, *self.tail]

    async def go(self, key, apple, field_size=FIELD_SIZE):
        # snake can not go back
        self.move = key if key in OPPOSITE.keys() and OPPOSITE[key] != self.move else self.move
        print(f'{self} go {self.move}: {self.body()}')
        new_head = OPERATION[self.move](*self.head)
        new_tail = self.body()[:-1]

        if new_head == apple:
            print(f'{self} eats apple')
            self.score += 1
            new_tail = self.body()

        if new_head in new_tail:
            print(f'{self} crashes into itself')
            self.alive = False
            return

        if not (0 <= new_head[0] < field_size and 0 <= new_head[1] < field_size):
            print(f'{self} crashes into wall')
            self.alive = False
            return

        self.head = new_head
        self.tail = new_tail
        print(f'{self} moved: {self.body()}')
