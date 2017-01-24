# _*_ coding: utf-8 _*_

from flask import render_template, redirect, url_for, flash, request
from ..models import User, News, Weather
from . import main
from .. import HWMonitor
from flask_login import login_required, current_user, login_user
from sqlalchemy import desc
from random import sample


# 首页
@main.route('/', methods=['GET', 'POST'])
def index():
    # 如果当前未登录，登入测试帐号
    if not current_user.is_authenticated:
        user = User.query.filter_by(id=100).first()
        login_user(user)

    # 幻灯片部分
    news_count = News.query.filter_by(news_agency='BBC').order_by(desc(News.id)).first().id  # 获取数据库中最后一条新闻的id
    slider = []
    if news_count >= 20:
        selected_news = sample(range(news_count - 10, news_count), 5)  # 随机获得5条新闻的id
        for news in selected_news:
            slider.append(News.query.filter_by(id=news).first())

    # 分页和新闻部分
    page = request.args.get('page', 1, type=int)
    pagination = News.query.order_by(desc(News.id)).paginate(page, per_page=12, error_out=False)
    articles = pagination.items

    # 天气部分
    weather = Weather.query.filter_by(city="Tianjin").order_by(desc(Weather.id)).first()

    # 系统状态部分
    hw_status = HWMonitor()

    return render_template("index.html",
                           articles=articles,
                           weather=weather,
                           pagination=pagination,
                           slider=slider,
                           hw=hw_status)


# 抓取新闻接口 默认50条
@main.route('/fetchnews', methods=['GET', 'POST'])
@login_required
def fetch_news():
    News.fetch_news(50)
    return redirect(url_for('.index'))
