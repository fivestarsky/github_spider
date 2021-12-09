import json
from dynaconf import settings
import requests
import util.opensearch_api as opensearch_api
import util.opensearch_client as opensearch_client
import spider.github_commits as github_commits

def do_test():

    url = "https://api.github.com/repos/apache/spark/issues/events/5716212827".format()
    headers = {'Authorization': 'token %s' % next(settings.GITHUB_TOKENS_ITER)}
    r = requests.get(url, headers=headers)
    print(r.json())


if __name__ == '__main__':
    # print(opensearch_util.create_index("git-commits-match-github-commits-v1", create_index_json))
    # print(json.dumps(github_commits.up_github_commits("apache", "spark"), indent=2))
    opensearch_client.bulk_add_fields()
