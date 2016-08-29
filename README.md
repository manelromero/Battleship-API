#Battleship game API project
##Game Description:
Battleship game is played on two grids, one for each player. The grid size is 10×10 cells and the individual squares in the grid are identified by letter and number.

Before play begins, each player secretly arranges their ships on their primary grid. Each ship occupies a number of consecutive squares on the grid, arranged either horizontally or vertically. The number of squares for each ship is determined by the type of the ship. The ships cannot overlap (i.e., only one ship can occupy any given square in the grid). The types and numbers of ships allowed are the same for each player.

The default number of ships for each player is one aircraft carrier(5 cells long), one battleship(4), one cruiser(3), two destroyers(2) and two submarines(1). This ships can be changed in the ´new_board´ method of the ´Board´ class.

After the ships have been positioned, the game proceeds in a series of rounds. In each round, each player takes a turn to announce a target square in the opponent's grid which is to be shot at. The opponent announces whether or not the square is occupied by a ship, and if it is a "miss", the player marks their primary grid with a white peg; if a "hit" they mark this on their own primary grid with a red peg. The attacking player notes the hit or miss on their own "tracking" grid with the appropriate color peg (red for "hit", white for "miss"), in order to build up a picture of the opponent's fleet.
When all of the squares of a ship have been hit, the ship is sunk, and the ship's owner announces this (e.g. "You sank my battleship!"). If all of a player's ships have been sunk, the game is over and their opponent wins.

'Guesses' are sent to the `make_move` endpoint which will reply with either: 'too low', 'too high', 'you win', or 'game over' (if the maximum number of attempts is reached).
Many different Guess a Number games can be played by many different Users at any given time. Each game can be retrieved or played by using the path parameter `urlsafe_game_key`.

##Files Included:
- **app.yaml**: App configuration.
- **main.py**: Handler for taskqueue handler.
- **models.py**: Entity and message definitions including helper methods.
- **forms.py**: Forms definitions.
- **api.py**: Contains endpoints and game playing logic.
- **cron.yaml**: Cronjob configuration.
- **utils.py**: Helper function for retrieving ndb.Models by urlsafe Key string.

##Endpoints Included:
- **create_user**
 - Path: 'user'
 - Method: POST
 - Parameters: user1_name, user2_name, autoboard1, autoboard2
 - Returns: Message confirming creation of the User.
 - Description: Creates a new User. user_name provided must be unique. Will 
    raise a ConflictException if a User with that user_name already exists.
        
- **create_game**
 - Path: 'game'
 - Method: POST
 - Parameters: user_name, min, max, attempts
 - Returns: GameForm with initial game state.
 - Description: Creates a new Game. user_name provided must correspond to an
    existing user - will raise a NotFoundException if not. Min must be less than
    max. Also adds a task to a task queue to update the average moves remaining
    for active games.

- **get_game_history**
 - Path: 'game/history/{game_key}'
 - Method: GET
 - Parameters: game_key
 - Returns: StringMessage
 - Description: Gets the average number of attempts remaining for all games
    from a previously cached memcache key.

- **cancel_game**
 - Path: 'game/cancel/{game_key}'
 - Method: POST
 - Parameters: game_key
 - Returns: ScoreForms.
 - Description: Returns all Scores in the database (unordered).

- **shoot**
 - Path: 'shoot'
 - Method: POST
 - Parameters: game, coordinates
 - Returns: GameForm with current game state.
 - Description: Returns the current state of a game.

- **get_user_games**
 - Path: 'user/games/{user_name}'
 - Method: GET
 - Parameters: user_name
 - Returns: GameForm with new game state.
 - Description: Accepts a 'guess' and returns the updated state of the game.
    If this causes a game to end, a corresponding Score entity will be created.

- **get_high_scores**
 - Path: 'get_high_scores'
 - Method: GET
 - Parameters: None
 - Returns: ScoreForms. 
 - Description: Returns all Scores recorded by the provided player (unordered).
    Will raise a NotFoundException if the User does not exist.

##Models Included:
- **User**
 - Stores unique user_name and (optional) email address.
- **Board**
 - Stores unique game states. Associated with User model via KeyProperty.
- **Game**
 - Stores... 

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