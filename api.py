# -*- coding: utf-8 -*-
"""api.py"""

import endpoints
from protorpc import remote, messages
from random import randint
from models import User, Game
from models import StringMessage, NewGameForm, GameForm


USER_REQUEST = endpoints.ResourceContainer(
    user_name=messages.StringField(1),
    email=messages.StringField(2)
    )
NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)

@endpoints.api(name='battleship', version='1.0')
class BattleshipApi(remote.Service):
    """Game API"""
    # Endpoint from the Skeleton Project Guess-a-Number
    @endpoints.method(
        request_message=USER_REQUEST,
        response_message=StringMessage,
        path='user',
        name='create_user',
        http_method='POST'
        )
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                'A User with that name already exists!'
                )
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(
            message='User {} created!'.format(request.user_name)
            )

    @endpoints.method(
        request_message=NEW_GAME_REQUEST,
        response_message=GameForm,
        path='game',
        name='new_game',
        http_method='POST'
        )
    def new_game(self, request):
        """Creates new game"""
        user1 = User.query(User.name == request.user1_name).get()
        user2 = User.query(User.name == request.user2_name).get()
        if not user1:
            raise endpoints.NotFoundException(
                "User {} doesn't exist".format(request.user1_name)
                )
        if not user2:
            raise endpoints.NotFoundException(
                "User {} doesn't exist".format(request.user2_name)
                )
        try:
            game = Game.new_game(user1.key, user2.key)
        except ValueError:
            raise endpoints.BadRequestException('Something went wrong')
        return game.to_form('Good luck playing battleship')

    @endpoints.method(
        response_message=StringMessage,
        path='board',
        name='new_board',
        http_method='GET'
        )
    def new_board(self, request):
        """Generates all the positions"""
        board = []
        positions = []
        success = 0
        while success < 100:
            already_in_board = False
            letter = randint(1,10)
            number = randint(1,10)
            for element in board:
                if letter == element[0] and number == element[1]:
                    already_in_board = True
            if already_in_board == False:
                board.append([letter, number])
                positions.append(chr(64 + letter) + str(number))
                success += 1
        return StringMessage(message=positions)


api = endpoints.api_server([BattleshipApi])
