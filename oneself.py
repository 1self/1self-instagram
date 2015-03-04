from defaults import *
import json
from google.appengine.api import urlfetch


def sendTo1self(data):
    print("")


def register_stream(oneself_username, registration_token, instagramUserId):
	url = API_URL + "/v1/users/" + oneself_username + "/streams"
	auth_string = ONESELF_APP_ID + ":" + ONESELF_APP_SECRET
	body=""
        callback_url = getCallbackUrl(instagramUserId)
        body = json.dumps({"callbackUrl": callback_url})
	headers = {"Authorization": auth_string, "registration-token": registration_token, "Content-Type": "application/json"}
	r = requests.post(url, headers=headers, data=body)
	try:
		response = json.loads(r.text)
		return response, r.status_code
	except ValueError:
		return r.text, r.status_code


def getCallbackUrl(instagramUserId):
    return HOST + SYNC_ENDPOINT + "?username=" + instagramUserId + "&latestSyncField={{latestSyncField}}&streamid={{streamid}}"
