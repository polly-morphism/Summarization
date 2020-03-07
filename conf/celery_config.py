#import os

#from kombu import Exchange, Queue

#from conf.app_config import get_config

#Config = get_config()


#class CeleryConfig(object):
#    RABBIT_MQ_HOST = os.getenv("RABBIT_MQ_HOST", "localhost")
#    RABBIT_MQ_USER = os.getenv("RABBIT_MQ_USER", "admin")
#    RABBIT_MQ_PASS = os.getenv("RABBIT_MQ_PASS", "rabbit")
#    CELERY_APP_NAME = Config.APP_NAME
#    CELERY_BROKER_URL = (
#        f"amqp://{RABBIT_MQ_USER}:{RABBIT_MQ_PASS}@{RABBIT_MQ_HOST}:5672//"
#    )
#
#    CELERY_MODULES = ("src.pipeline.summarizer",)
#    app_exchange = Exchange(CELERY_APP_NAME, type="direct")
#    CELERY_QUEUES = (
#        Queue(
#            CELERY_APP_NAME,
#            app_exchange,
#            routing_key=CELERY_APP_NAME,
#            consumer_arguments={"x-priority": 0},
#        ),
#    )
#    CELERY_TASK_DEFAULT_QUEUE = CELERY_APP_NAME
#    CELERY_TASK_DEFAULT_EXCHANGE = CELERY_APP_NAME
#    CELERY_TASK_DEFAULT_ROUTING_KEY = CELERY_APP_NAME
#    CELERY_ROUTES = {
#        "src.pipeline.summarizer.*": {
#            "queue": CELERY_APP_NAME,
#            "routing_key": CELERY_APP_NAME,
#        },
#    }

#    CELERY_RESULT_SERIALIZER = "json"
#    CELERY_TASK_RESULT_EXPIRES = 300

#    CELERY_ACCEPT_CONTENT = ["json", "msgpack", "yaml"]
#    CELERY_TASK_SERIALIZER = "json"
