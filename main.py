import logging
import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = open('index.html').read()
        self.response.write(template)

app = webapp2.WSGIApplication([
  ('/', MainPage),
], debug=True)
