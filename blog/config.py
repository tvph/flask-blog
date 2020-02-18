import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLE = True
    # SECRET KEY config
    SECRET_KEY = str(secrets.token_hex(16))
    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # os.environ['DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # config mail server
    MAIL_USE_SMTP = True
    MAIL_SEVER = 'smtp.googlemail.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    # you need to export to environment: export EMAIL_USER=... and for EMAIL_PASS too
    # your email need to turn on less secure app on google (if you use google)
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')




class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
