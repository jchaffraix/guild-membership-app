# This file contains all the authentication related backend functions.

import hashlib
import logging

from google.appengine.api import users
import google.oauth2.id_token

# TODO: This really needs some testing as this is core to the app.

class Authentication:
  # TODO: Big hack, need to wire that to our database once I have the model down.
  known_users = set(
    ["9f927a92a4ace305922ba459ed36c4381784ff03d86c8f291417b9413c97c206",
     "afafa1e6b03387a3d53228a001285ad521031bc362b5297054e101fe47e5276a"])

  # Returns the authenticated user or None if the user is not authenticated.
  @staticmethod
  def GetUserEmail(request):
    # First check if the user is signed in with Google.
    user = users.get_current_user()
    if user:
      return user.email()

    # Fallback to Firebase's email based system.
    try:
      # TODO: Once I have validated this code, I should probably
      # move under a single try...except.
      authorization = request.headers['Authorization']
    except:
      return None

    id_token = authorization.split(' ').pop()
    # That is probably wrong.
    HTTP_REQUEST = request
    claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST)
    if not claims:
      return None
    return claims.get('email', None)

  # TODO: We should move to a role-based model where we allow
  # certain users to see some data read-only and some just their
  # own data.
  @staticmethod
  def CanUserSeeData(request):
      # Sanity check, admins should always be allowed.
      if users.is_current_user_admin():
          return True

      email = Authentication.GetUserEmail(request)
      if not email:
        return False

      email = email.lower()
      email_hash = hashlib.sha256(email).hexdigest()
      logging.info("Email %s (hash %s) tried to log in" % (email, email_hash))
      return email_hash in Authentication.known_users
