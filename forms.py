# -*- coding: utf-8 -*-

from protorpc import messages


class NewUserForm(messages.Message):
    """To create a new user"""
    user_name = messages.StringField(1, required=True)
    email = messages.StringField(2)


class NewGameForm(messages.Message):
    """To create a new game"""
    user1_name = messages.StringField(1, required=True)
    user2_name = messages.StringField(2, required=True)
    autoboard1 = messages.BooleanField(3, default=False)
    autoboard2 = messages.BooleanField(4, default=False)


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    board1 = messages.StringField(2, required=True)
    board2 = messages.StringField(3, required=True)
    turn = messages.StringField(4, required=True)


class GameForms(messages.Message):
    """Return multiple GameForms"""
    items = messages.MessageField(GameForm, 1, repeated=True)


class BoardForm(messages.Message):
    """BoardForm for outbound board state information"""
    user = messages.StringField(1, required=True)
    history = messages.StringField(2, required=True)


class BoardForms(messages.Message):
    """Return multiple BoardForms"""
    boards = messages.MessageField(BoardForm, 1, repeated=True)


class NewShotForm(messages.Message):
    """To create a shot"""
    game = messages.StringField(1, required=True)
    coordinates = messages.StringField(3, required=True)


class ShotForm(messages.Message):
    message = messages.StringField(1, required=True)
    board = messages.StringField(2, required=True)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    guesses = messages.IntegerField(4, required=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)