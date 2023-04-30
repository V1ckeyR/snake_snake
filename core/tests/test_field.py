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

    player1, player2 = 'r', 'g'
    f.add_player(player1)
    f.add_player(player2)
    apple = (2, 4)
    expected = ". . . . .\n" \
               ". . N . .\n" \
               ". . . . A\n" \
               ". . S . .\n" \
               ". . . . ."

    # WHEN
    f.generate_field_from_template(expected)
    f.print()
    printed = capsys.readouterr().out

    # THEN
    assert expected in printed
    assert f.apple == apple

def test_generate_field_from_template():
    # GIVEN
    f = Field(size=5)
    f.apple = (2, 4)
    player1, player2 = 'r', 'g'
    expected = ". . . . .\n" \
               ". . N . .\n" \
               ". . . . A\n" \
               ". . S . .\n" \
               ". . . . ."

#
#     # WHEN
#     f1.apple = (0, 0)
#
#     f1.add_player('r')
#     red = f1.snakes[f1.snakes.index('r')]
#     f1.move_snake(red, 'w')
#
#     f1.add_player('b')
#     blue = f1.snakes[f1.snakes.index('b')]
#     f1.move_snake(red, 'w')
#     f1.move_snake(blue, 'd')
#
#     f2.generate_field_from_template(expected_field)
#
#     # THEN
#     assert f1.snakes[0].body == f2.snakes[0].body
#
#
# def test_move_snakes_succeed():
#     # GIVEN
#     f = Field(size=3)
#     field = [
#         ['A', '.', '.'],
#         ['.', 'R', '.'],
#         ['.', 'B', '.'],
#     ]
#     players = {'r': 'w', 'b': 'd'}
#     expected_field = [
#         ['A', 'R', '.'],
#         ['.', '.', '.'],
#         ['.', '.', 'B'],
#     ]
#
#     # WHEN
#     f.generate_field_from_template(field)
#     results = f.move_snakes(players)
#
#     # THEN
#     assert results['r'] and results['b'] and not results['game over']
#     assert 'r' in f.snakes and 'b' in f.snakes
#     assert f.field == expected_field
#
#
# def test_move_snakes_eat_apple():
#     # GIVEN
#     f = Field(size=3)
#     field = [
#         ['A', 'R', '.'],
#         ['.', '.', '.'],
#         ['.', 'B', '.'],
#     ]
#     players = {'r': 'a', 'b': 'w'}
#
#     # WHEN
#     f.generate_field_from_template(field)
#     results = f.move_snakes(players)
#
#     # THEN
#     assert results['r'] and results['b'] and not results['game over']
#     assert 'r' in f.snakes and 'b' in f.snakes
#
#
# def test_move_snakes_meet_boundary():
#     # GIVEN
#     f = Field(size=3)
#     field = [
#         ['A', 'R', '.'],
#         ['.', '.', '.'],
#         ['.', 'B', '.'],
#     ]
#     players = {'r': 'w', 'b': 'w'}
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
