import requests
from dynaconf import settings
import json


def get_github_commits(owner, repo, per_page=100, page=None, since=None, until=None):
    url = "https://api.github.com/repos/{owner}/{repo}/commits".format(
        owner=owner, repo=repo)
    headers = {'Authorization': 'token %s' % next(settings.GITHUB_TOKENS_ITER)}
    r = requests.get(url, headers=headers, params={'per_page': 100, 'page': page, 'since': since, 'until': until})
    # return json.dumps(r.json())  &since={since}&until{until}
    if r.status_code == 200:
        return r.json()
    else:
        print(r.status_code, r.text)
        return None

def get_all_github_commits(owner, repo, since=None, until=None):
    all_commits = []
    for page in range(9999):
        commits = get_github_commits(owner, repo, page)
        print('commitslen',len(commits))
        if (commits is not None) and len(commits) > 0:
            all_commits = all_commits + commits
        elif (commits is not None) and len(commits) == 0:
            return all_commits
        else:
            raise Exception("get_all_github_commits")
    return all_commits


