from google.appengine.ext import ndb
from protorpc import messages


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()


class Game(ndb.Model):
    """Game"""
    user1 = ndb.KeyProperty(required=True, kind='User')
    user2 = ndb.KeyProperty(required=True, kind='User')
    # board1 = ndb.KeyProperty(required=True, kind='Board')
    # board2 = ndb.KeyProperty(required=True, kind='Board')
    # game_over = ndb.BooleanProperty(required=True, default=False)

    @classmethod
    def new_game(cls, user1, user2):
        """Creates and returns a new game"""
        game = Game(user1=user1, user2=user2)
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        # form.urlsafe_key = self.key.urlsafe()
        form.user1_name = self.user1.get().name
        form.user2_name = self.user2.get().name
        form.message = message
        return form


class Board(ndb.Model):
    """Board for the game"""


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    user1_name = messages.StringField(1, required=True)
    user2_name = messages.StringField(2, required=True)
    message = messages.StringField(3, required=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    user1_name = messages.StringField(1, required=True)
    user2_name = messages.StringField(2, required=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
