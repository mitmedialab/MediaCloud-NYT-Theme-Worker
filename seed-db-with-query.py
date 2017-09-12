import logging
import sys
import time

from themeworker import db, SERVICE_NAME

logger = logging.getLogger(__name__)

# load task-specific
if len(sys.argv) is not 3:
    logger.error("You have to give this script a query and the number of stories to fetch")
    sys.exit()

query = str(sys.argv[1])
stories_to_fetch = int(sys.argv[2])
app_config = {
    "name": SERVICE_NAME,
    "query": query,
    "last_processed_stories_id": 0,
    "stories_to_fetch": stories_to_fetch,
    "created_at": time.strftime("%Y%m%d-%H%M%S"),
    "retag": True,
}

existing_app_config = db.apps.find_one({'name': SERVICE_NAME})
if existing_app_config:
    # need to update the existing app config
    db.apps.delete_many({'name': SERVICE_NAME})
    logger.info("Deleting existing {} job in the DB".format(SERVICE_NAME))
# now to create a new config
result = db.apps.insert_one(app_config)

logger.info("Created a new {} job in the DB".format(SERVICE_NAME))
logger.debug(app_config)
