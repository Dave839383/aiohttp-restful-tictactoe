from aiohttp import web
from settings import config
from routes import setup_routes
from db import init_pg, close_pg


def init_app():
	app = web.Application()
	setup_routes(app)
	app['config'] = config

	conf = app['config']['postgres']

	# For making DB queries we need an engine instance.
	app.on_startup.append(init_pg)

	# graceful shutdown of database
	app.on_cleanup.append(close_pg)
	print(config)
	return app
	

def main():
	app = init_app()
	web.run_app(app)

if __name__ == '__main__':
    main()