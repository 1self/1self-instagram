from defaults import *
import json
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(60)
from datetime import datetime
import logging

def sendTo1self(user, events):
    url = ONESELF_API_ENDPOINT + (ONESELF_SEND_BATCH_EVENTS_PATH % user.stream_id)

    headers = {"Authorization": user.oneself_writeToken, "Content-Type": "application/json"}

    body = json.dumps(events)

    logging.info("Ready to send event url: %s headers: %s body: %s" % (url, headers, body))

    urlfetch.set_default_fetch_deadline(60)

    r = urlfetch.fetch(url=url,
                       payload=body,
                       method=urlfetch.POST,
                       headers=headers)
    
    try:
        logging.info("Response after sending event to 1self %s" % r.content)
        response = json.loads(r.content) if not r.content else json.loads("{}")
        return response, r.status_code
    except ValueError:
        logging.info("Error sending event to 1self: %s %s" % (r.content, r.status_code))
        return r.content, r.status_code


def media_upload_event():
    return {
        "source": APP_SOURCE,
        "actionTags": STANDARD_ACTION_TAGS + ["share", "publish"],
        "objectTags": STANDARD_OBJECT_TAGS + ["media"],
        "dateTime": datetime.now().isoformat(),
        "properties": {
            "Media-Upload": 1
            }
        }
        
def sync_event(action_type):
    return {
        "actionTags": [action_type],
        "objectTags": ["1self", "integration", "sync"],
        "dateTime": datetime.now().isoformat(),
        "source": APP_SOURCE,
        "properties": {
            }
        }

def sync_error_event(action_type, code, message):
    return {
        "actionTags": [action_type],
        "objectTags": ["1self", "integration", "sync"],
        "dateTime": datetime.now().isoformat(),
        "source": APP_SOURCE,
        "properties": {
            "code": code,
            "message": message
            }
        }        

def following_event(count):
    return {
        "source": APP_SOURCE,
        "actionTags": STANDARD_ACTION_TAGS + ["following", "sample"],
        "objectTags": STANDARD_OBJECT_TAGS + ["social-graph", "outbound", "following"],
        "dateTime": datetime.now().isoformat(),
        "properties": {
            "latest-count": count
            }
        }

def followers_event(count):
    return {
        "source": APP_SOURCE,
        "actionTags": STANDARD_ACTION_TAGS + ["follower", "sample"],
        "objectTags": STANDARD_OBJECT_TAGS + ["social-graph", "inbound", "follower"],
        "dateTime": datetime.now().isoformat(),
        "properties": {
            "latest-count": count
            }
        }


def register_stream(oneself_username, registration_token, instagramUserId):
    logging.info("registering stream for " + oneself_username)

    url = ONESELF_API_ENDPOINT + "/v1/users/" + oneself_username + "/streams"
    auth_string = ONESELF_APP_ID + ":" + ONESELF_APP_SECRET
    body=""
    callback_url = getCallbackUrl(instagramUserId)
    logging.info("callback URL " + callback_url)
    body = json.dumps({"callbackUrl": callback_url})
    headers = {"Authorization": auth_string, 
               "registration-token": registration_token, 
               "Content-Type": "application/json"
               }

    r = urlfetch.fetch(url=url,
                       payload=body,
                       method=urlfetch.POST,
                       headers=headers)

    try:
        response = json.loads(r.content)
        logging.info("Stream registration successfull")
        return response
    except ValueError:
        logging.info("Stream registration error: " + r.content)
        return r.content, r.status_code


def getCallbackUrl(instagramUserId):
    return HOST + OFFLINE_SYNC_ENDPOINT + "?username=" + instagramUserId + "&latestSyncField={{latestSyncField}}&streamid={{streamid}}"
