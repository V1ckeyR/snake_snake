from core.game.field import Field


def test_add_player():
    # GIVEN
    f = Field(size=4)
    player = 'r'

    # WHEN
    f.add_player(player)

    # THEN
    assert f.snakes == [player]


def test_add_same_player():
    # GIVEN
    f = Field(size=4)
    player = 'r'

    # WHEN
    f.add_player(player)
    f.add_player(player)

    # THEN
    assert f.snakes == [player]


def test_remove_player():
    # GIVEN
    f = Field(size=4)
    player = 'r'

    # WHEN
    f.add_player(player)
    f.remove_player(player)

    # THEN
    assert not f.snakes


def test_generate_field_from_template():
    # GIVEN
    f1, f2 = Field(size=3), Field(size=3)
    expected_field = [
        ['A', 'R', '.'],
        ['.', '.', '.'],
        ['.', '.', 'B'],
    ]

    # WHEN
    f1.apple = (0, 0)

    f1.add_player('r')
    red = f1.snakes[f1.snakes.index('r')]
    f1.move_snake(red, 'w')

    f1.add_player('b')
    blue = f1.snakes[f1.snakes.index('b')]
    f1.move_snake(red, 'w')
    f1.move_snake(blue, 'd')

    f2.generate_field_from_template(expected_field)

    # THEN
    assert f1.snakes[0].body == f2.snakes[0].body


def test_move_snakes_succeed():
    # GIVEN
    f = Field(size=3)
    field = [
        ['A', '.', '.'],
        ['.', 'R', '.'],
        ['.', 'B', '.'],
    ]
    players = {'r': 'w', 'b': 'd'}
    expected_field = [
        ['A', 'R', '.'],
        ['.', '.', '.'],
        ['.', '.', 'B'],
    ]

    # WHEN
    f.generate_field_from_template(field)
    results = f.move_snakes(players)

    # THEN
    assert results['r'] and results['b'] and not results['game over']
    assert 'r' in f.snakes and 'b' in f.snakes
    assert f.field == expected_field


def test_move_snakes_eat_apple():
    # GIVEN
    f = Field(size=3)
    field = [
        ['A', 'R', '.'],
        ['.', '.', '.'],
        ['.', 'B', '.'],
    ]
    players = {'r': 'a', 'b': 'w'}

    # WHEN
    f.generate_field_from_template(field)
    results = f.move_snakes(players)

    # THEN
    assert results['r'] and results['b'] and not results['game over']
    assert 'r' in f.snakes and 'b' in f.snakes


def test_move_snakes_meet_boundary():
    # GIVEN
    f = Field(size=3)
    field = [
        ['A', 'R', '.'],
        ['.', '.', '.'],
        ['.', 'B', '.'],
    ]
    players = {'r': 'w', 'b': 'w'}

    # WHEN
    f.generate_field_from_template(field)
    results = f.move_snakes(players)

    # THEN
    assert not results['r'][0] and results['b'][0] and not results['game over']
    assert 'r' not in f.snakes and 'b' in f.snakes


def test_move_snakes_eat_itself():
    # GIVEN
    f = Field(size=3)
    field = [
        ['A', 'r', 'r'],
        ['.', 'R', 'r'],
        ['.', 'B', 'r'],
    ]
    players = {'r': 'd', 'b': 'a'}

    # WHEN
    f.generate_field_from_template(field)
    results = f.move_snakes(players)

    # THEN
    assert not results['r'][0] and results['b'][0] and not results['game over']
    assert 'r' not in f.snakes and 'b' in f.snakes


def test_move_snakes_fight():
    # GIVEN
    f = Field(size=3)
    field = [
        ['A', 'r', 'r'],
        ['R', 'r', 'r'],
        ['B', '.', '.'],
    ]
    players = {'r': 's', 'b': 'w'}

    # WHEN
    f.generate_field_from_template(field)
    results = f.move_snakes(players)

    # THEN
    assert results['r'] and not results['b'] and not results['game over']
    assert 'r' in f.snakes and 'b' not in f.snakes


def test_game_win():
    # GIVEN
    f = Field(size=3)
    field = [
        ['B', 'A', 'R'],
        ['b', 'G', 'r'],
        ['b', 'g', 'r'],
    ]
    players = {'g': 'w'}

    # WHEN
    f.generate_field_from_template(field)
    results = f.move_snakes(players)

    # THEN
    assert results['g'] and results['game over']
    assert 'r' in f.snakes and 'b' in f.snakes and 'g' in f.snakes
