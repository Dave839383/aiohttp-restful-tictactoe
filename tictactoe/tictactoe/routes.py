from views import index, game, add_player_to_game, make_move, show_game_board
# app.router.add_post('/poll/{question_id}/vote', vote, name='vote')

def setup_routes(app):
    app.router.add_get('/', index)

    # GET: gets ids of all running games
    # POST: post { 'new_game': <name> } to create game.
    app.router.add_view('/game', game, name='game')

    # GET : 'get players in game'
    # POST : { 'player_name': <name> } to create player.
    app.router.add_view('/game/{game_id}/player', add_player_to_game, name='add_player_game')

    # POST : { 'square': <square_number> } square number is a number from 1 to 9.
    app.router.add_post('/game/{game_id}/player/{player_id}/move', make_move, name='make_move')
    
    # GET: shows the game current game board
    app.router.add_get('/game/{game_id}/show', show_game_board, name='show_game_board')
