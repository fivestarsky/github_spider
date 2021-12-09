from opensearchpy import OpenSearch
from dynaconf import settings
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


def bulk_add_fields():
    all_github_commits = github_commits.get_all_github_commits("apache", "spark", since=None, until=None)
    if (all_github_commits is not None) and (len(all_github_commits > 0)):
        bulk_all_github_commits = []
        templet = {"_index": "github_commits",
                   "_source": None}
        for now_commit in all_github_commits:
            commit_item = templet.copy()
            commit_item["_source"] = now_commit
            bulk_all_github_commits.append(commit_item)
        OpenSearchHelpers.bulk(client=client, actions=bulk_all_github_commits)
