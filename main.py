#!/usr/bin/env python

import webapp2
# from api import BattleshipApi
# from models import User


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Battleship game')


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
