import os
import pwd
import socket
from datetime import timedelta
from tempfile import NamedTemporaryFile
from typing import List
from urllib.request import urlopen

from accelerator.utils import import_callable
from asgiref.sync import async_to_sync
from axes.signals import user_locked_out
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.files import File
from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from accounts.models import Notification, User


def get_os_user_info():
    username = os.getenv("USER")
    user_info = pwd.getpwnam(username)

    return username, user_info


def get_first_last_name(name: List[str]):
    try:
        first_name = name[0]
    except IndexError:
        first_name = "First"
    try:
        last_name = name[-1]
    except IndexError:
        last_name = "Last"

    return first_name, last_name


@receiver(models.signals.post_migrate)
def create_default_user(*args, **kwargs):
    # Get OS user
    if not settings.DEBUG:
        return None

    username, user_info = get_os_user_info()
    full_name = user_info.pw_gecos.split(",")[0]
    first_name, last_name = get_first_last_name(name=full_name.split(" "))

    if not User.objects.filter(username=username).exists():
        image_url = "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=500&h=500&q=80"  # noqa

        user = User.objects.create_superuser(
            is_staff=True,
            is_superuser=True,
            is_active=True,
            username=username,
            email=f"{username}@localhost",
            first_name=first_name,
            last_name=last_name,
            password=username,
        )

        # Download image
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(image_url).read())
        img_temp.flush()

        user.image = File(img_temp)
        user.save()

        try:
            from allauth.account.models import EmailAddress

            email = EmailAddress._default_manager.create(
                user=user, email=user.email, verified=True
            )
            email.set_as_primary()

        except ImportError:
            pass

        print(
            "Credentials:",
            "\n",
            f"\tUsername: {username}",
            "\n",
            f"\tPassword: {username}",
            end="\n",
        )


@receiver(user_locked_out)
def raise_permission_denied(*args, **kwargs):
    from rest_framework.exceptions import PermissionDenied

    AXES_COOLOFF_TIME = getattr(
        settings, "AXES_COOLOFF_TIME", timedelta(seconds=600)
    )
    raise PermissionDenied(
        f"Too many failed login attempts, try again in {AXES_COOLOFF_TIME}."
    )


@receiver(signals.post_save, sender=Notification)
def send_user_notification(sender, instance, created, **kwagrs):
    serializer_class = import_callable(sender.MESSAGE_SERIALIZER)
    serializer = serializer_class(instance, read_only=True)

    channel_layer = get_channel_layer()

    data = {}
    data["data"] = serializer.data
    data["action"] = "update" if not created else "create"
    data["table"] = "notifications"

    try:
        async_to_sync(channel_layer.group_send)(
            "subscribe_to_user_%s_notifications" % instance.pk,
            {"type": "send_notification_message", "message": data},
        )
    except (socket.gaierror, AttributeError):
        pass
