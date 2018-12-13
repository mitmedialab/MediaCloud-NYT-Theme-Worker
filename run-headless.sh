source venv/bin/activate
nohup celery worker -A themeworker -l info > celery.log &
