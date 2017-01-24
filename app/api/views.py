# _*_ coding: utf-8 _*_

from . import api
from .. import db
from ..models import News, User
from flask import make_response, request
from flask_login import current_user, login_required
from .. import HWMonitor
import json


def text_shorten(text, width=10):
    if len(text) <= width:
        return text
    else:
        try:
            return text[:width] + '... '
        except ValueError:
            print u"传入的对象不可缩短"

@api.route('/api/v1/hw_status', methods=['GET'])
def hw_monitor():
    hw_status = HWMonitor()
    result = {}
    result['r'] = 0
    result['status'] = 200
    result['hw_status'] = hw_status.__dict__

    response = make_response()
    response.headers['Content-Type'] = 'application/json'
    response.data = json.dumps(result)
    return response, 200


@api.route('/api/v1/favourites', methods=['GET', 'POST', 'DELETE'])
def favourites():
    result = {}
    response = make_response()
    if not current_user.is_authenticated:
        result['message'] = u'请先登录再使用收藏功能'
        response.headers['Content-Type'] = 'application/json'
        response.data = json.dumps(result)
        return response, 403
    news_id = request.json.get('newsID')
    news = News.query.filter_by(id=int(news_id)).first()
    if news and request.method == 'POST':
        user = current_user._get_current_object()
        user.star(news)
        db.session.add(user)
        result['message'] = u"成功添加 " + text_shorten(news.title, width=20) + u"到 " + user.username + u" 的收藏夹"
        response.headers['Content-Type'] = 'application/json'
        response.data = json.dumps(result)
        return response, 200
    if news and request.method == 'DELETE':
        user = current_user._get_current_object()
        user.cancel_star(news)
        db.session.add(user)
        result['message'] = u"成功从 " + user.username + u" 的收藏夹" + u"取消收藏 " + text_shorten(news.title, width=20)
        response.headers['Content-Type'] = 'application/json'
        response.data = json.dumps(result)
        return response, 200
    else:
        result['message'] = u'提交的newsID不存在'
        response.headers['Content-Type'] = 'application/json'
        response.data = json.dumps(result)
        return response, 400