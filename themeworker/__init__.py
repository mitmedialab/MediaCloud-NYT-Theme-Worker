import os
import sys
import logging
import mediacloud
from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging

from themeworker.config import get_default_config, ConfigException

VERSION = "0.3.0"

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# set up logging
logging.basicConfig(stream=sys.stdout, filename=os.path.join(base_dir, 'worker.log'),
                    level=logging.INFO, format='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
logger = logging.getLogger(__name__)
logger.info("------------------------------------------------------------------------")
logger.info("Starting up NYT Theme Worker v{}".format(VERSION))

config = get_default_config()

BROKER_URL = config.get('BROKER_URL')
logger.info("BROKER_URL: {}".format(BROKER_URL))

MC_API_KEY = config.get('MC_API_KEY')
mc = mediacloud.api.AdminMediaCloud(MC_API_KEY)
logger.info("MC_API_KEY: {}".format(MC_API_KEY))

LABELLER_URL = config.get('LABELLER_URL')
logger.info("LABELLER_URL: {}".format(LABELLER_URL))

try:
    SENTRY_DSN = config.get('SENTRY_DSN')
    logger.info("SENTRY_DSN: {}".format(SENTRY_DSN))
    handler = SentryHandler(SENTRY_DSN)
    handler.setLevel(logging.WARN)
    setup_logging(handler)
except ConfigException:
    logger.info("No logging to sentry")