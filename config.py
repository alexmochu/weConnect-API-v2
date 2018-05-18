# config.py
import os

class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

class TestingConfig(Config):
    """ Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY') or 'gkldfgdflkgdflkgjdfjk'
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DB_URL')
    PRESERVE_CONTEXT_ON_EXCEPTION = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}