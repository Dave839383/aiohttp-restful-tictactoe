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


async def test_player_same_player_not_allowed_to_game_twice(cli, tables_and_data):
    resp = await cli.post('/game', data={'name':'anewgame'})
    assert resp.status == 200
    resp = await cli.post('/game/anewgame/player', data={'player_name':'John'})
    assert resp.status == 200
    resp = await cli.post('/game/anewgame/player', data={'player_name':'John'})
    assert await resp.text() == 'the game must have two different players'


async def test_player_only_allowed_two_players(cli, tables_and_data):
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




