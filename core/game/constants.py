from collections import namedtuple


FIELD_SIZE = 15
FIELD_CENTER = FIELD_SIZE // 2  # 7
OPPOSITE = {'w': 's', 'a': 'd', 's': 'w', 'd': 'a'}
OPERATION = {
    'w': lambda x, y: (x - 1, y),
    'a': lambda x, y: (x, y - 1),
    's': lambda x, y: (x + 1, y),
    'd': lambda x, y: (x, y + 1),
}


class NoMorePlayers(Exception):
    pass


class GameOver(Exception):
    pass


class GameOverLose(Exception):
    pass


class GameOverWin(Exception):
    pass


Point = namedtuple('Point', ('name', 'move', 'head'))


class EntryPoint:
    def __init__(self, size=FIELD_SIZE):
        self.North = Point(name='n', move='s', head=(0, size // 2))
        self.South = Point(name='s', move='w', head=(size - 1, size // 2))
        self.West = Point(name='w', move='d', head=(size // 2, 0))
        self.East = Point(name='e', move='a', head=(size // 2, size - 1))
        self.points = [self.North, self.South, self.West, self.East]
