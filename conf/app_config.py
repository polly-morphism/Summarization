import os
import logging
from typing import Union, Type


class Config(object):
    DEBUG = False
    LOG_LEVEL = logging.INFO

    APP_NAME = "summarizer"

    #MONGO_DATABASE = "news_inn"
    #MONGO_PORT = 27017
    #MONGO_ALIAS = "default"
    #MONGODB_SETTINGS = {"db": MONGO_DATABASE, "alias": MONGO_ALIAS, "connect": False}

    SUMMARIZER_API_URL = os.getenv("SUMMARIZER_API_URL")


class ProductionConfig(Config):
    LOG_LEVEL = logging.ERROR

    #MONGO_HOST = os.getenv("MONGO_HOST")
    #MONGO_DATABASE = os.getenv("MONGO_DATABASE")
    #MONGO_PORT = int(os.getenv("MONGO_PORT", 0))
    #MONGO_USERNAME = os.getenv("MONGO_USERNAME")
    #MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    #MONGODB_SETTINGS = {
    #    "host": MONGO_HOST,
    #    "port": MONGO_PORT,
    #    "db": MONGO_DATABASE,
    #    "username": MONGO_USERNAME,
    #    "password": MONGO_PASSWORD,
    #    "connect": False,
    #}


class DevelopmentConfig(Config):
    DEBUG = True


def get_config() -> Type[Union[ProductionConfig, DevelopmentConfig]]:
    env = os.getenv("ENV", "dev")
    if env == "prod":
        result = ProductionConfig
    else:
        result = DevelopmentConfig
    return result
