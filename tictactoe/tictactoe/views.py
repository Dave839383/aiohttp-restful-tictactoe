from aiohttp import web
from psycopg2 import IntegrityError
import db


async def index(request):
    # async with request.app['db'].acquire() as conn:
    return web.Response(text='Lets play tic tac toe')


# inserts a new game into the game table
# throws IntegrityError if game already exists with this name
async def game(request):

    data = await request.post()
    try:
        game_name = data['name']

        async with request.app['db'].acquire() as conn:
            await conn.execute(db.game.insert().values(name=game_name, 
                                                        status='NEW'))
        
    except (KeyError, TypeError, ValueError) as e:
        raise web.HTTPBadRequest(text='You have not specified a game name') from e
    except(IntegrityError):
        raise web.HTTPNotAcceptable(text="a game called "+ game_name+ " already exists.")

    return web.Response(text='New Game: '+game_name+' has been created')


# /game/{game_name}/player
async def add_player_to_game(request):

    try:

        game_name = request.match_info['game_name']
        player_name = ''

        # the GET request retrieves all players for the game_name
        if request.method == 'GET':

            # select all the players in game_name
            s = db.gameplayerinformation.select().where(db.player.c.name 
                                                        == game_name)
            async with request.app['db'].acquire() as conn:
                cursor = await conn.execute(s)
                records = cursor.fetchall()
                return web.Response(text='players in game are: ')

        # the POST request inserts a new player for the game_name
        elif request.method == 'POST':

            data = await request.post()
            player_name = data['player_name']
            move_type = ''

            # check if player has been added to player table
            # if not we'll add it
            s = db.player.select().where(db.player.c.name == player_name)

            async with request.app['db'].acquire() as conn:
                # get the number of players in the game already
                num_players = db.gameplayerinformation.select().where(db.gameplayerinformation.c.game_name == game_name)
                cursor = await conn.execute(num_players)
                num_players = cursor.rowcount

                # tic tac toe can only have 2 players
                if num_players >= 2:
                    return web.Response(text='this game already has 2 players')

                cursor = await conn.execute(s)
                row_count = cursor.rowcount

                # add player to player table if it doesn't exist
                if row_count is 0:
                    await conn.execute(db.player.insert().values(name=player_name))
                # if no players exist, this player is assigned crosses
                if num_players is 0:
                    await conn.execute(db.gameplayerinformation.insert().values(move_type='X',
                                                                                     game_name=game_name,
                                                                                     player_name=player_name))
                    move_type = 'crosses'
                # if we're here num_players must be 1 
                else:
                    # we cannot add the same player to the same game
                    cursor = await conn.execute(db.gameplayerinformation.select().where(db.gameplayerinformation.c.game_name==game_name))
                    result = await cursor.fetchone()
                    current_player = result['player_name']

                    if (player_name == current_player):
                        return web.Response(text='the game must have two different players')

                    else:
                        await conn.execute(db.gameplayerinformation.insert().values(move_type='O',
                                                                                 game_name=game_name,
                                                                                 player_name=player_name))

                        move_type = 'noughts'

                return web.Response(text='new player: '+ player_name + ' has been added to game: '+ game_name + ' and is using '+ move_type)

    except (KeyError, TypeError, ValueError) as e:
        print(e)
        raise web.HTTPBadRequest(text='You have not specified a game or player name') from e
    
    except(IntegrityError) as e:
        print(e)
        raise web.HTTPNotAcceptable(text="The game does not exist or the player POST data is incorrect")
    
    return web.Response(text='Wrong request type')


# /game/{game_id}/player/{player_id}/move
async def make_move(request):
    # same checks as add_player_to_game, put in a function
    # CHECK if game_id is in game table - IF NOT THROW EXCEPTION
    # CHECK if game_id status is finished or game_id num_players 
    # is greater than 2 - IF YES THROW EXCEPTION.

    # CHECK if player exists in Player table, if not EXCEPTION
    # CHECK if player is part of this game in gameplayerinformation table, 
    # if not throw exception.

    # CHECK move post data was added in correct format.
    # CHECK move number is between 1 and 9

    # CHECK if no moves have been made in gameplayerinformation table,
    # if none, randomise and add a nought or cross to the player 
    # in gameplayerinformation,
    # INSERT move to moves table.
    # return you made a move with a cross to _____
    return web.Response(text='making a move')


# /game/{game_id}/show
async def show_game_board(request):
    # SELECT * FROM moves WHERE game_id = game_id
    return web.Response(text='Showing game board')

async def show_or_insert_players(request):
    return web.Response(text='Showing or insert players')


