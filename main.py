from dynaconf import settings
import requests
import util.opensearch as opensearch_util


def do_test():
    url = "https://api.github.com/repos/apache/spark/issues/events/5716212827".format()
    headers = {'Authorization': 'token %s' % next(settings.GITHUB_TOKENS_ITER)}
    r = requests.get(url, headers=headers)
    print(r.json())

if __name__ == '__main__':
    print(opensearch_util.search_sql())



