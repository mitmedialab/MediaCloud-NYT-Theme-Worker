import sys
import logging

from themeworker import mc
from themeworker.tasks import label_from_story_text

logger = logging.getLogger(__name__)

if len(sys.argv) != 2:
    logger.error("Please specify a topic id")
    sys.exit()

TOPIC_ID = sys.argv[1]
logger.info("Processing topic {}".format(TOPIC_ID))

# debug logging
topic = mc.topic(TOPIC_ID)
logger.info("  {}".format(topic['name']))
total_stories = mc.topicStoryCount(TOPIC_ID)['count']
logger.info("  {} stories".format(total_stories))

# page throug stories in topic
link_id = None
more_stories = True
while more_stories:
    # grab one page of stories
    story_page = mc.topicStoryList(TOPIC_ID, link_id=link_id, limit=500)
    # now get the stories with the text
    story_ids = [str(s['stories_id']) for s in story_page['stories']]
    query = "stories_id:({})".format(" ".join(story_ids))
    stories_with_text = mc.storyList(query, text=True)
    for s in stories_with_text:
        label_from_story_text.delay(s)
    # and get ready for the next page
    if 'next' in story_page['link_ids']:
        link_id = story_page['link_ids']['next']
    else:
        more_stories = False
