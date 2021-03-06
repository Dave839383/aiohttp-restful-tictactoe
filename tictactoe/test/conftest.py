import os, sys
sys.path.append('tictactoe')

import pytest
from main import init_app
from init_db import setup

@pytest.fixture
async def cli(loop, test_client):
    app = init_app()
    return await test_client(app)


@pytest.fixture
def tables_and_data():
    #create_tables()
    #sample_data()
    setup()