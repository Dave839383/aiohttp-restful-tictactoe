import pytest
from tictactoe.main import init_app
from init_db import (
    create_tables,
    sample_data,
)


@pytest.fixture
async def cli(loop, test_client):
    app = init_app()
    return await test_client(app)


@pytest.fixture
def tables_and_data():
    create_tables()
    sample_data()