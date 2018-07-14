# aiohttp-restful-tictactoe
a game of tic tac toe using a RESTFul aiohttp based server

### SOME QUICK START TIPS

#### launch the server
```
  $ python3 main.py
```

#### create a database
```
  $ python3 init_db.py
```

#### run the test suite
```
pytest test.py
```

### TO PLAY THE GAME

#### create a game
make a POST request to ```/game```.  Send:
```
{ 'name' : <a_name> }
```

#### create a player for that game

make a POST request to ```/game/{game_name}/player```. Send:
```
{ 'player_name' : <a_name> }
```
The first player to be added to a game is automatically assigned crosses.

#### make a move in the game
make a POST request to ```/game/{game_name}/player/{player_name}/move```. Send:
```
{ 'square' : <a_number> }
```
Each square needs to be a number from 1 to 9, with each number representing a square in the following grid:

1 2 3
4 5 6
7 8 9

### PLAYING A FULL GAME WITH THE REQUESTS LIBRARY
```
>>> requests.post('http://localhost/game', {'name': 'anewgame'}).text
'New Game: anewgame has been created'

>>> requests.post('http://localhost/game/anewgame/player', {'player_name': 'Dave'}).text
'new player: Dave has been added to game: anewgame and is using crosses'

>>> requests.post('http://localhost/game/anewgame/player', {'player_name': 'John'}).text
'new player: John has been added to game: anewgame and is using noughts'

>>> requests.post('http:/localhost/game/anewgame/player/Dave/move', {'square': '1'}).text
'Dave moved an X to square 1'

>>> requests.post('http://localhost/game/anewgame/player/Jason/move', {'square': '2'}).text
'Player with name Jason is not playing this game'

>>> requests.post('http://localhost/game/anewgame/player/John/move', {'square': '2'}).text
'John moved an O to square 2'

>>> requests.post('http://localhost/game/anewgame/player/Dave/move', {'square': '1'}).text
'Square 1 has already been used'

>>> requests.post('http://localhost/game/anewgame/player/Dave/move', {'square': '5'}).text
'Dave moved an X to square 5'

>>> requests.post('http://localhost/game/anewgame/player/John/move', {'square': '3'}).text
'John moved an O to square 3'

>>> requests.post('http://localhost/game/anewgame/player/Dave/move', {'square': '9'}).text
'Congratulations Dave.  You won the game.'
```

### DOCUMENTATION

Needs to have a postgres database set up.
The code uses SQLAlchemy for queries, and aiopg as the connection wrapper for Psycopg

