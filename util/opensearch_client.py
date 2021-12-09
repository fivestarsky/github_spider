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
    client.search()
    temp='''GET github_issue_raw/_search
{
  "query": {
    "bool": {"must": [
    {"term": {
      "search_fields.owner": {
        "value": "apache"
      }
    }},
    {"term": {
      "search_fields.repo": {
        "value": "spark"
      }
    }}  
    ]}
  }
}'''