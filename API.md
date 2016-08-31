# Battleship API

## Introduction to battleship API

### Overview
This API adds a new way to play the famous game **Battleship**.  Using a few HTTP calls in your Front End code, you will be able to store users, games and provide a lot of fun in your application.

### Target audience
Any developer willing to code this game focusing only on the client side.

### Installation
The battleship API is working [here](https://apis-explorer.appspot.com/apis-explorer/?base=https://battleship-api.appspot.com/_ah/api#p/battleship/1.0/) for testing, but you can download all the files needed from [here](https://github.com/manelromero/Battleship-API).
You will also need to install [Google App Engine](https://cloud.google.com/appengine/downloads).

## API reference

### `create_user`
#### Description
Creates a new user. Requires a unique user name.
#### Request URL
`POST http://localhost:8080/_ah/api/battleship/1.0/user/create`
#### Request body
- user_name
- email (optional)

Example:
```
{
 "user_name": "Frank",
 "email": "frank@test.com"
}
```
#### Response
Example:
```
{
 "message": "User Frank created!"
}
```

### `create_game`
#### Description
Creates a new game. Checks if both users provided exist. Creates both boards, randomly places all the ships and decides the player turn.
#### Request URL
`POST http://localhost:8080/_ah/api/battleship/1.0/game/create`
#### Request body
- user1_name
- user2_name

Example:
```
{
 "user1_name": "Julia",
 "user2_name": "Frank"
}
```
#### Response
The response includes the both players board configuration represented by a list of 10 lists, each of them represents a row in the grid and any value represents a cell following the next rule:

- 0, empty cell
- 1, empty cell after hit
- 2, ship cell
- 3, ship cell after hit

Example:
```
{
 "board1": "[[2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 2, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 2, 0, 0, 0, 0, 0], [0, 2, 0, 0, 2, 0, 2, 2, 0, 0], [0, 2, 0, 0, 2, 0, 0, 0, 0, 0], [0, 2, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]",
 "board2": "[[0, 0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 2, 2, 0, 0], [2, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 2, 0, 2, 0, 2, 0, 0, 0], [0, 0, 0, 0, 2, 0, 2, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2]]",
 "game_over": false,
 "key": "ahJkZXZ-YmF0dGxlc2hpcC1hcGlyEQsSBEdhbWUYgICAgIDQ-wgM",
 "turn": "Julia"
}
```

### `get_game_history`
#### Description
Gets the shot history of a given game.
#### Request URL
`GET http://localhost:8080/_ah/api/battleship/1.0/game/history?game_key=<game_key>`
#### Response
You can check both boards history and how many ship cells are pending to hit in `ships`.

Example:
```
{
 "message": "[{\"Date\": 1472662123.974824, \"Result\": \"miss\", \"Coordinates\": \"A4\", \"User\": \"Frank\"}, {\"Date\": 1472662136.605685, \"Result\": \"miss\", \"Coordinates\": \"B7\", \"User\": \"Julia\"}, {\"Date\": 1472662142.349353, \"Result\": \"miss\", \"Coordinates\": \"B7\", \"User\": \"Frank\"}, [\"C5\", \"hit\"], [\"C6\", \"hit\"], [\"C7\", \"hit\"], [\"C8\", \"sunk\"]]"
}
```

### `delete_game`
#### Description
Deletes a game in progress.
#### Request URL
`POST http://localhost:8080/_ah/api/battleship/1.0/game/delete?game_key=<game_key>`
#### Response
Example:
```
{
 "message": "Game deleted"
}
```

### `shoot`
#### Description
Fires a shot. Checks if the game exists and is not over, if the coordinates are correct and returns the result of the shot.
#### Request URL
`POST http://localhost:8080/_ah/api/battleship/1.0/game/shoot`
#### Request body
- game
- coordinates

Example
```
{
 "game": <game_key>,
 "coordinates": "B3"
}
```
#### Response
There are four possible **result** responses:

- **miss**, when an empty cell is hit. The turn changes to the other player.
- **hit**, when a ship's cell is hit but there are others cells of the same ship that have not been hit yet. The turn does not change until the player shots a 'miss' or finishes the game.
- **sunk**, when a cell is the last of a ship. The turn does not change until the player shots a 'miss' or finishes the game.
- **shot**, when the cell was already hit before. The turn does not change. Is the same player's turn until a valid cell is shot.

Example:
```
{
 "game_over": false,
 "next_turn": "Frank",
 "opponent_board": "[[1, 0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 2, 2, 0, 0, 0, 2, 0, 2], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0], [2, 2, 2, 0, 2, 0, 0, 2, 0, 0], [0, 0, 0, 0, 2, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 2, 2, 2], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]]",
 "result": "miss",
 "user_board": "[[3, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 0, 1, 0, 0, 0, 0, 0, 2, 0], [3, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 0, 0, 0, 0, 0, 0, 1, 0, 2], [0, 0, 0, 2, 2, 2, 2, 0, 0, 2], [0, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 2, 2, 2, 0, 0, 0, 0, 0]]"
}
```

### `get_user_games`
#### Description
Returns all active games for a given user.
#### Request URL
`GET http://localhost:8080/_ah/api/battleship/1.0/user/get_games?user_name=<user_name>`
#### Response
Example:
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

### `get_user_rankings`
#### Description
Returns a leader board of all users ordered by victories.
#### Request URL
`GET http://localhost:8080/_ah/api/battleship/1.0/user/get_user_rankings`
#### Response
Example:
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
