import logging
from logging import StreamHandler
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Th1s 5h0uld b3 h4rd 70 gu355'
    MESSAGE_SIZE_LIMIT = 1000

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True


class ProdConfig(Config):
    PROD = True


class HerokuConfig(ProdConfig):

    @classmethod
    def init_app(cls, app):
        ProdConfig.init_app(app)
        # log to stderr
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


def config(env):
    cfg = {
        'dev': DevConfig,
        'test': TestConfig,
        'prod': ProdConfig,
        'heroku': HerokuConfig,
        'default': DevConfig
    }
    return cfg[env]
