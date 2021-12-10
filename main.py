import util.opensearch.opensearch_client as opensearch_client

if __name__ == '__main__':
    opensearch_client.sync_github_commits("apache", "spark")


