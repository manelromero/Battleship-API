# -*- coding: utf-8 -*-
"""api.py"""

import endpoints
from protorpc import remote, message_types
from random import randint
from models import StringMessage



@endpoints.api(name='battleship', version='v1')
class BattleshipApi(remote.Service):
	"""Game API"""
	@endpoints.method(
		response_message=StringMessage,
		path='board',
		name='positions',
		http_method='GET'
		)
	def positions(self, request):
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
