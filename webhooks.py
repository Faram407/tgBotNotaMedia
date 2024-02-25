import json
import requests

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url_webhook = "https://b.loc/rest/1/ndsrhts4ollpr3cb/"
method = "tasks.task.list"

param = {
    "filter ": {
        "?TITLE": "test",
        # "GROUP_ID": "1",
        # "STAGE_ID": "8"
    },
    "select": {
        # "*"
        'ID', 'TITLE', 'DESCRIPTION'
    },
    "order": {
        "ID": 'ACS'
    },
}


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def b24rest_request(url_web_hook: str, meth: str, par: dict) -> dict:
    url = url_web_hook + meth + '.json?'

    response = requests.post(url, json=json.dumps(par, default=set_default), verify=False)
    return response.json()


resp = b24rest_request(url_webhook, method, param)

print(json.dumps(resp.pop("result").pop('tasks'), indent=4, ensure_ascii=False))
