import logging
import json
import webapp2

from google.appengine.ext import ndb

class GuildMember(ndb.Model):
  # TODO: Track last modified, who modified and when added?
  # TODO: Add a unique identifier (needed for ACL)?
  firstName = ndb.StringProperty()
  lastName = ndb.StringProperty()
  # TODO: We probably don't need to index all those properties.
  address = ndb.StringProperty()
  tel = ndb.StringProperty()
  email = ndb.StringProperty()

  @classmethod
  def save(cls, jsonString):
    parsedJSON = json.loads(jsonString)
    firstName = parsedJSON["firstName"]
    lastName = parsedJSON["lastName"]
    member = GuildMember(
      firstName = firstName,
      lastName = lastName,
      address = parsedJSON["address"],
      tel = parsedJSON["tel"],
      email = parsedJSON["email"]
    )
    member.put()

  @classmethod
  def getAll(cls):
    allMembers = cls.query().fetch()
    result = '{"members": ['
    for member in allMembers:
      # TODO: This should use json.dumps instead of custom code.
      logging.info(member)

      result += '{"firstName": "' + member.firstName + '", '
      result += '"lastName": "' + member.lastName + '", '
      # TODO TODO TODO: Address can have carriage return, for now we horribly cheat.
      #result += '"address": "' + member.tel + '", '
      result += '"tel": "' + member.tel + '", '
      result += '"email": "' + member.email + '"}, '
    # TODO: Gross to remove the last 2 chars.
    result = result[:-2]
    result += ']}'
    return result

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.write(open("add.html").read());

  def post(self):
    logging.info(self.request.body)
    # TODO: We can have collisions here, we should probably handle them.
    GuildMember.save(self.request.body);
    self.response.write("Saved")


class GetAll(webapp2.RequestHandler):
  def get(self):
    self.response.write(GuildMember.getAll())

app = webapp2.WSGIApplication([
  ('/add', MainPage),
  ('/getall', GetAll),
], debug=True)