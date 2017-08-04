from __future__ import absolute_import
from celery import Celery

from themeworker import RABBIT_MQ_URL

app = Celery('themeworker',
             broker=RABBIT_MQ_URL,
             include=['themeworker.tasks'])
