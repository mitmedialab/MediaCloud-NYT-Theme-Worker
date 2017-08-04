import time
import logging
import sys

from themeworker import mc
from themeworker.tags import NYT_LABELER_1_0_0_TAG_ID
import themeworker.tasks

RELABEL = True
STORIES_AT_A_TIME = 1000

logger = logging.getLogger(__name__)

# load task-specific
if len(sys.argv) is not 2:
    logger.error("You have to give this script a topic id")
    sys.exit()

topic_id = str(sys.argv[1])
logger.info("Fetching all stories from Topic #{}".format(topic_id))

more_stories = True
next_link_id = None

# best to just go through all the stories in an open loop and fill up the redis queue
while more_stories:

    start_time = time.time()
    # Fetch some story ids and queue them up to get text (because topicStoryList doesn't support text option)
    logger.info("Fetch link_id {}".format(next_link_id))
    stories = mc.topicStoryList(topic_id, link_id=next_link_id, limit=STORIES_AT_A_TIME)
    story_ids = [story['stories_id'] for story in stories['stories'] if story['language'] in [None,'en']]
    logger.debug("  fetched {} stories ({} in english)".format(len(stories['stories']),len(story_ids)))
    if 'next' in stories['link_ids']:
        next_link_id = stories['link_ids']['next']
        more_stories = True
    else:
        more_stories = False
    story_time = time.time()
    logger.debug("    fetched stories in {} seconds".format(story_time - start_time))

    # now we need to fetch text
    logger.debug("  fetching text")
    story_ids = [str(sid) for sid in story_ids]
    stories_with_text = mc.storyList("stories_id:("+" ".join(story_ids)+")", text=True, rows=STORIES_AT_A_TIME)
    text_time = time.time()
    logger.debug("    fetched {} text in {} seconds".format(len(stories_with_text), text_time - story_time))

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

logger.info("Done queueing entire topic")
