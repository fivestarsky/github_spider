import json
import requests
from requests.auth import HTTPBasicAuth
from dynaconf import settings
from opensearchpy import OpenSearch
from opensearchpy import helpers as OpenSearchHelpers
import spider.github_commits as github_commits

client = OpenSearch(
    hosts=[{'host': settings.OPENSEARCH_CONFIG.HOST, 'port': settings.OPENSEARCH_CONFIG.PORT}],
    http_compress=True,
    http_auth=(settings.OPENSEARCH_CONFIG.HTTP_BASIC_AUTH_USER, settings.OPENSEARCH_CONFIG.HTTP_BASIC_AUTH_PASS),
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False
)


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


def sync_github_commits(owner, repo, since=None, until=None):
    success, failed = 0, 0
    all_github_commits = github_commits.get_all_github_commits(owner, repo, since, until)
    if (all_github_commits is not None) and (len(all_github_commits > 0)):
        bulk_all_github_commits = []
        template = {"_index": "github_commits",
                    "_source": None}
        for now_commit in all_github_commits:
            commit_item = template.copy()
            commit_item["_source"] = now_commit
            bulk_all_github_commits.append(commit_item)
        success, failed = OpenSearchHelpers.bulk(client=client, actions=bulk_all_github_commits)

    return success, failed


def get_all_github_issues(owner, repo, since=None, until=None):
    print("")
