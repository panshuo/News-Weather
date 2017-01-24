# _*_ coding: utf-8 _*_

import os
from celery.schedules import crontab


class Config:
    def __init__(self):
        pass

    SECRET_KEY = os.environ.get('SECRET_KEY') or '$%^NB4%^#_+UHha'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_ECHO = True
    WEIBO_APP_KEY = '3797168746'
    WEIBO_APP_SECRET = 'cf1eb69ab2ea726b1b0542da97160c52'
    WEIBO_CALLBACK_URI = 'http://tetewechat.ngrok.cc/oauth/weibo'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')
    # SQLALCHEMY_DATABASE_URI = 'postgresql://tete:8888@127.0.0.1/tetedb'
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERYBEAT_SCHEDULE = {  # 每30分钟刷新一次天气
                            'refresh-weather-every-30-minutes': {'task': 'tasks.refresh_weather',
                                                                 'schedule': crontab(minute='*/30'),
                                                                 'args': ("Tianjin",)},
                            # 每1小时刷新一次新闻
                            'refresh-news-every-hour': {'task': 'tasks.fetch_news',
                                                        'schedule': crontab(minute=0, hour='*/1'),
                                                        'args': (50,)},

                            # 每2小时缓存新闻图片到本地
                            'cache-news-image-every-2-hours': {'task': 'tasks.cache_image',
                                                               'schedule': crontab(minute=0, hour='*/2')}
    }
