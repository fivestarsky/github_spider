import requests
from requests.auth import HTTPBasicAuth
from opensearchpy import OpenSearch
from dynaconf import settings
import json


def search_sql():
    url = "https://{host}:{port}/{path}".format(
        host=settings.OPENSEARCH_CONFIG.HOST,
        port=settings.OPENSEARCH_CONFIG.PORT,
        path="_plugins/_sql")
    body = {"query": "SELECT event, actor FROM github-issues-timeline WHERE actor.login='HyukjinKwon'"}
    r = requests.post(url,
                      verify=False,
                      auth=HTTPBasicAuth(
                          settings.OPENSEARCH_CONFIG.HTTP_BASIC_AUTH_USER,
                          settings.OPENSEARCH_CONFIG.HTTP_BASIC_AUTH_PASS),
                      headers={'content-type': 'application/json'},
                      data=json.dumps(body),
                      )
    return json.dumps(r.json(), sort_keys=True, indent=2)


def add_timeline(timeline_json):
    print("")
