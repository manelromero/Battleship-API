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
###create_user
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

###create_game
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

###get_game_history
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
   "user": "manel"
  },
  {
   "history": "[[\"F2\", \"miss\"], [\"C4\", \"miss\"], [\"B2\", \"miss\"], [\"G3\", \"miss\"], [\"D2\", \"miss\"]]",
   "ships": "18",
   "user": "xavi"
  }
 ]
}
```

###cancel_game
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

###shoot
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

###get_user_games
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

###get_user_rankings
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
