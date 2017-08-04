import requests
import logging

from themeworker import LABELLER_URL

logger = logging.getLogger(__name__)


def _get_url():
    return "{}/predict.json".format(LABELLER_URL)


def get_labels(story_text):
    return _query({'text': story_text})


def _query(data):
    try:
        r = requests.post(_get_url(), json=data)
        logger.debug('labeller says %r', r.content)
        return r.json()
    except requests.exceptions.RequestException as e:
        logger.exception(e)
    return None
