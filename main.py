#!/usr/bin/env python

import webapp2
from google.appengine.api import mail, app_identity
from models import User, Game


class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each User with an email about games.
        Called every hour using a cron job"""
        app_id = app_identity.get_application_id()
        users = self.get_users()
        for user in users:
            subject = 'Game reminder'
            body = 'Hello {}, you have an unfinished game!'.format(user.name)
            # This will send test emails, the arguments to send_mail are:
            # from, to, subject, body
            mail.send_mail(
                'noreply@{}.appspotmail.com'.format(app_id),
                user.email,
                subject,
                body
                )

    def get_users(self):
        """Get users with unfinished games and email for reminder"""
        users = []
        games = Game.query(Game.game_over == False).fetch()
        for game in games:
            user1 = User.query(User.key == game.user1).get()
            user2 = User.query(User.key == game.user2).get()
            if user1.email:
                users.append(user1)
            if user2.email:
                users.append(user2)
        return users


app = webapp2.WSGIApplication([
    ('/crons/send_reminder', SendReminderEmail)
], debug=True)
