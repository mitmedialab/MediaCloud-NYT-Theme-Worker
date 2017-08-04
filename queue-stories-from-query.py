import time
import logging
import sys

from themeworker import mc
from themeworker.tags import NYT_LABELER_1_0_0_TAG_ID
import themeworker.tasks

RELABEL = True

logger = logging.getLogger(__name__)

# load task-specific
if len(sys.argv) is not 3:
    logger.error("You have to give this script a query and the number of stories to fetch")
    sys.exit()

query = str(sys.argv[1])
stories_to_fetch = int(sys.argv[2])
last_processed_stories_id = 0

logger.info("Fetching {} stories matching:".format(stories_to_fetch))
logger.info("  query: {}".format(query))

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
    if RELABEL or not already_labeled:
        themeworker.tasks.label_from_story_text.delay(story)
        queued += 1
    else:
        already_labeled += 1

queued_time = time.time()
logger.debug("    queued in {} seconds".format(queued_time - text_time))

# and report back timing on this round
logger.info("    queued {} stories in {} seconds ({} already labelled)".format(queued, time.time() - start_time, already_labeled))

# and save that we've made progress
logger.info("  can start at {} next time".format(last_processed_stories_id))

logger.info("Done queueing")
