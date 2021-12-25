class _Snake:
    def __init__(self, color):
        self.head = ()
        self.body = []
        self.color = color
        self.last_op = 'w'
        self.score = 0

        self.operation = {
            'w': lambda x, y: (x - 1, y),
            'a': lambda x, y: (x, y - 1),
            's': lambda x, y: (x + 1, y),
            'd': lambda x, y: (x, y + 1),
        }

    def move(self, key, field_size, apple):
        if key not in 'wasd':
            key = self.last_op

        new_head = self.operation[key](*self.head)

        if self.body and new_head == self.body[0]:
            key = self.last_op
            new_head = self.operation[key](*self.head)

        if not (0 <= new_head[0] < field_size and 0 <= new_head[1] < field_size):
            print(f"{self} is dead")
            return False

        if new_head in self.body:
            print(f"{self} is dead")
            return False

        if new_head == apple:
            self.body = [self.head] + self.body
            self.score += 1
        elif self.body:
            self.body = [self.head] + self.body[:-1]
        self.head = new_head
        self.last_op = key
        return True

    def __eq__(self, other):
        return self.color == other

    def __repr__(self):
        return f'Snake {self.color}'
