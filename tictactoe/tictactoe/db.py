# db.py
import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String
)

meta = MetaData()

game = Table(
    'game', meta,

    Column('name', String(200), primary_key=True),
    Column('status', String(200)),
)

# store a history of all moves in all games here,
# each row has a gameid, a playerid, squarenum, and typeofmove
moves = Table(
    'moves', meta,

    Column('id', Integer, primary_key=True),
    Column('square', String(200)),
    Column('move_type', String(10)),
    Column('game_name',
           String(200),
           ForeignKey('game.name', ondelete='CASCADE')),
    Column('player_name',
           String(200),
           ForeignKey('player.name', ondelete='CASCADE')),
)

player = Table(
    'player', meta,

    Column('name', String(200), primary_key=True),
)

# history of all games and the players tied to those games.
# Will store current score for each player in the game.
# useful for retrieving game statistics.
gameplayerinformation = Table(
    'gameplayerinformation', meta,

    Column('id', Integer, primary_key=True),
    Column('score', String(200), nullable=False),
    Column('move_type', String(10), nullable=False),
    Column('game_name',
           String(200),
           ForeignKey('game.name', ondelete='CASCADE')),
    Column('player_name',
           String(200),
           ForeignKey('player.name', ondelete='CASCADE')),
)


async def init_pg(app):
    print('init_pg')
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()
