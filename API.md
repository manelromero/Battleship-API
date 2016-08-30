#Battleship API
##Introduction to battleship API
###Overview
This API adds a new way to play the famous game **Battleship**.  Using a few HTTP calls in your Front End code, you will be able to store users, games and provide a lot of fun in your application.
###Target audience
Any developer willing to code this game focusing only on the client side.
###Installation
The battleship API is working [here](https://apis-explorer.appspot.com/apis-explorer/?base=https://battleship-api.appspot.com/_ah/api#p/battleship/1.0/) for testing, but you can download all the files needed from [here](https://github.com/manelromero/Battleship-API).
You will also need to install [Google App Engine](https://cloud.google.com/appengine/downloads).
##API reference
###`create_user`
####Description
Creates a new user. Requires a unique user name.
####Request URL
`POST http://localhost:8080/_ah/api/battleship/1.0/user`
####Request body
- user_name
- email (optional)

```
{
 "user_name": "Frank",
 "email": "frank@test.com"
}
```

####Response

```
{
 "message": "User Frank created!"
}
```

###`create_game`
####Description
Creates a new game. Checks if both users provided exist. Creates both boards, randomly places all the ships and decides the player turn.
####Request URL
`POST http://localhost:8080/_ah/api/battleship/1.0/game`
####Request body
- user1_name
- user2_name

```
{
 "user1_name": "Julia",
 "user2_name": "Frank"
}
```

####Response
The response includes the both players board configuration represented by a list of 10 lists, each of them represents a row in the grid and any value represents a cell following the next rule:

- 0, empty cell
- 1, empty cell after hit
- 2, ship cell
- 3, ship cell after hit

```
{
 "board1": "[[2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 2, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 2, 0, 0, 0, 0, 0], [0, 2, 0, 0, 2, 0, 2, 2, 0, 0], [0, 2, 0, 0, 2, 0, 0, 0, 0, 0], [0, 2, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]",
 "board2": "[[0, 0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 2, 2, 0, 0], [2, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 2, 0, 2, 0, 2, 0, 0, 0], [0, 0, 0, 0, 2, 0, 2, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2]]",
 "game_over": false,
 "key": "ahJkZXZ-YmF0dGxlc2hpcC1hcGlyEQsSBEdhbWUYgICAgIDQ-wgM",
 "turn": "Julia"
}
```

###`get_game_history`
####Description
Gets the shot history of a given game.
####Request URL
`GET http://localhost:8080/_ah/api/battleship/1.0/game/history/<game_key>`
####Response
You can check both boards history and how many ship cells are pending to hit in `ships`.

```
{
 "boards": [
  {
   "history": "[[\"A5\", \"miss\"], [\"J3\", \"miss\"], [\"C8\", \"miss\"], [\"A1\", \"sunk\"], [\"A9\", \"miss\"], [\"H6\", \"miss\"], [\"F5\", \"hit\"], [\"F6\", \"miss\"]]",
   "ships": "16",
   "user": "Julia"
  },
  {
   "history": "[[\"F2\", \"miss\"], [\"C4\", \"miss\"], [\"B2\", \"miss\"], [\"G3\", \"miss\"], [\"D2\", \"miss\"]]",
   "ships": "18",
   "user": "Frank"
  }
 ]
}
```

###`cancel_game`
####Description
Cancels a game in progress.
####Request URL
`POST http://localhost:8080/_ah/api/battleship/1.0/game/cancel/<game_key>`
####Response

```
{
 "message": "Game canceled"
}
```

###`shoot`
####Description
Fires a shot. Checks if the game exists and is not over, if the coordinates are correct and returns the result of the shot.
####Request URL
`POST http://localhost:8080/_ah/api/battleship/1.0/shoot`
####Request body
- game
- coordinates

```
{
 "game": <game_key>,
 "coordinates": "B3"
}
```

####Response
There are four possible responses:

- **miss**, when an empty cell is hit. The turn changes to the other player.
- **hit**, when a cell that is part of a ship is hit but there are others cells of the same ship that has not been hit yet. The turn does not change until the player shots a 'miss' or finishes the game.
- **sunk**, when a cell is the last of a ship. The turn does not change until the player shots a 'miss' or finishes the game.
- **shot**, when the cell was already hit before. The turn does not change. Is the same player turn until a valid cell is shot.

```

{
 "message": "miss"
}
```

###`get_user_games`
####Description
Returns all active games for a given user.
####Request URL
`GET http://localhost:8080/_ah/api/battleship/1.0/user/games/<user>`
####Response

```
{
 "games": [
  {
   "board1": "[[1, 0, 3, 3, 3, 0, 0, 0, 2, 0], [1, 0, 0, 0, 0, 0, 0, 0, 2, 0], [0, 2, 0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 2, 2, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 0], [2, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]",
   "board2": "[[0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 0, 0, 2, 2, 2, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0, 2], [0, 2, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 2, 0, 0, 0, 0, 0, 0, 0, 2], [0, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 2, 2, 0, 0, 0]]",
   "game_over": false,
   "key": "ahJkZXZ-YmF0dGxlc2hpcC1hcGlyEQsSBEdhbWUYgICAgIDArwsM",
   "turn": "Frank"
  }
 ]
}
```

###`get_user_rankings`
####Description
Returns a leader board of all users.
####Request URL
`GET http://localhost:8080/_ah/api/battleship/1.0/get_user_rankings`
####Response

```
{
 "user": [
  {
   "user_name": "Julia",
   "victories": "5"
  },
  {
   "user_name": "Frank",
   "victories": "3"
  },
  {
   "user_name": "Sara",
   "victories": "2"
  }
 ]
}
```
