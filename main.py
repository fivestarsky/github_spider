import json
from dynaconf import settings
import requests
import util.opensearch_api as opensearch_api
import util.opensearch_client as opensearch_client
import spider.github_commits as github_commits

if __name__ == '__main__':
    opensearch_client.sync_github_commits("apache", "spark")


