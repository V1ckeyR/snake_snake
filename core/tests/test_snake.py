import pytest

import core.game.constants as const

from ..game.snake import Snake

@pytest.mark.asyncio
async def test_go_wrong_direction():
    # GIVEN
    field_size = 3
    snake1, snake2 = Snake(const.EntryPoint(field_size).North), Snake(const.EntryPoint(field_size).South)
    apple = (field_size - 1, field_size - 1)

    # WHEN
    await snake1.go('z', apple, field_size)
    await snake2.go('w', apple, field_size)

    # THEN
    assert snake1.alive
    assert snake2.alive
    assert snake1.head == snake2.head

@pytest.mark.asyncio
async def test_go_back():
    # GIVEN
    field_size = 3
    snake1, snake2 = Snake(const.EntryPoint(field_size).North), Snake(const.EntryPoint(field_size).South)
    apple = (field_size - 1, field_size - 1)

    # WHEN
    await snake1.go('w', apple, field_size)
    await snake2.go('w', apple, field_size)

    # THEN
    assert snake1.alive
    assert snake2.alive
    assert snake1.head == snake2.head

@pytest.mark.asyncio
async def test_go_in_empty_cell():
    # GIVEN
    field_size = 3
    snake = Snake(const.EntryPoint(field_size).North)
    apple = (field_size - 1, field_size - 1)

    # WHEN
    await snake.go('s', apple, field_size)

    # THEN
    assert snake.head == (1, 1)
    assert snake.tail == []
    assert snake.alive

@pytest.mark.asyncio
async def test_go_meet_apple():
    # GIVEN
    field_size = 3
    snake = Snake(const.EntryPoint(field_size).North)
    apple = (1, 1)

    # WHEN
    await snake.go('s', apple, field_size)

    # THEN
    assert snake.head == (1, 1)
    assert snake.tail == [(0, 1)]
    assert snake.alive

@pytest.mark.asyncio
async def test_go_meet_boundaries():
    # GIVEN
    field_size = 3
    snake = Snake(const.EntryPoint(field_size).North)
    apple = (field_size - 1, field_size - 1)

    # WHEN
    await snake.go('s', apple, field_size)
    await snake.go('s', apple, field_size)
    await snake.go('s', apple, field_size)

    # THEN
    assert not snake.alive

@pytest.mark.asyncio
async def test_go_meet_itself():
    # GIVEN
    field_size = 3
    snake = Snake(const.EntryPoint(field_size).North)
    apple = (field_size - 1, field_size - 1)
    await snake.go('s', (1, 1), field_size)
    await snake.go('s', (2, 1), field_size)
    await snake.go('a', (2, 0), field_size)
    await snake.go('w', (1, 0), field_size)

    # WHEN
    await snake.go('d', apple, field_size)

    # THEN
    assert not snake.alive
