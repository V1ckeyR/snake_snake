import pytest

import core.game.constants as const

from ..game.field import Field
from ..game.snake import Snake


def test_add_player():
    # GIVEN
    f = Field(size=5)
    player = 'r'

    # WHEN
    f.add_player(player)

    # THEN
    assert f.players
    assert len(f.players) == 1
    assert f.players[player].name == const.EntryPoint(size=5).points[0].name

def test_add_same_player():
    # GIVEN
    f = Field(size=5)
    player = 'r'

    # WHEN
    f.add_player(player)
    f.add_player(player)

    # THEN
    assert f.players
    assert len(f.players) == 1
    assert f.players[player].name == const.EntryPoint(size=5).points[0].name

def test_add_fifth_player():
    # GIVEN
    f = Field(size=5)
    player1, player2, player3, player4, player5 = 'r', 'g', 'b', 'y', 'c'

    # WHEN
    f.add_player(player1)
    f.add_player(player2)
    f.add_player(player3)
    f.add_player(player4)

    with pytest.raises(const.NoMorePlayers):
        f.add_player(player5)

    # THEN
    assert f.players
    assert len(f.players) == 4

def test_remove_player():
    # GIVEN
    f = Field(size=5)
    player1, player2 = 'r', 'g'

    # WHEN
    f.add_player(player1)
    f.add_player(player2)
    f.remove_player(player2)

    # THEN
    assert len(f.players) == 1
    assert player1 in f.players.keys()
    assert player2 not in f.players.keys()

def test_remove_nonexistent_player():
    # GIVEN
    f = Field(size=5)
    player1, player2 = 'r', 'g'

    # WHEN
    f.add_player(player1)
    f.remove_player(player2)

    # THEN
    assert len(f.players) == 1
    assert player1 in f.players.keys()
    assert player2 not in f.players.keys()


@pytest.mark.asyncio
async def test_print_field(capsys):
    # GIVEN
    f = Field(size=5)
    player1, player2, player3, player4 = 'r', 'g', 'b', 'y'
    f.add_player(player1)
    f.add_player(player2)
    f.add_player(player3)
    f.add_player(player4)
    a_x, a_y = [(x, y) for x in range(5) for y in range(5) if f.field[x][y] == 'A'][0]  # find apple coordinates
    expected_field = [
        ['.', '.', 'G', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['G', '.', '.', '.', 'G'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', 'G', '.', '.'],
    ]
    expected_field[a_x][a_y] = 'A'
    printed_field = '\n'.join([' '.join(i) for i in expected_field])

    # WHEN
    f.print()
    printed = capsys.readouterr().out

    # THEN
    assert expected_field == f.field
    assert printed_field in printed

@pytest.mark.asyncio
async def test_move_snakes_succeed(capsys):
    # GIVEN
    f = Field(size=5)
    f.add_player('r')
    f.add_player('g')
    expected_r = 'Snake n go d'
    expected_g = 'Snake s go a'

    # WHEN
    await f.move_snakes({'r': 'd', 'g': 'a'})
    printed = capsys.readouterr().out

    # THEN
    assert expected_r in printed
    assert expected_g in printed

@pytest.mark.asyncio
async def test_move_snakes_eat_apple():
    # GIVEN
    f = Field(size=3)
    f.add_player('r')

    # WHEN
    await f.move_snakes({'r': 'd'})  # check every cell in field
    await f.move_snakes({'r': 's'})
    await f.move_snakes({'r': 's'})
    await f.move_snakes({'r': 'a'})
    await f.move_snakes({'r': 'a'})
    await f.move_snakes({'r': 'w'})
    await f.move_snakes({'r': 'w'})
    await f.move_snakes({'r': 'd'})
    await f.move_snakes({'r': 's'})

    # THEN
    assert len(f.players['r'].body()) != 0

@pytest.mark.asyncio
async def test_move_snakes_meet_boundary(capsys):
    # GIVEN
    f = Field(size=3)
    f.add_player('r')
    await f.move_snakes({'r': 'd'})
    expected = 'Snake n crashes into wall'

    # WHEN
    with pytest.raises(const.GameOverLose):
        await f.move_snakes({'r': 'd'})
    printed = capsys.readouterr().out

    # THEN
    assert not f.players
    assert expected in printed

@pytest.mark.asyncio
async def test_move_snakes_eat_itself(capsys):
    # GIVEN
    f = Field(size=3)
    f.add_player('r')
    f.players['r'].tail = [(1, 1), (2, 1), (2, 0)]
    expected = 'Snake n crashes into itself'

    # WHEN
    with pytest.raises(const.GameOverLose):
        await f.move_snakes({'r': 's'})
    printed = capsys.readouterr().out

    # THEN
    assert expected in printed

@pytest.mark.asyncio
async def test_move_snakes_fight_draw(capsys):
    # GIVEN
    f = Field(size=3)
    f.add_player('r')
    f.add_player('g')
    expected = 'Ready to fight'

    # WHEN
    with pytest.raises(const.GameOverLose):
        await f.move_snakes({'r': 's', 'g': 'w'})
    printed = capsys.readouterr().out

    # THEN
    assert expected in printed
    assert not f.players.get('r')
    assert not f.players.get('g')

@pytest.mark.asyncio
async def test_move_snakes_fight_player_r(capsys):
    # GIVEN
    f = Field(size=3)
    f.add_player('r')
    f.players['r'].head = (1, 1)
    f.players['r'].tail = [(1, 0)]
    f.add_player('g')
    expected = 'Ready to fight'

    # WHEN
    await f.move_snakes({'r': 's', 'g': 'w'})
    printed = capsys.readouterr().out

    # THEN
    assert expected in printed
    assert f.players['r'].alive
    assert not f.players.get('g')

@pytest.mark.asyncio
async def test_move_snakes_fight_player_g(capsys):
    # GIVEN
    f = Field(size=3)
    f.add_player('r')
    f.add_player('g')
    f.players['g'].head = (1, 1)
    f.players['g'].tail = [(1, 2)]
    expected = 'Ready to fight'

    # WHEN
    await f.move_snakes({'r': 's', 'g': 'w'})
    printed = capsys.readouterr().out

    # THEN
    assert expected in printed
    assert not f.players.get('r')
    assert f.players['g'].alive

@pytest.mark.asyncio
async def test_game_win(capsys):
    # GIVEN
    f = Field(size=2)
    f.add_player('r')
    expected = 'Game over! Players won!'

    # WHEN
    with pytest.raises(const.GameOverWin):
        while f.players['r'].alive:
            await f.move_snakes({'r': 'a'})
            await f.move_snakes({'r': 's'})
            await f.move_snakes({'r': 'd'})
            await f.move_snakes({'r': 'w'})

    printed = capsys.readouterr().out

    # THEN
    assert expected in printed
