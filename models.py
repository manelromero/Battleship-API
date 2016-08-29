# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
from random import randint, choice
from forms import GameForm, BoardForm, ShotForm, ScoreForm
import json
import time


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    victories = ndb.IntegerProperty(default=0)
    email = ndb.StringProperty()

    def get_user_games(self):
        """Gets all user's games"""
        user_games = Game.query(ndb.OR(
            Game.user1 == self.key, Game.user2 == self.key)
            )
        return user_games

    def to_form(self):
        """Returns a ScoreForm representation of the user"""
        form = ScoreForm()
        form.user_name = self.name
        form.victories = self.victories
        return form


class Board(ndb.Model):
    """Board for the game"""
    user = ndb.KeyProperty(required=True, kind='User')
    board = ndb.JsonProperty(required=True)
    ships = ndb.IntegerProperty(default=0)
    history = ndb.JsonProperty(default=[])

    @classmethod
    def new_board(cls, user):
        """Creates and returns a new board"""
        empty_board = []
        for row in xrange(0, 10):
            empty_board.append([0] * 10)
        board = Board(user=user, board=empty_board)
        # Add ships (modify list for different ships)
        board.add_ships([5, 4, 3, 2, 2, 1, 1])
        board.put()
        return board

    def cancel_board(self):
        """Cancels a game in progress"""
        self.key.delete()
        return

    def to_form(self):
        """Returns a BoardForm representation of the Board"""
        form = BoardForm()
        form.user = User.query(User.key == self.user).get().name
        form.history = json.dumps(self.history)
        form.ships = str(self.ships)
        return form

    def add_ships(self, ships):
        """Ramdonly adds ships to an existing board"""
        for ship, ship_length in enumerate(ships):
            success = False
            while not success:
                # Horizontal(hz) or vertical?
                hz = choice([True, False])
                # Start cell
                row = randint(0, 9 * hz + (10 - ship_length) * (not hz))
                col = randint(0, 9 * (not hz) + (10 - ship_length) * hz)
                # Check free space around the ship placement
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
                                    # For index greater than 10
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
                                    # For index greater than 10
                                    pass
                # Place the ship
                if free_space:
                    for l in xrange(0, ship_length):
                        if hz:
                            self.board[row][col + l] = 2
                        else:
                            self.board[row + l][col] = 2
                    # Increase board.ships by ship_length
                    self.ships += ship_length
                    self.put()
                    # success is now True so while loop stops
                    success = True
        return self

    def shoot(self, game, coordinates):
        """Returns the result of a shot"""
        if game.game_over:
            raise endpoints.ConflictException('Game is already over')
        form = ShotForm()
        x = ord(coordinates[0]) - 65
        y = int(coordinates[1:]) - 1
        # Check given coordinates are right
        if 0 <= x <= 9 and 0 <= y <= 9:
            cell = self.board[x][y]
            # Miss
            if cell == 0:
                form.message = 'miss'
                self.board[x][y] += 1
                self.history.append([coordinates, form.message])
                self.put()
                game.turn += 1
                game.put()
            # Cell already shot
            if cell == 1 or cell == 3:
                form.message = 'shot'
            # Hit
            if cell == 2:
                form.message = self.check_hit(x, y)
                self.ships -= 1
                self.board[x][y] += 1
                self.history.append([coordinates, form.message])
                self.put()
                # Check if all ships are sunk
                if self.ships == 0:
                    game.finish_game()
        # Given coordinates are not right
        else:
            form.message = 'Bad coordinates'
        # Return the updated board
        form.board = json.dumps(self.board)
        print self.layout()
        return form

    def check_hit(self, x, y):
        """Checks if a hit sinks a ship"""
        sunk = True
        # Check up
        ship = True
        while ship:
            i = -1
            while i > -10:
                if x + i >= 0:
                    value = self.board[x + i][y]
                    if value == 2:
                        sunk = False
                    elif value == 0 or value == 1:
                        ship = False
                        break
                else:
                    ship = False
                i -= 1
        # Check down
        ship = True
        while ship:
            i = 1
            while i < 10:
                try:
                    value = self.board[x + i][y]
                except:
                    ship = False
                    break
                if value == 2:
                    sunk = False
                elif value == 0 or value == 1:
                    ship = False
                    break
                i += 1
        # Check left
        ship = True
        while ship:
            i = -1
            while i > -10:
                if y + i >= 0:
                    value = self.board[x][y + i]
                    if value == 2:
                        sunk = False
                    elif value == 0 or value == 1:
                        ship = False
                        break
                else:
                    ship = False
                i -= 1
        # Check right
        ship = True
        while ship:
            i = 1
            while i > -10:
                try:
                    value = self.board[x][y + i]
                except:
                    ship = False
                    break
                if value == 2:
                    sunk = False
                elif value == 0 or value == 1:
                    ship = False
                    break
                i += 1
        message = 'sunk' if sunk else 'hit'
        return message

    def layout(self):
        """Returns board layout (for debug)"""
        user = User.query(User.key == self.user).get()
        options = {0: '   │', 1: ' x │', 2: ' ☐ │', 3: ' ⊠ │'}
        board = '\nBoard of ' + str(user.name)
        board += '\n   1   2   3   4   5   6   7   8   9   10\n'
        board += ' ┌─' + '──┬─' * 9 + '──┐\n'
        for x in xrange(0, 10):
            board += chr(x + 65) + '│'
            for y in xrange(0, 10):
                value = self.board[x][y]
                board += options[value]
            if x < 9:
                board += '\n ├─' + '──┼─' * 9 + '──┤\n'
            else:
                board += '\n └─' + '──┴─' * 9 + '──┘\n'
        return board


class Game(ndb.Model):
    """Game"""
    user1 = ndb.KeyProperty(required=True, kind='User')
    user2 = ndb.KeyProperty(required=True, kind='User')
    board1 = ndb.KeyProperty(required=True, kind='Board')
    board2 = ndb.KeyProperty(required=True, kind='Board')
    turn = ndb.IntegerProperty()
    game_over = ndb.BooleanProperty(default=False)

    @classmethod
    def new_game(cls, user1, user2, board1, board2):
        """Creates and returns a new game"""
        turn = randint(0, 1)
        game = Game(
            user1=user1,
            user2=user2,
            board1=board1,
            board2=board2,
            turn=turn
            )
        game.put()
        return game

    def cancel_game(self):
        """Cancels a game in progress"""
        self.key.delete()
        return

    def finish_game(self):
        """Finishes a game and updates the score"""
        self.game_over = True
        self.put()
        if self.turn % 2 == 0:
            winner = User.query(User.key == self.user2).get()
        else:
            winner = User.query(User.key == self.user1).get()
        winner.victories += 1
        winner.put()
        return

    def to_form(self):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.key = self.key.urlsafe()
        form.board1 = json.dumps(self.board1.get().board)
        form.board2 = json.dumps(self.board2.get().board)
        if self.turn % 2 == 0:
            form.turn = User.query(User.key == self.user2).get().name
        else:
            form.turn = User.query(User.key == self.user1).get().name
        form.game_over = self.game_over
        return form
