# init_db.py
# this file heavily based on https://github.com/aio-libs/aiohttp-demos/blob/master/demos/polls/init_db.py
# sets up a user and test database
import asyncio
from sqlalchemy import create_engine, MetaData
from tictactoe.settings import config
from tictactoe.db import game, player, gameplayerinformation, moves
from tictactoe.db import init_pg


DSN = "postgresql://davidlloyd:aiohttpdemo_pass@localhost:5432/aiohttp_rest_tictactoe"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[game, player, gameplayerinformation, moves])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(game.insert(), [
        {'name': 'testName',
         'status': 'NEW'}
    ])
    conn.close()

def drop_tables(engine):
    meta = MetaData()
    meta.drop_all(bind=engine, tables=[game, player, gameplayerinformation, moves])

def drop_and_rebuild(engine):
    drop_tables(engine)
    create_tables(engine)

def setup():
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)
    drop_and_rebuild(engine)
    # create_tables(engine)
    #sample_data(engine)

if __name__ == '__main__':
    setup()

