from google.appengine.ext import ndb
from protorpc import messages


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()


class Board(ndb.Model):
    """Board for the game"""
    user = ndb.KeyProperty(required=True, kind='User')
    board = ndb.JsonProperty(required=True)

    @classmethod
    def new_board(cls, user):
        """Creates and returns a new board"""
        # Generate the empty board
        new_board = []
        for row in xrange(0, 10):
            new_board.append([0] * 10)
        # Add battleships
        # add_ship(5)
        # add_ship(4)
        # add_ship(3)
        # add_ship(2)
        # add_ship(2)
        # add_ship(1)
        # add_ship(1)
        board = Board(user=user, board=new_board)
        board.put()
        return board

    def add_ship(self, ship_length):
        success = False
        while not success:
            # Horizontal or vertical?
            horizontal = True if randint(0, 1) == 0 else False
            # Start cell
            row = randint(0, 9) if horizontal else randint(0, 5)
            column = randint(0, 5) if horizontal else randint(0, 9)
            # Check free space for the ship
            free_space = True
            for length in xrange(-1, ship_length + 1):
                for width in xrange(-1, 2):
                    if horizontal:
                        try:
                            value = board[row + width][column + length]
                            if value == 1:
                                free_space = False
                        except IndexError:
                            pass
                    else:
                        try:
                            value = board[row + length][column + width]
                            if value == 1:
                                free_space = False
                        except IndexError:
                            pass
            # If there is free space, place the ship
            if free_space:
                board[row][column] = 1
                for l in xrange(1, ship_length):
                    if horizontal:
                        board[row][column + l] = 1
                    else:
                        board[row + l][column] = 1
                # success is now True so while loop stops
                success = True
        return board


class Game(ndb.Model):
    """Game"""
    user1 = ndb.KeyProperty(required=True, kind='User')
    user2 = ndb.KeyProperty(required=True, kind='User')
    board1 = ndb.KeyProperty(required=True, kind='Board')
    board2 = ndb.KeyProperty(required=True, kind='Board')
    game_over = ndb.BooleanProperty(required=True, default=False)

    @classmethod
    def new_game(cls, user1, user2, board1, board2):
        """Creates and returns a new game"""
        game = Game(user1=user1, user2=user2, board1=board1, board2=board2)
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        print self.board1.get().board
        form = GameForm()
        # form.urlsafe_key = self.key.urlsafe()
        form.user1_name = self.user1.get().name
        form.user2_name = self.user2.get().name
        # form.board1 = self.board1.get().board
        # form.board2 = self.board2.get().board
        form.message = message
        return form


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    user1_name = messages.StringField(1, required=True)
    user2_name = messages.StringField(2, required=True)
    # board1 = messages.StringField(3, required=True)
    # board2 = messages.StringField(4, required=True)
    message = messages.StringField(5, required=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    user1_name = messages.StringField(1, required=True)
    user2_name = messages.StringField(2, required=True)
    autoboard1 = messages.BooleanField(3, required=True)
    autoboard2 = messages.BooleanField(4, required=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
