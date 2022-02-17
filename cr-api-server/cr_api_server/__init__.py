# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_mail import Mail
from flask_mail import Message

db = SQLAlchemy()
app = Flask(__name__)

db.init_app(app)
# config
app.config.from_object(Config)
mail = Mail(app)


# app router
with app.app_context():
    from .views import user_view
    app.register_blueprint(user_view, url_prefix="/user")
    from .views import data_view
    app.register_blueprint(data_view, url_prefix="/data")
