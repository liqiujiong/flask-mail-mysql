# -*- coding:utf-8 -*-
from .helpers import env


class Config(object):
    DEBUG = env("DEBUG", cast=bool)
    JWT_SECRET = env("JWT_SECRET", cast=str)
    PORT = env("PORT", cast=int)

    SQLALCHEMY_DATABASE_URI = env("SQLALCHEMY_DATABASE_URI", cast=str)
    SQLALCHEMY_TRACK_MODIFICATIONS = env("SQLALCHEMY_TRACK_MODIFICATIONS",
                                         cast=bool,
                                         default=False)

    REDIS_URL = env("REDIS_URL", cast=str)

    MAIL_SERVER = env("MAIL_SERVER", cast=str)
    MAIL_PROT = env("MAIL_PROT", cast=int)
    MAIL_USE_TLS = env("MAIL_USE_TLS", cast=bool)
    MAIL_USE_SSL = env("MAIL_USE_SSL", cast=bool)
    MAIL_USERNAME = env("MAIL_USERNAME", cast=str)
    MAIL_PASSWORD = env("MAIL_PASSWORD", cast=str)

    MAIL_CODE_TIME = env("MAIL_CODE_TIME", cast=int)
    MAIL_CODE_RESEND = env("MAIL_CODE_RESEND", cast=int)

    USER_ROLE_ROOT = 0
    USER_ROLE_PROVINCE = 1
    USER_ROLE_CITY = 2
