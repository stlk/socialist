web: gunicorn socialist.wsgi --log-file -
worker: celery worker --app=console.tasks.app --concurrency 2 --loglevel=info
