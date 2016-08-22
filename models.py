from google.appengine.ext import ndb
from protorpc import messages
from random import randint, choice
import json


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()


class Board(ndb.Model):
    """Board for the game"""
    user = ndb.KeyProperty(required=True, kind='User')
    board = ndb.JsonProperty(required=True)

    @classmethod
    def empty_board(cls, user):
        """Creates and returns an empty board"""
        empty_board = []
        for row in xrange(0, 10):
            empty_board.append([0] * 10)
        board = Board(user=user, board=empty_board)
        board.put()
        return board

    def auto_board(self):
        """Randomly create ships in a board"""
        self.add_ship(5)
        self.add_ship(4)
        self.add_ship(3)
        self.add_ship(2)
        self.add_ship(2)
        self.add_ship(1)
        self.add_ship(1)
        self.put()
        return self

    def add_ship(self, ship_length):
        """Adds a ship to an existing board"""
        success = False
        while not success:
            # Horizontal(hz) or vertical?
            hz = choice([True, False])
            # Start cell
            row = randint(0, 9 * hz + (10 - ship_length) * (not hz))
            col = randint(0, 9 * (not hz) + (10 - ship_length) * hz)
            # If there is free space, place the ship
            free_space = self.check_cell(row, col, hz, ship_length)
            if free_space:
                for l in xrange(0, ship_length):
                    if hz:
                        self.board[row][col + l] = 2
                    else:
                        self.board[row + l][col] = 2
                self.put()
                # success is now True so while loop stops
                success = True
        return self


    def check_cell(self, row, col, hz, ship_length):
        """Checks space around a cell"""
        free_space = True
        for l in xrange(-1, ship_length + 1):
            for w in xrange(-1, 2):
                if hz:
                    # Check if the chosen position is in the first col
                    # In this case x[-1] = x[9] and we don't want that
                    if col + l >= 0:
                        try:
                            value = self.board[row + w][col + l]
                            if value > 0:
                                free_space = False
                        except IndexError:
                            # Index 10 doesn't exist, it's ok not to check
                            pass
                else:
                    # Check if the chosen position is in the first col
                    # In this case x[-1] = x[9] and we don't want that
                    if col + w >= 0:
                        try:
                            value = self.board[row + l][col + w]
                            if value > 0:
                                free_space = False
                        except IndexError:
                            # Index 10 doesn't exist, it's ok not to check
                            pass
        return free_space



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
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user1_name = self.user1.get().name
        form.user2_name = self.user2.get().name
        form.board1 = json.dumps(self.board1.get().board)
        form.board2 = json.dumps(self.board2.get().board)
        form.message = message
        print '\n'
        print form.board1
        print '\n'
        print form.board2
        print '\n'
        return form

    def shot(self, board, coordinates):
        """Returns the result of a shot"""
        form = ShotForm()
        x = ord(coordinates[0]) - 65
        y = int(coordinates[1:]) - 1
        # Check given coordinates are right
        if 0 <= x <= 9 and 0 <= y <= 9:
            cell = board.board[x][y]
            # Miss
            if cell == 0:
                form.message = 'miss'
                board.board[x][y] += 1
                board.put()
            # Hit
            if cell == 2:
                form.message = 'hit'
                # Check if ship it's been sunk
                sunk = True
                up = -1 if y > 0 else 0
                down = 2 if y < 9 else 1
                left = -1 if x > 0 else 0
                right = 2 if x < 9 else 1
                for width in xrange(left, right):
                    for height in xrange(up, down):
                        value = board.board[x + width][y + height]
                        if value == 2 and (width != 0 or height != 0):
                            sunk = False
                        if value == 3:
                            pass
                if sunk:
                    form.message = 'sunk'
                board.board[x][y] += 1
                board.put()
            # Cell already shot
            if cell == 1 or cell == 3:
                form.message = 'shot'
        # Coordinates were not correct
        else:
            form.message = 'Bad coordinates'
        # Return the updated board
        form.board = json.dumps(board.board)
        return form


class NewUserForm(messages.Message):
    """To create a new user"""
    user_name = messages.StringField(1, required=True)
    email = messages.StringField(2)


class NewGameForm(messages.Message):
    """To create a new game"""
    user1_name = messages.StringField(1, required=True)
    user2_name = messages.StringField(2, required=True)
    autoboard1 = messages.BooleanField(3, required=True)
    autoboard2 = messages.BooleanField(4, required=True)


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    user1_name = messages.StringField(2, required=True)
    user2_name = messages.StringField(3, required=True)
    board1 = messages.StringField(4, required=True)
    board2 = messages.StringField(5, required=True)
    message = messages.StringField(6, required=True)


class NewShotForm(messages.Message):
    """To create a shot"""
    game = messages.StringField(1, required=True)
    board = messages.StringField(2, required=True)
    coordinates = messages.StringField(3, required=True)


class ShotForm(messages.Message):
    message = messages.StringField(1, required=True)
    board = messages.StringField(2, required=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
