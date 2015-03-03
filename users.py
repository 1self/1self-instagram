from google.appengine.ext import ndb

class User(ndb.Model):
    access_token = ndb.StringProperty(indexed=False)
    full_name = ndb.StringProperty(indexed=False)
    uid = ndb.StringProperty(indexed=False)
    username = ndb.StringProperty(indexed=False)
    profile_picture = ndb.StringProperty(indexed=False)
    created_date = ndb.DateTimeProperty(auto_now_add=True)

def getUser(key):
    key_to_int = int(key)
    user_key = ndb.Key('User', key_to_int)
    return user_key.get()
