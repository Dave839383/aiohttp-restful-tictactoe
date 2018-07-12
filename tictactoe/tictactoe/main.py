from aiohttp import web
from settings import config
from routes import setup_routes
from db import init_pg

async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()

app = web.Application()
setup_routes(app)
app['config'] = config

# For making DB queries we need an engine instance.
app.on_startup.append(init_pg)

# graceful shutdown of database
app.on_cleanup.append(close_pg)
print(config)
web.run_app(app)