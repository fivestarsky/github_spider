from dynaconf import settings
from dynaconf.loaders.redis_loader import delete as dc_redis_delete
from dynaconf.loaders.redis_loader import load as dc_redis_load
from dynaconf.loaders.redis_loader import write as dc_redis_write


def init_dynaconf_redis_opensearch_config():
    configs = {}
    configs["OPENSEARCH_CONFIG"] = {
        "OPENSEARCH_CONFIG": {"HOST": '192.168.8.10',
                              "PORT": 9200,
                              "HTTP_BASIC_AUTH_USER": "admin",
                              "HTTP_BASIC_AUTH_PASS": "admin"
                              }}
    dc_redis_write(settings, configs["OPENSEARCH_CONFIG"])


def init_dynaconf_redis_github_token_config():
    configs = {}
    configs["GITHUB_TOKENS_ITER"] = {
        "GITHUB_TOKENS_ITER": ["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",
                               "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",
                               ]}
    dc_redis_write(settings, configs["GITHUB_TOKENS_ITER"])


def init_all_dynaconf_redis_config():
    init_dynaconf_redis_opensearch_config()
    init_dynaconf_redis_github_token_config()

# 用于配置各种更新
if __name__ == '__main__':
    init_all_dynaconf_redis_config()
