import os
import secrets
from dotenv import load_dotenv


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
env_path = os.path.join(PARENT_DIR, '.env')
load_dotenv(env_path, override=True)


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLE = True
    # SECRET KEY config
    SECRET_KEY = str(secrets.token_hex(16))
    # SQLAlchemy config - use sqlite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PARENT_DIR,
                                                          os.getenv('DB_NAME'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # config mail server
    MAIL_USE_SMTP = True
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = True
    # you need to export to environment: export EMAIL_USER=... and for EMAIL_PASS
    # your email need to turn on less secure app on google (if you use google)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'bad_key'
    # discard CSRF tokens in the form for testing
    CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
