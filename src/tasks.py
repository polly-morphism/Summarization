"""
# start local celery: celery worker -A src.tasks.celery --loglevel=info --autoscale=8,2 -n similarity_checker -Q similarity_checker
"""

#from celery import Celery

#from conf.celery_config import CeleryConfig

#celery = Celery(
#    main=CeleryConfig.CELERY_APP_NAME,
#    broker=CeleryConfig.CELERY_BROKER_URL,
#    include=CeleryConfig.CELERY_MODULES,
#)
#celery.conf.update(CeleryConfig.__dict__)
