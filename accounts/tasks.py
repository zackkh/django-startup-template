from celery import shared_task
from django.conf import settings
from django.utils.module_loading import import_string


@shared_task
def update_rates(backend=settings.EXCHANGE_BACKEND, **kwargs):
    backend = import_string(backend)()
    backend.update_rates(**kwargs)
