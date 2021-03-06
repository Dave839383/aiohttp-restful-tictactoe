from views import index, game, add_player_to_game, make_move, show_game_board, show_or_insert_players


def setup_routes(app):
    app.router.add_get('/', index)

    # GET: gets ids of all running games
    # POST: post { 'new_game': <name> } to create game.
    app.router.add_view('/game', game, name='game')

    # POST : { 'player_name': <name> } to create player for the game
    app.router.add_view('/game/{game_name}/player', add_player_to_game,
                        name='add_player_to_game')

    # POST : { 'square': <square_number> } square
    # sqaure is a number from 1 to 9.
    app.router.add_post('/game/{game_name}/player/{player_name}/move',
                        make_move, name='make_move')

    # GET: shows the game current game board
    app.router.add_get('/game/{game_name}/board', show_game_board,
                       name='show_game_board')

    # GET: shows all players
    # POST: { 'player_name': <name> } to create player.
    app.router.add_view('/player', show_or_insert_players,
                       name='show_or_insert_players')
