import logging
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

api = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID, client_secret=INSTAGRAM_CLIENT_SECRET, redirect_uri=INSTAGRAM_REDIRECT_HANDLER)
sessions.default_config['secret_key'] = APP_SESSION_SECRET
sessions.default_config['cookie_name'] = 'oneself_cookie'

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
        logging.info("Redirecting to: %s" % auth_uri)

        self.redirect(auth_uri)

class AuthRedirect(webapp2.RequestHandler):
    
    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    def get(self):
        code = self.request.get('code')
        user_metadata = api.exchange_code_for_access_token(code)
        access_token, user_info = user_metadata

        logging.info("Access token successfully found: %s" % access_token)
        logging.info("User info fetched successfully: %s" % user_info)

        self.session_store = sessions.get_store(request=self.request)
        oneself_userName = self.session.get("oneself_userName")
        oneself_regToken = self.session.get("oneself_regToken")

        stream = register_stream(oneself_userName, oneself_regToken, user_info["id"])

        user = User()
        user.access_token = access_token
        user.full_name = user_info["full_name"]
        user.uid = user_info["id"]
        user.username = user_info["username"]
        user.profile_picture = user_info["profile_picture"]
        user.oneself_stream_id = stream["streamid"]
        user.oneself_readToken = stream["readToken"]
        user.oneself_writeToken = stream["writeToken"]
        
        key = user.put()
        
        logging.info("User stored successfully. Key id: %s" % key)
        logging.info("Instagram UserId: %s" % user.uid)

        self.redirect(ONESELF_API_ENDPOINT + ONESELF_AFTER_SETUP_REDIRECT)

class GetUser(webapp2.RequestHandler):

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    def get(self):
        self.session_store = sessions.get_store(request=self.request)
        logging.info(self.session.get("oneself_userName"))

        userid = self.request.get('userid')
        user = getUserByInstagramId(userid)
        logging.info(user)


class HandlePushFromInstagram(webapp2.RequestHandler):
    def get(self):
        challenge = self.request.get('hub.challenge')
        self.response.write(challenge)

    def post(self):
        jsonstring = self.request.body
        jsonobject = json.loads(jsonstring)
        logging.info("Request received from instagram: %s" % jsonobject)
        formatAndSend(jsonobject)
        #t = background_thread.start_new_background_thread(formatAndSend, [jsonobject])
        self.response.write("success")

class Nothing(webapp2.RequestHandler):
    def get(self):
        self.response.write("Sorry, there is nothing here")


class HandleOfflineSyncRequest(webapp2.RequestHandler):
    def get(self):
        self.response.write("Nothing to sync")


def formatAndSend(data):
    #currently instagram supports only media post notification
    #theoritically data will only come for 1 user, still iterating
    #we have to send each media upload as an event to 1self
    #logic may have to change as we support more

    for d in data:
        userid = d["object_id"]
        logging.info("Finding user with id: %s" % userid)
        user = getUserByInstagramId(userid)
        logging.info("User found with: %s" % userid)
        sendTo1self(user)


application = webapp2.WSGIApplication([
    ('/', Nothing),
    ('/login', MainPage),
    ('/authRedirect', AuthRedirect),
    ('/user', GetUser),
    ('/push', HandlePushFromInstagram),
    ('/sync', HandleOfflineSyncRequest)
], debug=True)

