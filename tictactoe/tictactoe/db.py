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
)

player = Table(
    'player', meta,

    Column('id', Integer, primary_key=True),
    Column('name', String(200), nullable=False),

    Column('game_id',
           Integer,
           ForeignKey('game.id', ondelete='CASCADE'))
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