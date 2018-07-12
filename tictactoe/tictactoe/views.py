from aiohttp import web

async def index(request):
	#async with request.app['db'].acquire() as conn:
	print(request)
	return web.Response(text='Lets play tic tac toe!')

async def game(request):
	#async with request.app['db'].acquire() as conn:
	#game_id = request.match_info['game_id']
	data = await request.post()
	try:
		game_id = data['game_id']
		# also if game_id already exists in db, raise exception
		
	except (KeyError, TypeError, ValueError) as e:
		raise web.HTTPBadRequest(text='You have not specified a game name') from e
	return web.Response(text='Game!')

# /game/{game_id}
async def create_game(request):
	# async with request.app['db'].acquire() as conn:
	# game_id = request.match_info['game_id']

	return web.Response(text='create game!')

# /game/{game_id}/player
async def add_player_to_game(request):
	return web.Response(text='adding player to game')

# /game/{game_id}/player/{player_id}/move
async def make_move(request):
	return web.Response(text='making a move')

# /game/{game_id}/show
async def show_game_board(request):
	return web.Response(text='Showing game board')