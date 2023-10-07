from django.apps import AppConfig
from django.db import models

from accounts.db import (
    prevent_permanent_users_deletion_trigger,
    prevent_permanent_users_update_trigger,
)


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self) -> None:
        try:
            from accounts import signals
        except ImportError:
            pass
        models.signals.post_migrate.connect(
            prevent_permanent_users_deletion_trigger, sender=self
        )

        models.signals.post_migrate.connect(
            prevent_permanent_users_update_trigger, sender=self
        )
        return super().ready()
