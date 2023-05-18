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
        ['.', '.', 'N', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['W', '.', '.', '.', 'E'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', 'S', '.', '.'],
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
    player1, player2 = 'r', 'g'
    f.add_player(player1)
    f.add_player(player2)
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
    player1 = 'r'
    f.add_player(player1)

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
    player1 = 'r'
    f.add_player(player1)
    await f.move_snakes({'r': 'd'})
    expected = 'Snake n crashes into wall'

    # WHEN
    with pytest.raises(const.GameOverLose):
        await f.move_snakes({'r': 'd'})
    printed = capsys.readouterr().out

    # THEN
    assert not f.players
    assert expected in printed

#
# def test_move_snakes_eat_itself():
#     # GIVEN
#     f = Field(size=3)
#     field = [
#         ['A', 'r', 'r'],
#         ['.', 'R', 'r'],
#         ['.', 'B', 'r'],
#     ]
#     players = {'r': 'd', 'b': 'a'}
#
#     # WHEN
#     f.generate_field_from_template(field)
#     results = f.move_snakes(players)
#
#     # THEN
#     assert not results['r'][0] and results['b'][0] and not results['game over']
#     assert 'r' not in f.snakes and 'b' in f.snakes
#
#
# def test_move_snakes_fight():
#     # GIVEN
#     f = Field(size=3)
#     field = [
#         ['A', 'r', 'r'],
#         ['R', 'r', 'r'],
#         ['B', '.', '.'],
#     ]
#     players = {'r': 's', 'b': 'w'}
#
#     # WHEN
#     f.generate_field_from_template(field)
#     results = f.move_snakes(players)
#
#     # THEN
#     assert results['r'] and not results['b'] and not results['game over']
#     assert 'r' in f.snakes and 'b' not in f.snakes
#
#
# def test_game_win():
#     # GIVEN
#     f = Field(size=3)
#     field = [
#         ['B', 'A', 'R'],
#         ['b', 'G', 'r'],
#         ['b', 'g', 'r'],
#     ]
#     players = {'g': 'w'}
#
#     # WHEN
#     f.generate_field_from_template(field)
#     results = f.move_snakes(players)
#
#     # THEN
#     assert results['g'] and results['game over']
#     assert 'r' in f.snakes and 'b' in f.snakes and 'g' in f.snakes
