# requires running server and database
import pytest
from tictactoe import main
from init_db import (
    create_tables,
    sample_data,
)


async def test_get_homepage(cli):
    resp = await cli.get('/')
    assert resp.status == 200
    assert await resp.text() == 'Lets play tic tac toe'


async def test_game_create(cli):
    resp = await cli.post('/game', data={'name':'testgame2'})
    assert resp.status == 200
    assert await resp.text() == 'New Game: testgame2 has been created'


async def test_duplicate_game_not_allowed(cli):
    resp = await cli.post('/game', data={'name':'testgame3'})
    resp = await cli.post('/game', data={'name':'testgame3'})
    assert resp.status == 406
    assert await resp.text() == 'a game called testgame3 already exists.'


async def test_game_with_no_name_throws_error(cli):
    resp = await cli.post('/game')
    assert resp.status == 400
    assert await resp.text() == 'You have not specified a game name'





