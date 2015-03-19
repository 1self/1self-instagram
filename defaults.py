#app defaults
def get_file_contents(fname):
    fhandle = open(fname, 'r')
    content = fhandle.read()
    fhandle.close()
    return content.strip()

HOST = "http://instagram-1self-integration.appspot.com"
INSTAGRAM_CLIENT_ID = get_file_contents("instagram_client_id.txt")
INSTAGRAM_CLIENT_SECRET = get_file_contents("instagram_client_secret.txt")
INSTAGRAM_REDIRECT_URL = HOST + "/authRedirect"
raw_scope = ""
OFFLINE_SYNC_ENDPOINT = "/sync"
APP_NAME = "1self instagram"
APP_SESSION_SECRET = get_file_contents("session_secret.txt")

#oneself defaults
ONESELF_API_ENDPOINT             = "http://api.1self.co"
ONESELF_SEND_BATCH_EVENTS_PATH   = "/v1/streams/%s/events/batch"
ONESELF_REGISTER_STREAM_ENDPOINT = "/v1/users/%s/streams"
ONESELF_VISUALIZATION_ENDPOINT   = "/v1/streams/%s/events/steps/walked/sum(numberOfSteps)/daily/barchart"
ONESELF_AFTER_SETUP_REDIRECT     = "/integrations"
ONESELF_APP_ID = get_file_contents("oneself_client_id.txt")
ONESELF_APP_SECRET = get_file_contents("oneself_client_secret.txt")
STANDARD_ACTION_TAGS = []
STANDARD_OBJECT_TAGS = ["internet", "social-network", "instagram"]
