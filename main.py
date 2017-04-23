import logging
import webapp2

from authentication import *

class MainPage(webapp2.RequestHandler):
    def get(self):
      email = Authentication.GetUserEmail(self.request)
      if email is None:
        self.response.write(open('authentication.html').read())
        return

      # Authenticated user
      template = open('index.html').read()
      self.response.write(template)

class GoogleLogin(webapp2.RequestHandler):
  def get(self):
    # This page has login: required, which forces to
    # authenticate using the user API.
    # TODO: We are missing the original page URL here
    # and always redirect to the homepage. Propagate
    # this information here if it makes sense.
    self.redirect('/')

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/glogin', GoogleLogin),
], debug=True)
