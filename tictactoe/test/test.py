# requires running server and database
import pytest
from tictactoe import main
from init_db import (
    create_tables,
    sample_data,
)

async def test_get_homepage(cli, tables_and_data):
    resp = await cli.get('/')
    assert resp.status == 200
    assert await resp.text() == 'Lets play tic tac toe'


async def test_game_create(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'testgame2'})
    assert resp.status == 200
    assert await resp.text() == 'New Game: testgame2 has been created'


async def test_duplicate_game_not_allowed(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'testgame3'})
    resp = await cli.post('/game', data={'name':'testgame3'})
    assert resp.status == 406
    assert await resp.text() == 'a game called testgame3 already exists.'


async def test_game_with_no_name_throws_error(cli, tables_and_data):
    resp = await cli.post('/game')
    assert resp.status == 400
    assert await resp.text() == 'You have not specified a game name'


async def test_player_same_player_not_allowed_in_a_game_twice(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'anewgame'})
    assert resp.status == 200
    resp = await cli.post('/game/anewgame/player', data={'player_name':'John'})
    assert resp.status == 200
    resp = await cli.post('/game/anewgame/player', data={'player_name':'John'})
    assert await resp.text() == 'the game must have two different players'


async def test_player_only_allowed_two_players_in_a_game(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'newgame'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Dave'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Dave1'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Dave2'})
    assert await resp.text() == 'this game already has 2 players'


async def test_player_first_player_added_to_game_and_given_crosses(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'newgamefirstplayer'})
    assert resp.status == 200
    resp = await cli.post('/game/newgamefirstplayer/player', data={'player_name':'Dave'})
    assert await resp.text() == 'new player: Dave has been added to game: newgamefirstplayer and is using crosses'


async def test_player_first_crosses_second_noughts(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'newgametwoplayers'})
    assert resp.status == 200
    resp = await cli.post('/game/newgametwoplayers/player', data={'player_name':'Dave'})
    assert await resp.text() == 'new player: Dave has been added to game: newgametwoplayers and is using crosses'
    resp = await cli.post('/game/newgametwoplayers/player', data={'player_name':'John'})
    assert await resp.text() == 'new player: John has been added to game: newgametwoplayers and is using noughts'


async def test_move_square_must_be_a_number(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'newgame'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Dave'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Dave/move', data={'square':'ioa'})
    assert resp.status == 400
    assert await resp.text() == 'square must be a number'


async def test_move_square_cant_be_less_than_1(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'newgame'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Dave'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Dave/move', data={'square':'-1'})
    assert resp.status == 400
    assert await resp.text() == 'square must be between 1 and 9'


async def test_move_square_cant_be_greater_than_9(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'newgame'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Dave'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Dave/move', data={'square':'11'})
    assert resp.status == 400
    assert await resp.text() == 'square must be between 1 and 9'

async def test_move_player_must_be_a_participant_of_the_game(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'newgame'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Dave'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Jason'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/John/move', data={'square':'1'})
    assert resp.status == 400
    assert await resp.text() == 'Player with name John is not playing this game'

async def test_move_player_must_be_a_participant_of_the_game(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'newgame'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Dave'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Jason'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Dave/move', data={'square':'1'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Jason/move', data={'square':'1'})
    assert resp.status == 400
    assert await resp.text() == 'Square 1 has already been used'

async def test_a_player_wins_with_diagonal_15(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'newgame'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Dave'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Jason'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Dave/move', data={'square':'1'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Jason/move', data={'square':'2'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Dave/move', data={'square':'5'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Jason/move', data={'square':'3'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Dave/move', data={'square':'9'})
    assert resp.status == 200
    assert await resp.text() == 'Congratulations Dave.  You won the game.'

async def test_moves_no_player_wins_all_squares_filled(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'newgame'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Dave'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Jason'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Dave/move', data={'square':'3'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Jason/move', data={'square':'1'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Dave/move', data={'square':'4'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Jason/move', data={'square':'2'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Dave/move', data={'square':'5'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Jason/move', data={'square':'6'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Dave/move', data={'square':'8'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Jason/move', data={'square':'7'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Dave/move', data={'square':'9'})
    assert await resp.text() == 'Game Over: No Winner, all squares filled'

async def test_move_not_this_players_turn(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'newgame'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Dave'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Jason'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Jason/move', data={'square':'1'})
    assert resp.status == 400
    assert await resp.text() == 'It is not this players turn'

async def test_check_game_board_is_correct_after_four_moves(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'newgame'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Dave'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Jason'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Dave/move', data={'square':'1'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Jason/move', data={'square':'2'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Dave/move', data={'square':'3'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Jason/move', data={'square':'5'})
    assert resp.status == 200
    resp = await cli.get('/game/newgame/board')
    assert resp.status == 200
    assert await resp.text() == '\nX O X \n  O   \n      \n'

async def test_three_correct_moves_have_correct_response(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'newgame'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Dave'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player', data={'player_name':'Jason'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Dave/move', data={'square':'1'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Jason/move', data={'square':'4'})
    assert resp.status == 200
    resp = await cli.post('/game/newgame/player/Dave/move', data={'square':'8'})
    assert resp.status == 200

async def test_add_a_new_player_to_db(cli, tables_and_data):
    resp = await cli.post('/player', data={'player_name':'Susan'})
    assert resp.status == 200
    assert await resp.text() == 'Player: Susan was successfully added.'

async def test_duplicate_players_cannot_be_added(cli, tables_and_data):
    resp = await cli.post('/player', data={'player_name':'Susan'})
    assert resp.status == 200
    resp = await cli.post('/player', data={'player_name':'Susan'})
    assert resp.status == 400
    assert await resp.text() == 'A player with name Susan has already been added'

async def test_get_all_players_returns_correct_players(cli, tables_and_data):
    resp = await cli.post('/player', data={'player_name':'Susan'})
    assert resp.status == 200
    resp = await cli.post('/player', data={'player_name':'Fred'})
    assert resp.status == 200
    resp = await cli.post('/player', data={'player_name':'Jeff'})
    assert resp.status == 200
    resp = await cli.get('/player')
    assert resp.status == 200
    assert await resp.text() == 'players are: [\'Susan\', \'Fred\', \'Jeff\']'

async def test_get_all_games_returns_correct_games(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'game1'})
    assert resp.status == 200
    resp = await cli.post('/game', data={'name':'game2'})
    assert resp.status == 200
    resp = await cli.post('/game', data={'name':'game3'})
    assert resp.status == 200
    resp = await cli.get('/game')
    assert resp.status == 200
    assert await resp.text() == 'Games are: [(\'game1\', \'NEW\'), (\'game2\', \'NEW\'), (\'game3\', \'NEW\')]'


