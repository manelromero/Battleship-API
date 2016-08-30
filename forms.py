# -*- coding: utf-8 -*-

from protorpc import messages


class NewUserForm(messages.Message):
    """Form to create a new user"""
    user_name = messages.StringField(1, required=True)
    email = messages.StringField(2)


class NewGameForm(messages.Message):
    """Form to create a new game"""
    user1_name = messages.StringField(1, required=True)
    user2_name = messages.StringField(2, required=True)


class NewShotForm(messages.Message):
    """Form to create a new shot"""
    game = messages.StringField(1, required=True)
    coordinates = messages.StringField(3, required=True)


class GameForm(messages.Message):
    """Form for outbound game state information"""
    key = messages.StringField(1, required=True)
    board1 = messages.StringField(2, required=True)
    board2 = messages.StringField(3, required=True)
    turn = messages.StringField(4, required=True)
    game_over = messages.BooleanField(5, required=True)


class GameForms(messages.Message):
    """Form for multiple GameForm"""
    games = messages.MessageField(GameForm, 1, repeated=True)


class BoardForm(messages.Message):
    """Form for outbound board state information"""
    user = messages.StringField(1, required=True)
    history = messages.StringField(2, required=True)
    ships = messages.StringField(3, required=True)


class BoardForms(messages.Message):
    """Form for multiple BoardForm"""
    boards = messages.MessageField(BoardForm, 1, repeated=True)


class BoardStateForm(messages.Message):
    """Form for outbound board hits information"""
    board = messages.StringField(1, required=True)


class ScoreForm(messages.Message):
    """Form for outbound board state information"""
    user_name = messages.StringField(1, required=True)
    victories = messages.IntegerField(2, required=True)


class ScoreForms(messages.Message):
    """Form for multiple ScoreForm"""
    user = messages.MessageField(ScoreForm, 1, repeated=True)


class StringMessage(messages.Message):
    """Form for outbound (single) string message"""
    message = messages.StringField(1, required=True)
