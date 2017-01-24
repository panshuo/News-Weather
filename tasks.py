# _*_ coding: utf-8 _*_

import requests
import os
from celery import Celery
from config import Config
from manage import db, app as flask_app
from app.models import News, Weather

celery = Celery('M', broker=Config.CELERY_BROKER_URL)
celery.conf.update(Config.__dict__)


@celery.task
def refresh_weather(city='Tianjin'):
    with flask_app.app_context():
        Weather.get_weather(city)


@celery.task
def fetch_news(count=50):
    with flask_app.app_context():
        News.fetch_news(count)



@celery.task
def cache_image():
    with flask_app.app_context():
        all = News.query.all()
        for news in all:
            if not news.static_media_thumbnail:
                download_image.delay(news.id)


@celery.task
def download_image(news_id):
    with flask_app.app_context():
        news = News.query.filter_by(id=news_id).first()
        filename = news.news_agency + str(news.id) + news.media_thumbnail.split('/')[-1]
        if not os.path.isfile(flask_app.config['BASE_DIR'] + '/app/resources/images/' + filename):
            print u'开始下载'
            r = requests.get(news.media_thumbnail)
            with open(flask_app.config['BASE_DIR'] + '/app/resources/images/' + filename, "wb") as image:
                image.write(r.content)
            news.static_media_thumbnail = filename
            print u"成功下载图片：" + filename
            db.session.add(news)
            db.session.commit()

if __name__ == '__main__':
    celery.start()
