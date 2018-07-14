from aiohttp import web
from psycopg2 import IntegrityError
from sqlalchemy import and_
from itertools import combinations
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
        raise web.HTTPBadRequest(
            text='You have not specified a game name') from e
    except(IntegrityError):
        raise web.HTTPNotAcceptable(
            text="a game called "+ game_name+ " already exists.")

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
                raise web.HTTPBadRequest(text='players in game are: ')

        # the POST request inserts a new player for the game_name
        elif request.method == 'POST':

            data = await request.post()
            player_name = data['player_name']
            move_type = ''

            async with request.app['db'].acquire() as conn:
                # get the number of players in the game already
                cursor = await conn.execute(
                    db.gameplayerinformation.select().where(
                    db.gameplayerinformation.c.game_name == game_name))
                get_players = await cursor.fetchone()
                num_players = cursor.rowcount

                # tic tac toe can only have 2 players
                if num_players >= 2:
                    raise web.HTTPBadRequest(text=
                        'this game already has 2 players')

                # check if player has been added to player table
                # if not we'll add it
                s = db.player.select().where(db.player.c.name == player_name)
                cursor = await conn.execute(s)
                row_count = cursor.rowcount

                # add player to player table if it doesn't exist
                if row_count is 0:
                    await conn.execute(db.player.insert().values(
                        name=player_name))
                # if no players exist, this player is assigned crosses
                if num_players is 0:
                    await conn.execute(
                        db.gameplayerinformation.insert().values(
                            move_type='X',
                            game_name=game_name,
                            player_name=player_name))
                    move_type = 'crosses'

                    # this player will start the game so make it
                    # their turn
                    await conn.execute(
                        db.game.update().where(
                            db.game.c.name==game_name).values(
                            next_turn=player_name))
                # if we're here num_players must be 1 
                else:
                    # we cannot add the same player to the same game
                    current_player = get_players['player_name']

                    if (player_name == current_player):
                        raise web.HTTPBadRequest(text=
                            'the game must have two different players')

                    else:
                        await conn.execute(
                            db.gameplayerinformation.insert().values(
                                move_type='O',
                                game_name=game_name,
                                player_name=player_name))

                        move_type = 'noughts'

                        # switch the game to IN PROGRESS so players
                        # can start making moves.
                        await conn.execute(
                            db.game.update().where(
                                db.game.c.name==game_name).values(
                                status='IN PROGRESS'))


                return web.Response(
                    text=
                    'new player: '+ player_name + ' has been added to game: '+ game_name + ' and is using '+ move_type)

    except (KeyError, TypeError, ValueError) as e:
        print(e)
        raise web.HTTPBadRequest(
            text='You have not specified a game or player name') from e
    
    except(IntegrityError) as e:
        print(e)
        raise web.HTTPNotAcceptable(
            text=
            "The game does not exist or the player POST data is incorrect")
    
    return web.Response(text='Wrong request type')


# /game/{game_name}/player/{player_name}/move
async def make_move(request):
    # https://stackoverflow.com/questions/2670217/detect-winning-game-in-nought-and-crosses
    # algorithm for finding winner assigns numbers to each square
    # so that all rows diagonals etc add to 15, if same X or O in any of 
    # these given rows or diagonals then we have a winner
    # User still enters numbers 1 to 9 for squares left to right,
    # top to bottom though so it isn't confusing for them
    # An index in this list is the user square, the number stored
    # at that index is the square used for calculating the winnder
    square_list = [4,3,8,9,5,1,2,7,6]

    game_name = request.match_info['game_name']
    player_name = request.match_info['player_name']
    move_square = ''

    data = await request.post()
    
    try:
        move_square = data['square']

    except (KeyError, TypeError, ValueError) as e:
        print(e)
        raise web.HTTPBadRequest(
            text='You have not requested a square correctly') from e
    
    # next two checks make sure square value is valid
    if not(RepresentsInt(move_square)):
        raise web.HTTPBadRequest(text='square must be a number')

    move_square = int(move_square)

    if move_square < 1 or move_square > 9:
        raise web.HTTPBadRequest(text='square must be between 1 and 9')

    async with request.app['db'].acquire() as conn:
        # game must be IN PROGRESS
        # this is initially set in the add_player_to_game view

        cursor = await conn.execute(
                        db.game.select().where(
                            db.game.c.name==game_name))

        result = await cursor.fetchone()
        game_status = result['status']
        next_turn = result['next_turn']

        if game_status != 'IN PROGRESS':
            raise web.HTTPBadRequest(
                text='To make a move the game must be in progress')

        # the player must be playing in this game
        cursor = await conn.execute(
                        db.gameplayerinformation.select().where(
                            db.gameplayerinformation.c.game_name==game_name))
        current_game = await cursor.fetchall()
        participants = [i[3] for i in current_game]

        if not(player_name in participants):
            raise web.HTTPBadRequest(
                text='Player with name '+ player_name + ' is not playing this game')
        
        # check if it's this players turn
        if next_turn != player_name:
            raise web.HTTPBadRequest(
                text='It is not this players turn')

        # cant move to same square twice
        cursor = await conn.execute(
                        db.moves.select().where(
                             db.moves.c.game_name==game_name))

        all_moves = await cursor.fetchall()
        all_squares = [i[1] for i in all_moves]

        if move_square in all_squares:
            raise web.HTTPBadRequest(
                text='Square '+ str(move_square) + ' has already been used')

        # insert the new move
        await conn.execute(
            db.moves.insert().values(
                square=move_square, move_type=current_game[0][1],
                game_name=game_name, player_name=player_name))

        # determine if there is a winner or all squares are filled
        # this gets all moves by the current player
        player_squares_list = [i[1] for i in all_moves if i[4] == player_name] 
        # add current move to the list
        player_squares_list.append(move_square)
        squares_for_sum = [square_list[i - 1] for i in player_squares_list]
        # check if a combination of squares add to 15
        awinner = subset_sum(squares_for_sum, 15)

        # update game status to FINISHED
        if awinner:
            await conn.execute(db.game.update().where(
                                db.game.c.name==game_name).values(
                                status='FINISHED'))
            return web.Response(text=
                'Congratulations '+ player_name+'.  You won the game.')

        # check if all squares have been filled
        # update status to FINISHED - NO WINNER
        if len(all_moves)+1 == 9:
            await conn.execute(db.game.update().where(
                                db.game.c.name==game_name).values(
                                status='FINISHED - NO WINNER'))
            return web.Response(text=
                'Game Over: No Winner, all squares filled')

        # if no winner and game is still going update whose turn it is
        next_player = [i for i in participants if i != player_name][0]

        await conn.execute(db.game.update().where(
                            db.game.c.name==game_name).values(
                            next_turn=next_player))

    return web.Response(text=player_name +' moved an '+current_game[0][1]
     + ' to square '+ str(move_square))


# /game/{game_name}/show 
async def show_game_board(request):
    # SELECT * FROM moves WHERE game_id = game_id
    return web.Response(text='Showing game board')


async def show_or_insert_players(request):
    return web.Response(text='Showing or insert players')

############ HELPFER FUNCTIONS ############

# helper function for determining if string is an int
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

# https://stackoverflow.com/questions/23501347/
# check-if-there-are-three-numbers-in-the-list-that-add-up-to-target
def subset_sum(lst, target):
    return len(lst) > 2 and any(sum(x) == target for x in combinations(lst, 3))

