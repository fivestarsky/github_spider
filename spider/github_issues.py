import requests
from dynaconf import settings
import json

def get_issue_event(owner, repo, issue_number):
    url = "https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}".format(
        owner=owner, repo=repo, issue_number=issue_number)
    headers = {'Authorization': 'token %s' % next(settings.GITHUB_TOKENS_ITER)}
    r = requests.get(url, headers=headers)


def get_issue_timeline(owner, repo, issue_number):
    url = "https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/timeline".format(
        owner=owner, repo=repo, issue_number=issue_number)
    headers = {'Authorization': 'token %s' % next(settings.GITHUB_TOKENS_ITER)}
    r = requests.get(url, headers=headers)
    # return json.dumps(r.json())
    return r.json()
