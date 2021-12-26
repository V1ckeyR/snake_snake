import random

from game._snake import _Snake


def test_move_wrong_direction():
    # GIVEN
    snake1, snake2 = _Snake('r'), _Snake('b')
    snake1.head, snake2.head = (1, 0), (1, 0)
    field_size = random.randint(2, 15)
    apple = (field_size - 1, field_size - 1)

    # WHEN
    snake1_alive = snake1.move('z', field_size, apple)
    snake2_alive = snake2.move('w', field_size, apple)

    # THEN
    assert snake1.head == (0, 0)
    assert snake1.head == snake2.head
    assert snake1.body == snake2.body
    assert snake1_alive
    assert snake2_alive


def test_move_back():
    # GIVEN
    snake1, snake2 = _Snake('r'), _Snake('b')
    snake1.head, snake2.head = (1, 0), (1, 0)
    snake1.body, snake2.body = [(2, 0)], [(2, 0)]
    field_size = random.randint(3, 15)
    apple = (field_size - 1, field_size - 1)

    # WHEN
    snake1_alive = snake1.move('s', field_size, apple)
    snake2_alive = snake2.move('w', field_size, apple)

    # THEN
    assert snake1.head == (0, 0)
    assert snake1.head == snake2.head
    assert snake1.body == snake2.body
    assert snake1_alive
    assert snake2_alive


def test_move_in_empty_cell():
    # GIVEN
    snake = _Snake('r')
    snake.head = (1, 0)
    snake.body = [(2, 0)]
    field_size = random.randint(3, 15)
    apple = (field_size - 1, field_size - 1)

    # WHEN
    snake_alive = snake.move('w', field_size, apple)

    # THEN
    assert snake.head == (0, 0)
    assert snake.body == [(1, 0)]
    assert snake_alive


def test_move_meet_apple():
    # GIVEN
    snake = _Snake('r')
    snake.head = (1, 0)
    snake.body = [(2, 0)]
    field_size = random.randint(3, 15)
    apple = (0, 0)

    # WHEN
    snake_alive = snake.move('w', field_size, apple)

    # THEN
    assert snake.head == (0, 0)
    assert snake.body == [(1, 0), (2, 0)]
    assert snake_alive


def test_move_meet_snake():
    # move method doesn't know where actually are other snakes
    # GIVEN
    #   0 1 2 3
    # 0 b b B
    # 1   R
    # 2   r
    # 3
    snake1, snake2 = _Snake('r'), _Snake('b')
    snake1.head, snake2.head = (1, 1), (0, 2)
    snake1.body, snake2.body = [(2, 1)], [(0, 1), (0, 0)]
    field_size = random.randint(4, 15)
    apple = (field_size - 1, field_size - 1)

    # WHEN
    snake1_alive = snake1.move('w', field_size, apple)
    snake2_alive = snake2.move('d', field_size, apple)

    # THEN
    assert snake1.head == (0, 1)
    assert snake1.body == [(1, 1)]
    assert snake1_alive
    assert snake2.head == (0, 3)
    assert snake2.body == [(0, 2), (0, 1)]
    assert snake2_alive


def test_move_meet_boundaries():
    # GIVEN
    snake = _Snake('r')
    snake.head = (0, 0)
    field_size = 3
    apple = (field_size - 1, field_size - 1)

    # WHEN + THEN
    assert not snake.move('w', field_size, apple)


def test_move_meet_itself():
    # GIVEN
    #   0 1 2 3
    # 0 r r r
    # 1   R r
    # 2   r r
    # 3
    snake = _Snake('r')
    snake.head = (1, 1)
    snake.body = [(2, 1), (2, 2), (1, 2), (0, 2), (0, 1), (0, 0)]
    field_size = 4
    apple = (field_size - 1, field_size - 1)

    # WHEN + THEN
    assert not snake.move('w', field_size, apple)


def test_attack_win():
    # GIVEN
    s1 = _Snake('r')
    s2 = _Snake('b')

    # WHEN
    s1.body = [(0, 1), (0, 2), (0, 3)]
    s2.body = [(0, 1)]
    result = s1.attack(s2)

    # THEN
    assert result == (True, False)
    assert s1.body == [(0, 1), (0, 2)]
    assert s2.body == [(0, 1)]


def test_attack_draw():
    # GIVEN
    s1 = _Snake('r')
    s2 = _Snake('b')

    # WHEN
    s1.body = [(0, 1)]
    s2.body = [(0, 1)]
    result = s1.attack(s2)

    # THEN
    assert (False, False) == result
    assert s1.body == [(0, 1)]
    assert s2.body == [(0, 1)]


def test_attack_lose():
    # GIVEN
    s1 = _Snake('r')
    s2 = _Snake('b')

    # WHEN
    s1.body = [(0, 1)]
    s2.body = [(0, 1), (0, 2), (0, 3)]
    result = s1.attack(s2)

    # THEN
    assert (False, True) == result
    assert s1.body == [(0, 1)]
    assert s2.body == [(0, 1), (0, 2)]


def test_custom_equal():
    # GIVEN
    name = 'r'
    s1 = _Snake(name)
    s2 = _Snake(name)

    # WHEN + THEN
    assert s1 == s2
    assert s1 == name
