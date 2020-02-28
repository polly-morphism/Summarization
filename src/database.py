from pymongo import MongoClient
from pymongo.database import Database

from conf.app_config import get_config


def get_mongo(config: dict) -> Database:
    username = config.get('username', None)
    if username:
        mongo_client: MongoClient = MongoClient(
            host=config.get('host'),
            port=config.get('port'),
            username=username,
            password=config.get('password'),
            authSource=config.get('db'),
            authMechanism='SCRAM-SHA-1',
            connect=config.get('connect'),
        )
    else:
        mongo_client: MongoClient = MongoClient(
            host=config.get('host'),
            port=config.get('port'),
            connect=config.get('connect'),
        )
    mongo_db = mongo_client[config.get('db')]
    return mongo_db


Config = get_config()
mongo_db = get_mongo(config=Config.MONGODB_SETTINGS)
