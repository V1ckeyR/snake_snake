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

        # snake can not go back
        if self.body and new_head == self.body[0]:
            key = self.last_op
            new_head = self.operation[key](*self.head)

        # snake grows from eating apple
        if new_head == apple:
            self.body = [self.head] + self.body
            self.score += 1
        elif self.body:
            self.body = [self.head] + self.body[:-1]

        # snake dies from boundaries
        if not (0 <= new_head[0] < field_size and 0 <= new_head[1] < field_size):
            print(f"{self} is dead")
            return False

        # snake dies from itself
        if new_head in self.body:
            print(f"{self} is dead")
            return False

        self.head = new_head
        self.last_op = key
        return True

    def attack(self, other):
        """
        Rule: Snake that crashed into another snake - attacker. Longer snake will survive, but will suffer damage
        :param other: snake-defender
        :return: True for survived, False for dead
        """
        delta = len(self.body) - len(other.body)
        if delta > 0:
            self.body = self.body[:delta]
            return True, False
        if delta < 0:
            other.body = other.body[:-delta]
            # print(other.body)
            return False, True
        return False, False

    def __eq__(self, other):
        return self.color == other

    def __repr__(self):
        return f'Snake {self.color}'
