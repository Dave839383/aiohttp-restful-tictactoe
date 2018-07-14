# aiohttp-restful-tictactoe
a game of tic tac toe using a RESTFul aiohttp based server

To create a game you can make a POST request to /game.  
Send { game_name : <a_name> }

To create a player for that game you can make a POST request to /game/{game_name}/player
Send { player_name : <a_name> }

To make a move in a game send a POST request to /game/{game_name}/player/{player_name}/move
