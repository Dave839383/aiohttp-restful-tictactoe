from aiohttp import web

async def index(request):
	#async with request.app['db'].acquire() as conn:
	print(request)
	return web.Response(text='Lets play tic tac toe!')

async def game(request):
	#async with request.app['db'].acquire() as conn:
	#game_id = request.match_info['game_id']
	# INSERT GameID into games table
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
	# CHECK if game_id is in game table - IF NOT THROW EXCEPTION
	# CHECK if game_id status is finished or game_id num_players is greater than 2 - IF YES THROW EXCEPTION.
	# CHECK if player exists in Player table, if not INSERT
	# CHECK gameplayerinformation table to see if player exists with game.  IF NOT INSERT.
	return web.Response(text='adding player to game')

# /game/{game_id}/player/{player_id}/move
async def make_move(request):
	# same checks as add_player_to_game, put in a function
	# CHECK if game_id is in game table - IF NOT THROW EXCEPTION
	# CHECK if game_id status is finished or game_id num_players is greater than 2 - IF YES THROW EXCEPTION.
	
	# CHECK if player exists in Player table, if not EXCEPTION
	# CHECK if player is part of this game in gameplayerinformation table, if not throw exception.

	# CHECK move post data was added in correct format.
	# CHECK move number is between 1 and 9

	# CHECK if no moves have been made in gameplayerinformation table, 
	# if none, randomise and add a nought or cross to the player in gameplayerinformation,
	# INSERT move to moves table.
	# CHECK 
	# return you made a move with a cross to _____
	return web.Response(text='making a move')

# /game/{game_id}/show
async def show_game_board(request):
	# SELECT * FROM moves WHERE game_id = game_id
	return web.Response(text='Showing game board')