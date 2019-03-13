import requests
import logging
import json

from themeworker import LABELLER_URL

logger = logging.getLogger(__name__)


def _get_url():
    return "{}/predict.json".format(LABELLER_URL)


def get_labels(story_text):
    return _query({'text': story_text})


def _query(data):
    try:
        r = requests.post(_get_url(), json=data)
        if r.status_code is not 200:
            message = "Server returned {} :-( (data len was {})".format(r.status_code, len(data['text']))
            logger.error(message)
            raise RuntimeError(message)
        else:
            logger.info('labeller says %r', r.content)
            return r.json()
    except requests.exceptions.RequestException as e:
        logger.exception(e)
    return None

if __name__ == "__main__":
    sample_text = "A day after the president declared he would be proud to let funding lapse for dozens of government agencies if he does not get the money he wants for the wall, congressional Republicans signaled little appetite to join his cause."
    labels = get_labels(sample_text)['descriptors600']
    print(json.dumps(labels, indent=2))
