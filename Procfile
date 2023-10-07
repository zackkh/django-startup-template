django: daphne core.asgi:application -b 0.0.0.0 -p 8000
worker: celery -A core worker --beat
flower: celery -A core flower