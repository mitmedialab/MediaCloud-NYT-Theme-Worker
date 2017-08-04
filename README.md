Media Cloud NYT Theme Worker
============================

A service that will pull form a queue of stories with text and tag stories with the results from an install of the
predict-news-labeller.


Dev Installation
----------------

 1. `virtualenv venv` to create your virtualenv
 2. `source venv/bin/activate` - to activate your virtualenv
 3. `pip install -r requirements.txt` - to install the dependencies

+++ Environment Variables

Define these:
 * **RABBITMQ_URL** - `amqp://` path to your RabbitMQ server to pull jobs from
 * **MC_API_KEY** - your mediacloud API key
 * **LABELLER_URL** - URL to your installation of the predict-news-labeller service
 * **SENTRY_DSN** - DSN for logging to sentry

Use
---

Test it locally by running `celery worker -A themeworker -l info`

Enqueue stories using the two queue scripts.
