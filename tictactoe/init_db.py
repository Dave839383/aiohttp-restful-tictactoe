# init_db.py
from sqlalchemy import create_engine, MetaData

from tictactoe.settings import config
from tictactoe.db import game, player
from tictactoe.db import init_pg


DSN = "postgresql://{name}}:{password}@localhost:5432/{dbname}"

def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[game, player])

'''
def sample_data(engine):
    conn = engine.connect()
    conn.execute(game.insert(), [
        {'question_text': 'What\'s new?',
         'pub_date': '2015-12-15 17:17:49.629+02'}
    ])
    conn.execute(player.insert(), [
        {'choice_text': 'Not much', 'votes': 0, 'question_id': 1},
        {'choice_text': 'The sky', 'votes': 0, 'question_id': 1},
        {'choice_text': 'Just hacking again', 'votes': 0, 'question_id': 1},
    ])
    conn.close()
'''

if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    #sample_data(engine)