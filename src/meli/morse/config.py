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


def config(env):
    cfg = {
        'dev': DevConfig,
        'test': TestConfig,
        'prod': ProdConfig,
        'default': DevConfig
    }
    return cfg[env]
