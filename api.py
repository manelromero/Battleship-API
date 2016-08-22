# -*- coding: utf-8 -*-
"""api.py"""

import endpoints
from protorpc import remote, messages
from random import randint
from models import User, Board, Game
from models import StringMessage, NewUserForm, NewGameForm, GameForm


@endpoints.api(name='battleship', version='1.0')
class BattleshipApi(remote.Service):
    """Game API"""
    # Endpoint from the Skeleton Project Guess-a-Number
    @endpoints.method(
        request_message=endpoints.ResourceContainer(NewUserForm),
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
        request_message=endpoints.ResourceContainer(NewGameForm),
        response_message=GameForm,
        path='game',
        name='create_game',
        http_method='POST'
        )
    def create_game(self, request):
        """Creates new game"""
        user1 = User.query(User.name == request.user1_name).get()
        user2 = User.query(User.name == request.user2_name).get()
        # Check if users exist
        if not user1:
            raise endpoints.NotFoundException(
                "User {} doesn't exist".format(request.user1_name)
                )
        if not user2:
            raise endpoints.NotFoundException(
                "User {} doesn't exist".format(request.user2_name)
                )
        board1 = Board.empty_board(user1.key)
        board2 = Board.empty_board(user2.key)
        # Check if we need to generate automatic boards
        if request.autoboard1:
            board1.auto_board()
        if request.autoboard2:
            board2.auto_board()
        # Generate new game
        try:
            game = Game.new_game(user1.key, user2.key, board1.key, board2.key)
        except ValueError:
            raise endpoints.BadRequestException('Something went wrong')
        return game.to_form('Game created')





    @endpoints.method(
        response_message=StringMessage,
        path='fire',
        name='fire',
        http_method='GET'
        )
    def fire(self, request):
        """Generates all the positions"""


api = endpoints.api_server([BattleshipApi])
