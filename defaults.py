#app defaults
import os
import logging

for key in os.environ.keys():
    logging.info("%30s %s \n" % (key,os.environ[key]))

def get_file_contents(fname):
    fhandle = open(fname, 'r')
    content = fhandle.read()
    fhandle.close()
    return content.strip()

HOST = os.getenv("INSTAGRAM_HOST", "http://instagram.1self.dev")
logging.info("HOST: %s", HOST)

INSTAGRAM_CLIENT_ID = os.getenv("INSTAGRAM_CLIENT_ID", "d2ad2a4c62ad434dba3f8a33a01cdfbc")
INSTAGRAM_CLIENT_SECRET = os.getenv("INSTAGRAM_CLIENT_SECRET", "32132ad1eb514df0bc31f662ee98a963")
logging.info("INSTAGRAM_CLIENT_SECRET: %s" % INSTAGRAM_CLIENT_SECRET)
INSTAGRAM_REDIRECT_URL = HOST + "/authRedirect"
raw_scope = ""
OFFLINE_SYNC_ENDPOINT = "/sync"
APP_NAME = "1self instagram"
APP_SOURCE = "1self-instagram"
APP_SESSION_SECRET = os.getenv("APP_SESSION_SECRET", "dev-secret")

#oneself defaults
ONESELF_APP_ENDPOINT             = os.getenv("ONESELF_APP_ENDPOINT")
logging.info("ONESELF_APP_ENDPOINT: " + ONESELF_APP_ENDPOINT)
ONESELF_API_ENDPOINT             = os.getenv("INSTAGRAM_ONESELF_API_ENDPOINT", "http://api.1self.dev")
ONESELF_SEND_BATCH_EVENTS_PATH   = "/v1/streams/%s/events/batch"
ONESELF_REGISTER_STREAM_ENDPOINT = "/v1/users/%s/streams"
ONESELF_VISUALIZATION_ENDPOINT   = "/v1/streams/%s/events/steps/walked/sum(numberOfSteps)/daily/barchart"
ONESELF_AFTER_SETUP_REDIRECT     = "/integrations"
ONESELF_APP_ID = os.getenv("INSTAGRAM_APP_ID", "app-id-instagram")
ONESELF_APP_SECRET = os.getenv("INSTAGRAM_APP_SECRET", "app-secret-instagram")
STANDARD_ACTION_TAGS = []	
STANDARD_OBJECT_TAGS = ["internet", "social-network", "instagram"]
