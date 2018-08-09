from __future__ import absolute_import
from celery import Celery

from themeworker import BROKER_URL

app = Celery('themeworker',
             broker=BROKER_URL,
             include=['themeworker.tasks'])
