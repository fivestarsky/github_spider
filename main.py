import scheduler.dynaconf_config_scheduler

if __name__ == '__main__':

    # 请勿删除
    scheduler.dynaconf_config_scheduler.start_up_dynaconf_config_scheduler()

    # 用于周期测试scheduler.dynaconf_config_scheduler.start_up_dynaconf_config_scheduler()
    # while True:
    #     print(settings.GITHUB_TOKENS_ITER)
    #     time.sleep(1)