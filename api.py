# -*- coding: utf-8 -*-

from protorpc import remote, messages
from models import User, Board, Game
from forms import (
    NewUserForm,
    NewGameForm,
    NewShotForm,
    ShotForm,
    GameForm,
    GameForms,
    BoardForms,
    ScoreForms,
    StringMessage)
from utils import get_by_urlsafe
import endpoints
import json


@endpoints.api(name='battleship', version='1.0')
class BattleshipApi(remote.Service):
    """Game API"""
    # Endpoint from the Skeleton Project Guess-a-Number
    @endpoints.method(
        request_message=endpoints.ResourceContainer(NewUserForm),
        response_message=StringMessage,
        path='user/create',
        name='create_user',
        http_method='POST')
    def create_user(self, request):
        """Creates a new user, requires a unique user name"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(
            message='User {} created!'.format(request.user_name))

    @endpoints.method(
        request_message=endpoints.ResourceContainer(NewGameForm),
        response_message=GameForm,
        path='game/create',
        name='create_game',
        http_method='POST')
    def create_game(self, request):
        """Creates a new game"""
        # Check if users exist
        user1 = User.query(User.name == request.user1_name).get()
        if not user1:
            raise endpoints.NotFoundException(
                "User {} doesn't exist".format(request.user1_name))
        user2 = User.query(User.name == request.user2_name).get()
        if not user2:
            raise endpoints.NotFoundException(
                "User {} doesn't exist".format(request.user2_name))
        # Check if both users are the same
        if user1 == user2:
            raise endpoints.NotFoundException("Two different users needed")
        # Create boards
        board1 = Board.new_board(user1.key)
        board2 = Board.new_board(user2.key)
        # Generate new game
        game = Game.new_game(user1.key, user2.key, board1.key, board2.key)
        return game.to_form()

    @endpoints.method(
        request_message=endpoints.ResourceContainer(
            game_key=messages.StringField(1, required=True)),
        response_message=StringMessage,
        path='game/history',
        name='get_game_history',
        http_method='GET')
    def get_game_history(self, request):
        """Returns a game shot history"""
        game = get_by_urlsafe(request.game_key, Game)
        # Check if game exists
        if not game:
            raise endpoints.NotFoundException("Game doesn't exist")
        # Create a list with both boards
        history = json.dumps(game.history)
        return StringMessage(message=history)

    @endpoints.method(
        request_message=endpoints.ResourceContainer(
            game_key=messages.StringField(1, required=True)),
        response_message=StringMessage,
        path='game/delete',
        name='delete_game',
        http_method='POST')
    def delete_game(self, request):
        """Deletes a game in progress"""
        # Get game and boards
        game = get_by_urlsafe(request.game_key, Game)
        # Check if game exists
        if not game:
            raise endpoints.NotFoundException("Game doesn't exist")
        # Check if game is over
        if game.game_over:
            raise endpoints.ConflictException(
                'The game you are trying to delete is over')
        board1 = Board.query(Board.key == game.board1).get()
        board2 = Board.query(Board.key == game.board2).get()
        # Delete them all
        game.delete_game()
        board1.delete_board()
        board2.delete_board()
        return StringMessage(message='Game deleted')

    @endpoints.method(
        request_message=endpoints.ResourceContainer(NewShotForm),
        response_message=ShotForm,
        path='game/shoot',
        name='shoot',
        http_method='POST')
    def shoot(self, request):
        """Fires a shot"""
        game = get_by_urlsafe(request.game, Game)
        # Check if game exists
        if not game:
            raise endpoints.NotFoundException("Game doesn't exist")
        # Check if game is already over
        if game.game_over:
            raise endpoints.ConflictException('Game is already over')
        # Check given coordinates are right
        x = ord(request.coordinates[0]) - 65
        y = int(request.coordinates[1:]) - 1
        if 0 <= x <= 9 and 0 <= y <= 9:
            # Find out whose turn is
            turn = game.turn % 2
            if turn == 0:
                board = game.board1.get()
            else:
                board = game.board2.get()
            return board.shoot(game, x, y)
        # Given coordinates are not right
        else:
            raise endpoints.ConflictException('Bad coordinates')

    @endpoints.method(
        request_message=endpoints.ResourceContainer(
            user_name=messages.StringField(1, required=True)),
        response_message=GameForms,
        path='user/get_games',
        name='get_user_games',
        http_method='GET')
    def get_user_games(self, request):
        """Returns all user's active games"""
        user = User.query(User.name == request.user_name).get()
        # Check if user exists
        if not user:
            raise endpoints.NotFoundException("User doesn't exist")
        user_games = user.get_user_games()
        return GameForms(games=[game.to_form() for game in user_games])

    @endpoints.method(
        request_message=endpoints.ResourceContainer(),
        response_message=ScoreForms,
        path='user/get_user_rankings',
        name='get_user_rankings',
        http_method='GET')
    def get_user_rankings(self, request):
        """Returns a leader-board"""
        # Get all users
        users = User.query()
        # Order them by victories
        users.order(User.victories).fetch()
        return ScoreForms(user=[user.to_form() for user in users])


api = endpoints.api_server([BattleshipApi])
