import google.oauth2.id_token
import logging
import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
      try:
        # TODO: Once I have validated this code, I should probably
        # move under a single try...except.
        authorization = self.request.headers['Authorization']
      except:
        self.response.write(open('authentication.html').read())
        return

      id_token = authorization.split(' ').pop()
      claims = google.oauth2.id_token.verify_firebase_token(
      id_token, HTTP_REQUEST)
      if not claims:
        #self.response.write(open('authentication.html').read())
        return 'Unauthorized', 401

      # Authenticated user
      template = open('index.html').read()
      self.response.write(template)

app = webapp2.WSGIApplication([
  ('/', MainPage),
], debug=True)
