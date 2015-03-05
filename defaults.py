#app defaults

HOST = "http://localhost:8080"
client_id = "9c389bb2cce44dd7bcd5271ef516d82c"
client_secret = "785e7cf10ec74d4e936d1d10c7ea9d3c"
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
ONESELF_APP_ID = "app-id-1bb5f1c77f0df722a9b1bc650a41988a"
ONESELF_APP_SECRET = "app-secret-70ddd9b5cd842c9747241a5510d831b0fd18110d9bbb487d3e276f1a1c31b448"
STANDARD_ACTION_TAGS = ["upload"]
STANDARD_OBJECT_TAGS = ["instagram", "media"]
