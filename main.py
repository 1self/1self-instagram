import webapp2
import vendor
vendor.add("lib")
from instagram.client import InstagramAPI


client_id = "9c389bb2cce44dd7bcd5271ef516d82c"
client_secret = "785e7cf10ec74d4e936d1d10c7ea9d3c"
redirect_uri = "http://localhost:8080/authRedirect"
raw_scope = ""
scope = raw_scope.split(' ')
if not scope or scope == [""]:
    scope = ["basic"]

api = InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)


class MainPage(webapp2.RequestHandler):
    def get(self):
        auth_uri = api.get_authorize_login_url(scope = scope)
        print(auth_uri)
        self.redirect(auth_uri)

class AuthRedirect(webapp2.RequestHandler):
    def get(self):
        access_token = api.exchange_code_for_access_token(code)
        print ("access token: " )
        print (access_token)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/authRedirect', AuthRedirect)
], debug=True)

