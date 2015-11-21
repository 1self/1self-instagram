from google.appengine.ext import ndb

class User(ndb.Model):
    access_token = ndb.StringProperty(indexed=False)
    full_name = ndb.StringProperty(indexed=False)
    uid = ndb.StringProperty(indexed=True)
    username = ndb.StringProperty(indexed=False)
    profile_picture = ndb.StringProperty(indexed=False)
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    oneself_stream_id = ndb.StringProperty(indexed=True)
    stream_id = ndb.StringProperty(indexed=True)
    oneself_readToken = ndb.StringProperty(indexed=False)
    oneself_writeToken = ndb.StringProperty(indexed=False)

def getUserByInstagramId(key):
    key_to_int = int(key)
    qry = User.query(User.uid == key)
    return qry.get()

def get_user_by_stream_id(streamId):
    qry = User.query(User.oneself_stream_id == str(streamId))
    return qry.get()

def update_user_stream_id(logging):
    qry = User.query()
    for user in qry:
        user.stream_id = user.oneself_stream_id
        user.put()
        logging.info("updated {0} for streamid {1}".format(user.username, user.stream_id))

        