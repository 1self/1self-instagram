#app defaults
def get_file_contents(fname):
    fhandle = open(fname, 'r')
    content = fhandle.read()
    fhandle.close()
    return content

HOST = "http://localhost:8080"
client_id = get_file_contents("instagram_client_id.txt")
client_secret = get_file_contents("instagram_client_secret.txt")
redirect_uri = "http://localhost:8080/authRedirect"
realtime_callback = "http://localhost:8080/push"
raw_scope = ""
SYNC_ENDPOINT = "/sync"
APP_NAME = "1self instagram"


#oneself defaults
ONESELF_API_ENDPOINT             = "http://api-staging.1self.co"
ONESELF_SEND_BATCH_EVENTS_PATH   = "/v1/streams/%s/events/batch"
ONESELF_REGISTER_STREAM_ENDPOINT = "/v1/users/%s/streams"
ONESELF_VISUALIZATION_ENDPOINT   = "/v1/streams/%s/events/steps/walked/sum(numberOfSteps)/daily/barchart"
ONESELF_AFTER_SETUP_REDIRECT     = "/integrations"
ONESELF_APP_ID = get_file_contents("oneself_client_id.txt")
ONESELF_APP_SECRET = get_file_contents("oneself_client_secret.txt")
STANDARD_ACTION_TAGS = ["upload"]
STANDARD_OBJECT_TAGS = ["instagram", "media"]

    
