import time
import logging
import sys

from themeworker import mc, db, SERVICE_NAME
from themeworker.tags import NYT_LABELER_1_0_0_TAG_ID
import themeworker.tasks

logger = logging.getLogger(__name__)

app_config = db.apps.find_one({'name': SERVICE_NAME})
if app_config is None:
    logger.info("No job configured - stopping")
    sys.exit()

query = app_config['query']
stories_to_fetch = app_config['stories_to_fetch']
last_processed_stories_id = app_config['last_processed_stories_id']
retag = app_config['retag']
created_at = app_config['created_at']

logger.info("Fetching {} stories matching:".format(stories_to_fetch))
logger.info("  query: {}".format(query))
logger.info("  last_processed_stories_id: {}".format(last_processed_stories_id))

# Fetch the story texts
start_time = time.time()
stories_with_text = mc.storyList(query, last_processed_stories_id=last_processed_stories_id,
                                 rows=stories_to_fetch, text=True)
text_time = time.time()
logger.debug("    fetched {} story texts in {} seconds".format(len(stories_with_text), text_time - start_time))

if len(stories_with_text) > 0:
    last_processed_stories_id = int(stories_with_text[-1]['processed_stories_id']) + 1

# now toss them into the queue
queued = 0
already_labeled = 0
for story in stories_with_text:
    already_labeled = NYT_LABELER_1_0_0_TAG_ID in story['story_tags']
    if retag or not already_labeled:
        logger.debug("       queued story {}".format(story['stories_id']))
        themeworker.tasks.label_from_story_text.delay(story)
        queued += 1
    else:
        already_labeled += 1

queued_time = time.time()
logger.debug("    queued in {} seconds".format(queued_time - text_time))

# and report back timing on this round
logger.info("    queued {} stories in {} seconds ({} already labelled)".format(queued, time.time() - start_time, already_labeled))

# and save that we've made progress
new_app_config = db.apps.find_one({'name': SERVICE_NAME})
if new_app_config['created_at'] == app_config['created_at']:
    result = db.apps.update_one(
        {"name": SERVICE_NAME},
        {
            "$set": {
                "last_processed_stories_id": last_processed_stories_id
            },
            "$currentDate": {"lastModified": True}
        }
    )
    logger.info("  saved to start at {} next time".format(last_processed_stories_id))
else:
    logger.warn("Job changed underneath worked from {} to {}".format(app_config['query'], new_app_config['query']))

logger.info("Done queueing")

