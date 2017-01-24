# _*_ coding: utf-8 _*_

import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from utils import HWMonitor
# from tasks import download_image
from weibo import APIClient

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.signin'
weibo_client = APIClient(app_key=Config.WEIBO_APP_KEY,
                         app_secret=Config.WEIBO_APP_SECRET,
                         redirect_uri=Config.WEIBO_CALLBACK_URI
                         )


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
