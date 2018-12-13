import logging

from themeworker import mc, config
from themeworker.tasks import label_from_story_text

logger = logging.getLogger(__name__)

# debug logging
logger.info("Starting to tag stories matching a query:")
query = config.get('query')
logger.info("  query: {}".format(query))
filter_query = config.get('filter_query')
logger.info("  filter_query: {}".format(filter_query))
processed_stories_id = config.get('processed_stories_id')
logger.info("  processed_stories_id: {}".format(processed_stories_id))
stories_per_page = config.get('stories_per_page')
logger.info("  stories_per_page: {}".format(stories_per_page))

# page through stories matching query, starting at specific processed_stories_id
count = mc.storyCount(query, filter_query)['count']
logger.info("Stories remaining: {}".format(count))
logger.info("  fetching {} stories:".format(stories_per_page))
page = mc.storyList(query, filter_query, last_processed_stories_id=processed_stories_id,
                    rows=stories_per_page, text=True)
last_processed_stories_id = page[-1]['processed_stories_id']
queued_stories = 0
for story in page:
    if story['metadata']['nyt_themes_version'] is None:
        label_from_story_text.delay(story)
        queued_stories += 1
logger.info("  queued {} stories".format(queued_stories))
config.set('processed_stories_id', last_processed_stories_id)
logger.info("  processed_stories_id: {}".format(last_processed_stories_id))
