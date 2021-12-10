from dynaconf import settings
from apscheduler.schedulers.background import BackgroundScheduler


def up_dynaconf_config():
    # 用于周期性更新dynaconf，防止redis的dynaconf配置改变后不同步
    settings._setup()


def start_up_dynaconf_config_scheduler():
    dynaconf_config_scheduler = BackgroundScheduler()
    dynaconf_config_scheduler.add_job(up_dynaconf_config, 'interval', seconds=5)
    dynaconf_config_scheduler.start()
