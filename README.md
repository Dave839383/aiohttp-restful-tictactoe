# aiohttp-restful-tictactoe
a game of tic tac toe using a RESTFul aiohttp based server
The server currently doesn't have a UI set up, but a user can access the endpoints through
the requests library etc (see example below).

### SOME QUICK START TIPS

#### launch the server
```
  $ python3 tictactoe/main.py
```

#### create a database
```
  $ python3 init_db.py
```

#### run the test suite
```
pytest test/test.py
```

### TO PLAY THE GAME

#### create a game
make a POST request to ```/game```.  Send:
```
{ 'name' : <a_name> }
```
A game has status NEW if there are no players, IN PROGRESS if players have been added, and FINISHED if there
has been a winner or all squares have been filled.  Statuses of all games can be checked by sending a GET request to /game.

#### create a player for that game

make a POST request to ```/game/{game_name}/player```. Send:
```
{ 'player_name' : <a_name> }
```
The first player to be added to a game is automatically assigned crosses, and is also assigned as the player who needs to make the first move.

#### make a move in the game
make a POST request to ```/game/{game_name}/player/{player_name}/move```. Send:
```
{ 'square' : <a_number> }
```
Each square needs to be a number from 1 to 9, with each number representing a square in the following grid:

1 2 3\
4 5 6\
7 8 9

#### show all games and their status
make a GET request to ```/game```.

#### show all players in db
make a GET request to ```/player```.

#### show a current game board
make a GET request to ```/game/{game_name}/board```.
```
{ 'name' : <a_name> }
```

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

>>> print(requests.get('http://localhost/game/anewgame/board').text)

X O O 
  X   

>>> requests.post('http://localhost/game/anewgame/player/Dave/move', {'square': '9'}).text
'Congratulations Dave.  You won the game.'
```

### THINGS TO NOTE

Server is currently setup to connect to a postgres database
Update database name, password and host in config/tictactoe.yaml to connect to a postgres database on your computer.

All endpoints for POST and GET requests are in routes.py and are well commented so you should be able to figure out how they work.  The views that are connected to these routes are well commented also.

At the moment calling init_db.py to build the database drops all tables in the current database and rebuilds the database.
Calling test.py also drops the tables in this database and then rebuilds.  An update needs to be made to create a test database.

You can stop init_db.py from dropping the database by commenting out the dropandrebuild() function.


