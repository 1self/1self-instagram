from defaults import *
import webapp2
import vendor
vendor.add("lib")
from instagram.client import InstagramAPI
from users import *
import json
from google.appengine.api import background_thread
from oneself import *
from webapp2_extras import sessions


scope = raw_scope.split(' ')
if not scope or scope == [""]:
    scope = ["basic"]

api = InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
sessions.default_config = {
    'secret_key':      'lol',
    'cookie_name':     '1self-session',
    'session_max_age': None,
    'cookie_args': {
        'max_age':     None,
        'domain':      None,
        'path':        '/',
        'secure':      None,
        'httponly':    False,
    },
    'backends': {
        'securecookie': 'webapp2_extras.sessions.SecureCookieSessionFactory',
        'datastore':    'webapp2_extras.appengine.sessions_ndb.' \
                        'DatastoreSessionFactory',
        'memcache':     'webapp2_extras.appengine.sessions_memcache.' \
                        'MemcacheSessionFactory',
    },
}


class MainPage(webapp2.RequestHandler):

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    def get(self):
        oneself_userName = self.request.get("username")
        oneself_regToken = self.request.get("token")

        if (oneself_userName == "") or (oneself_regToken == ""):
            self.response.write("1self metadata not found")
            return

        self.session_store = sessions.get_store(request=self.request)
        self.session['oneself_userName'] = oneself_userName
        self.session['oneself_regToken'] = oneself_regToken
        
        self.session_store.save_sessions(self.response)

        auth_uri = api.get_authorize_login_url(scope = scope)
        print(auth_uri)
        self.redirect(auth_uri)

class AuthRedirect(webapp2.RequestHandler):
    
    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    def get(self):
        code = self.request.get('code')
        user_metadata = api.exchange_code_for_access_token(code)
        access_token, user_info = user_metadata

        print(access_token)
        print(user_info)

        self.session_store = sessions.get_store(request=self.request)
        oneself_userName = self.session.get("oneself_userName")
        oneself_regToken = self.session.get("oneself_regToken")

        stream, status = register_stream(oneself_userName, oneself_regToken, user.uid)

        user = User()
        user.access_token = access_token
        user.full_name = user_info["full_name"]
        user.uid = user_info["id"]
        user.username = user_info["username"]
        user.profile_picture = user_info["profile_picture"]

        key = user.put()
        
        print("Key(so called)")
        print(key)


class GetUser(webapp2.RequestHandler):

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    def get(self):
        self.session_store = sessions.get_store(request=self.request)
        print(self.session.get("oneself_userName"))

        userid = self.request.get('userid')
        user = getUserByInstagramId(userid)
        print(user)


class HandlePushFromInstagram(webapp2.RequestHandler):
    def get(self):
        challenge = self.request.get('hub.challenge')
        self.response.write(challenge)

    def post(self):
        jsonstring = self.request.body
        jsonobject = json.loads(jsonstring)
        t = background_thread.BackgroundThread(sendTo1self, [jsonobject])
        t.start()
        print(jsonobject)


class Nothing(webapp2.RequestHandler):
    def get(self):
        self.response.write("Sorry, there is nothing here")


application = webapp2.WSGIApplication([
    ('/', Nothing),
    ('/login', MainPage),
    ('/authRedirect', AuthRedirect),
    ('/user', GetUser),
    ('/push', HandlePushFromInstagram)
], debug=True)

