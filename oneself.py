from defaults import *
import json
from google.appengine.api import urlfetch
from datetime import datetime

def sendTo1self(user):
    event = construct_event(data)
    
    url = ONESELF_API_ENDPOINT + (ONESELF_SEND_BATCH_EVENTS_PATH % user.oneself_stream_id)

    headers = {"Authorization": user.oneself_writeToken, "Content-Type": "application/json"}

    body = json.dumps(event)

    r = urlfetch.fetch(url=url,
                                payload=body,
                                method=urlfetch.POST,
                                headers=headers)

    try:
        response = json.loads(r.content)
        return response, r.status_code
    except ValueError:
        return r.content, r.status_code


def construct_event(data):
    return {
        "source": APP_NAME,
        "actionTags": STANDARD_ACTION_TAGS,
        "objectTags": STANDARD_OBJECT_TAGS,
        "dateTime": datetime.now().isoformat(),
        "properties": {"Photo-posted": 1},
        }
        

def register_stream(oneself_username, registration_token, instagramUserId):
	url = API_URL + "/v1/users/" + oneself_username + "/streams"
	auth_string = ONESELF_APP_ID + ":" + ONESELF_APP_SECRET
	body=""
        callback_url = getCallbackUrl(instagramUserId)
        body = json.dumps({"callbackUrl": callback_url})
	headers = {"Authorization": auth_string, "registration-token": registration_token, "Content-Type": "application/json"}

        r = urlfetch.fetch(url=url,
                                payload=body,
                                method=urlfetch.POST,
                                headers=headers)

	try:
		response = json.loads(r.content)
		return response, r.status_code
	except ValueError:
		return r.content, r.status_code


def getCallbackUrl(instagramUserId):
    return HOST + SYNC_ENDPOINT + "?username=" + instagramUserId + "&latestSyncField={{latestSyncField}}&streamid={{streamid}}"
