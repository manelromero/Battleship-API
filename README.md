#Battleship game API project
##Game Description:
Battleship game is played on two grids, one for each player. The grid size is 10×10 cells and the individual squares in the grid are identified by letter and number (e.g. 'B6').

Each player arranges their ships on his grid. Each ship occupies a number of consecutive squares on the grid, arranged either horizontally or vertically. The number of squares for each ship is determined by the type of the ship. The ships cannot overlap (i.e., only one ship can occupy any given square in the grid). The types and numbers of ships allowed are the same for each player.

The default number of ships for each player is one aircraft carrier(5 cells long), one battleship(4), one cruiser(3), two destroyers(2) and two submarines(1). This ships can be changed in the `new_board` method of the `Board` class.

After the ships have been positioned, the game proceeds in a series of rounds. In each round, each player takes a turn to announce a target square in the opponent's grid which is to be shot at. The opponent announces whether or not the square is occupied by a ship, and if it is a "miss", the player marks their primary grid with a white peg; if a "hit" they mark this on their own primary grid with a red peg. The attacking player notes the hit or miss on their own "tracking" grid with the appropriate color peg (red for "hit", white for "miss"), in order to build up a picture of the opponent's fleet.

When all of the squares of a ship have been hit, the ship is sunk, and the ship's owner announces this (e.g. "You sank my battleship!"). If all of a player's ships have been sunk, the game is over and their opponent wins.

##Files Included:
- **app.yaml**: App configuration.
- **cron.yaml**: Cron job configuration.
- **index.yaml**: Entities configuration.
- **main.py**: Handler for cron job.
- **models.py**: Entity and message definitions including helper methods.
- **forms.py**: Forms definitions.
- **api.py**: Contains endpoints and game playing logic.
- **utils.py**: Helper function for retrieving ndb.Models by urlsafe Key string.
- **API.py**: Information about API use for developers.
- **README.md**: Information file you are reading just now.

##Endpoints Included:
- **create_user**
 - Path: 'user'
 - Method: POST
 - Parameters: user.name, email
 - Returns: Message confirming creation of the User.
 - Description: Creates a new User. user_name provided must be unique. Will raise a ConflictException if a User with that user_name already exists.
        
- **create_game**
 - Path: 'game'
 - Method: POST
 - Parameters: user1_name, user2_name
 - Returns: GameForm with initial game state.
 - Description: Creates a new Game, creating also two boards, one for each user. User names provide must correspond to an existing user, will raise a NotFoundException if not.

- **get_game_history**
 - Path: 'game/history/{game_key}'
 - Method: GET
 - Parameters: game_key
 - Returns: BoardForms with every shot fired so far in the game.
 - Description: Gets information about history shots fired for both players in the game.

- **cancel_game**
 - Path: 'game/cancel/{game_key}'
 - Method: POST
 - Parameters: game_key
 - Returns: Message confirming game cancellation.
 - Description: Cancels any ongoing game.

- **shoot**
 - Path: 'shoot'
 - Method: POST
 - Parameters: game, coordinates
 - Returns: ShotForm with information about the shot.
 - Description: Stores a shot in the board history, checks if the game is over and returns information about the cell hit.

- **get_user_games**
 - Path: 'user/games/{user_name}'
 - Method: GET
 - Parameters: user_name
 - Returns: GameForms with every game for the given player.
 - Description: Gets all the games for a given player. Will raise a NotFounException if the user name does not exist.

- **get_user_rankings**
 - Path: 'get_high_scores'
 - Method: GET
 - Parameters: None
 - Returns: ScoreForms with all the users ranking.
 - Description: Returns all users ordered by victories.

##Models Included:
- **User**
 - Stores unique user_name and (optional) email address.
- **Board**
 - Stores unique boards, automatically generated for using in games. Associated with User model via KeyProperty. Contains `board`, a list of lists with cells information, `ships` with the amount of cells remaining to hit and `history` with all shots fired to the board so far.
- **Game**
 - Stores unique games, automatically generated. Associated with User model via KeyProperty both `user1` and `user2` and with Board both `board1` and `board2`. Contains `turn` to rotate the turn betweeen players and `game_over` to check if game has been finished.

##Forms Included:
- **NewUserForm**
 - Representation of a Game's state (urlsafe_key, attempts_remaining,
    game_over flag, message, user_name).
- **NewGameForm**
 - Used to create a new game (user_name, min, max, attempts)
- **NewShotForm**
 - Inbound make move form (guess).
- **GameForm**
 - Representation of a completed game's Score (user_name, date, won flag,
    guesses).
- **GameForms**
 - Multiple ScoreForm container.
- **BoardForm**
 - General purpose String container.
- **BoardForms**
 - General purpose String container.
- **ShotForm**
 - General purpose String container.
- **ScoreForm**
 - General purpose String container.
- **ScoreForms**
 - General purpose String container.
- **StringMessage**
 - General purpose String container.