# db.py
# SQL Alchemy ORM doesn't work asynchronously, see https://demos.aiohttp.org/en/latest/tutorial.html
# better to do it this way.
import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date
)

meta = MetaData()

game = Table(
    'game', meta,

    Column('id', Integer, primary_key=True),
    Column('status', String(200)),
)

# store a history of all moves in all games here, each row has a gameid, a playerid, squarenum, and typeofmove
moves = Table(
    'moves', meta,

    Column('id', Integer, primary_key=True),
    Column('square', String(200)),
    Column('move_type', String(10)),
    Column('player_id',
           Integer,
           ForeignKey('player.id', ondelete='CASCADE'))
    Column('game_id',
           Integer,
           ForeignKey('game.id', ondelete='CASCADE'))
)

player = Table(
    'player', meta,

    Column('id', Integer, primary_key=True),
    Column('name', String(200), nullable=False),
)

# history of all games and the players tied to those games.  
# Will store current score for each player in the game.
# useful for retrieving game statistics.
gameplayerinformation= Table(
    'gameplayerinformation', meta,

    Column('id', Integer, primary_key=True),
    Column('score', String(200), nullable=False),
    Column('move_type', String(10), nullable=False),
    Column('game_id',
           Integer,
           ForeignKey('game.id', ondelete='CASCADE'))
    Column('player_id',
           Integer,
           ForeignKey('player.id', ondelete='CASCADE'))
)

async def init_pg(app):
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