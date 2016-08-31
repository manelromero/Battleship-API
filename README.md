# Battleship game API project
For instructions about how to use this API [go here](https://github.com/manelromero/Battleship-API/blob/master/API.md).

## Game Description
Battleship game is played on two grids, one for each player. The grid size is 10×10 cells and the individual squares in the grid are identified by letter and number (e.g., 'B6').

Each gets a grid with the ships arranged. Each ship occupies a number of consecutive squares on the grid, arranged either horizontally or vertically. The number of squares for each ship is determined by the type of the ship. The ships cannot overlap (i.e., only one ship can occupy any given square in the grid). The types and numbers of ships allowed are the same for each player.

The default number of ships for each player is one aircraft carrier(5 cells long), one battleship(4), one cruiser(3), two destroyers(2) and two submarines(1).

After the ships have been positioned, the game proceeds in a series of rounds. In each round, each player takes a turn to announce a target square in the opponent's grid which is to be shot at. The opponent announces whether or not the square is occupied by a ship. The attacking player notes the hit or miss on their own "tracking" grid with the appropriate way in order to build up a picture of the opponent's fleet.

When all of the squares of a ship have been hit, the ship is sunk, and the ship's owner announces this (e.g., "You sank my battleship!"). If all of a player's ships have been sunk, the game is over and their opponent wins.

The player that has sunk all the opponent player's ships gets one vitory point. The number of victories of every player can be checked using the `get_user_rankings` endpoint.

## Files Included

- **app.yaml**: App configuration.
- **cron.yaml**: Cron job configuration.
- **index.yaml**: Entities configuration.
- **main.py**: Handler for cron job.
- **models.py**: Entities definitions including helper methods.
- **forms.py**: Forms definitions.
- **api.py**: Contains endpoints and game playing logic.
- **utils.py**: Helper function for retrieving ndb.Models by urlsafe Key string.
- **API.py**: Information about API use for developers.
- **README.md**: Information file you are reading just now.

## Endpoints Included

- #### create_user
    - Path: 'user/create'
    - Method: POST
    - Parameters: user_name, email
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will raise a ConflictException if a User with that user_name already exists.
        
- #### create_game
    - Path: 'game/create'
    - Method: POST
    - Parameters: user1_name, user2_name
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game, creating also two boards, one for each user. User names provide must correspond to an existing user, will raise a NotFoundException if not.

- #### get_game_history
    - Path: 'game/history'
    - Method: GET
    - Parameters: game_key
    - Returns: StringMessage with every shot fired so far in the game.
    - Description: Gets information about history shots fired in the game.

- #### delete_game
    - Path: 'game/delete'
    - Method: DELETE
    - Parameters: game_key
    - Returns: Message confirming game deletion.
    - Description: Deletes any ongoing game.

- #### shoot
    - Path: 'game/shoot'
    - Method: POST
    - Parameters: game, coordinates
    - Returns: ShotForm with the result of the shot and the state of the game.
    - Description: Stores a shot in the game history, checks if the game is over and returns information about the cell hit and the general state of the game.

- #### get_user_games
    - Path: 'user/get_games'
    - Method: GET
    - Parameters: user_name
    - Returns: GameForms with every game for the given player.
    - Description: Gets all the games for a given player. Will raise a NotFounException if the user name does not exist.

- #### get_user_rankings
    - Path: 'user/get_user_rankings'
    - Method: GET
    - Parameters: None
    - Returns: ScoreForms with all the users ranking.
    - Description: Returns all users ordered by victories.

## Models Included

- #### User

    Stores unique `user_name` and (optional) `email` address.
- #### Board

    Stores unique boards, automatically generated for using in games. Associated with User model via KeyProperty. Contains `board`, a list of lists with cells information and `ships` with the amount of cells remaining to hit.
- #### Game

    Stores unique games, automatically generated. Associated with User model via KeyProperty both `user1` and `user2` and with Board both `board1` and `board2`. Contains `turn` to rotate the turn betweeen players, `game_over` to check if game has been finished and `history` with all shots fired in the game.

## Forms Included

- #### NewUserForm

    Used to create a new user (user_name, email).

- #### NewGameForm

    Used to create a new game (user1_name, user2_name).

- #### NewShotForm

    Used to send a new shot (game, coordinates).

- #### ShotForm

    Representation of a shoot result (result, next_turn, opponent_board, user_board, game_over).

- #### GameForm

    Representation of a game state (key, board1, board2, turn, game_over).

- #### GameForms

    Multiple GameForm.

- #### BoardForm

    Representation of a board state (user, history, ships).

- #### BoardForms

    General BoardForm container.

- #### ScoreForm

    Representatoin of an user victories (user_name, victories).

- #### ScoreForms

    Multiple ScoreForm container.
    
- #### StringMessage

    General purpose String container.
