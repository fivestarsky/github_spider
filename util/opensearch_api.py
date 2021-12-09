import json
import requests
from requests.auth import HTTPBasicAuth
from dynaconf import settings


def search_sql(sql_text):
    url = "https://{host}:{port}/{path}".format(
        host=settings.OPENSEARCH_CONFIG.HOST,
        port=settings.OPENSEARCH_CONFIG.PORT,
        path="_plugins/_sql")
    body = {"query": "{sql_text}".format(sql_text=sql_text)}
    r = requests.post(url,
                      verify=False,
                      auth=HTTPBasicAuth(
                          settings.OPENSEARCH_CONFIG.HTTP_BASIC_AUTH_USER,
                          settings.OPENSEARCH_CONFIG.HTTP_BASIC_AUTH_PASS),
                      headers={'content-type': 'application/json'},
                      data=json.dumps(body),
                      )
    return json.dumps(r.json(), sort_keys=True, indent=2)


def create_index(index_name, index_config_json):
    url = "https://{host}:{port}/{index_name}".format(
        host=settings.OPENSEARCH_CONFIG.HOST,
        port=settings.OPENSEARCH_CONFIG.PORT,
        index_name=index_name)
    r = requests.put(url,
                     verify=False,
                     auth=HTTPBasicAuth(
                         settings.OPENSEARCH_CONFIG.HTTP_BASIC_AUTH_USER,
                         settings.OPENSEARCH_CONFIG.HTTP_BASIC_AUTH_PASS),
                     headers={'content-type': 'application/json'},
                     data=index_config_json,
                     )
    return json.dumps(r.json(), sort_keys=True, indent=2)


def delete_index(index_name):
    url = "https://{host}:{port}/{index_name}".format(
        host=settings.OPENSEARCH_CONFIG.HOST,
        port=settings.OPENSEARCH_CONFIG.PORT,
        index_name=index_name)
    r = requests.delete(url,
                        verify=False,
                        auth=HTTPBasicAuth(
                            settings.OPENSEARCH_CONFIG.HTTP_BASIC_AUTH_USER,
                            settings.OPENSEARCH_CONFIG.HTTP_BASIC_AUTH_PASS),
                        headers={'content-type': 'application/json'},
                        )
    return json.dumps(r.json(), sort_keys=True, indent=2)