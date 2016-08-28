# -*- coding: utf-8 -*-


import endpoints
from protorpc import remote, messages
from random import randint
from models import User, Board, Score, Game
from forms import StringMessage, NewUserForm, NewGameForm, BoardForm,\
    BoardForms, GameForm, GameForms, NewShotForm, ShotForm
from utils import get_by_urlsafe


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
        """Create a new user, requires a unique username"""
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
        """Creates a new game"""
        # Check if users exist
        user1 = User.query(User.name == request.user1_name).get()
        if not user1:
            raise endpoints.NotFoundException(
                "User {} doesn't exist".format(request.user1_name)
                )
        user2 = User.query(User.name == request.user2_name).get()
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
        return game.to_form()

    @endpoints.method(
        request_message=endpoints.ResourceContainer(NewShotForm),
        response_message=ShotForm,
        path='board',
        name='shot',
        http_method='POST'
        )
    def shot(self, request):
        """Fires a shot"""
        game = get_by_urlsafe(request.game, Game)
        turn = game.turn % 2
        if turn == 0:
            board = game.board1.get()
        else:
            board = game.board2.get()
        return board.shot(game, request.coordinates)

    @endpoints.method(
        request_message=endpoints.ResourceContainer(
            user_name=messages.StringField(1)
            ),
        response_message=GameForms,
        path='user/games/{user_name}',
        name='get_user_games',
        http_method='GET'
        )
    def get_user_games(self, request):
        """Returns all user's active games"""
        user = User.query(User.name == request.user_name).get()
        user_games = user.get_user_games()
        return GameForms(games=[game.to_form() for game in user_games])

    @endpoints.method(
        request_message=endpoints.ResourceContainer(
            game_key=messages.StringField(1)
            ),
        response_message=StringMessage,
        path='game/cancel/{game_key}',
        name='cancel_game',
        http_method='POST'
        )
    def cancel_game(self, request):
        """Cancels a game in progress"""
        game = get_by_urlsafe(request.game_key, Game)
        board1 = Board.query(Board.key == game.board1).get()
        board2 = Board.query(Board.key == game.board2).get()
        game.cancel_game()
        board1.cancel_board()
        board2.cancel_board()
        return StringMessage(message='Game canceled')

    @endpoints.method(
        request_message=endpoints.ResourceContainer(),
        response_message=StringMessage,
        path='get_high_scores',
        name='get_high_scores',
        http_method='GET'
        )
    def get_high_scores():
        """Returns a leader-board"""

    @endpoints.method(
        request_message=endpoints.ResourceContainer(
            game_key=messages.StringField(1)
            ),
        response_message=BoardForms,
        path='game/history/{game_key}',
        name='get_game_history',
        http_method='GET'
        )
    def get_game_history(self, request):
        """Returns a game movement's history"""
        game = get_by_urlsafe(request.game_key, Game)
        boards = []
        board1 = Board.query(Board.key == game.board1).get()
        board2 = Board.query(Board.key == game.board2).get()
        boards += [board1, board2]
        return BoardForms(boards=[board.to_form() for board in boards])


api = endpoints.api_server([BattleshipApi])
