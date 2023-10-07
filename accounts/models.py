from accelerator.builder.mixins import AcceleratorMixin
from accelerator.cache.mixins import CacheMixin
from accelerator.models import BaseMixin, TimestampMixin, fields
from accelerator.users import UserMixin
from allauth.account.adapter import get_adapter
from allauth.account.signals import user_logged_in as allauth_user_logged_in
from allauth.account.utils import send_email_confirmation, setup_user_email
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as _Group
from django.contrib.auth.models import Permission as _Permission
from django.contrib.auth.models import UserManager as _UserManager
from django.contrib.auth.signals import user_logged_in as django_user_logged_in
from django.core import exceptions
from django.db import models, transaction
from django.db.models.query import QuerySet
from django.db.utils import InternalError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Group(_Group, BaseMixin, TimestampMixin, CacheMixin, AcceleratorMixin):
    SERIALIZE_M2M = True

    description = fields.TextNullField(_("description"), max_length=500)


class _BaseMixin(BaseMixin):
    class Meta:
        abstract = True

    uuid = None
    is_localhost = None


class Permission(_Permission, _BaseMixin, CacheMixin, AcceleratorMixin):
    FORCE_CACHE = True
    VIEWSET_READONLY = True

    @classmethod
    def cache_filter_kwargs(cls):
        return {"content_type__app_label__in": ["accounts", "store", "flow"]}

    class Meta:
        proxy = True
        managed = False

    uuid = None
    is_localhost = None


class UserManager(_UserManager):
    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .annotate(
                access_type=models.Case(
                    models.When(
                        models.Q(is_superuser=True),
                        then=models.Value("Superuser"),
                    ),
                    models.When(
                        models.Q(is_superuser=False, is_staff=True),
                        then=models.Value("Staff"),
                    ),
                    default=models.Value("Member"),
                    output_field=models.TextField(),
                )
            )
        )


class User(AbstractUser, BaseMixin, CacheMixin, AcceleratorMixin):
    EXTRA_SERIALIZER_FIELDS = ["name", "label", "access_type"]
    SERIALIZE_M2M = True

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    date_joined = models.DateTimeField(
        _("date joined"), blank=True, default=timezone.now
    )

    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    groups = models.ManyToManyField(
        settings.AUTH_GROUP_MODEL,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
    )

    name = models.TextField(_("name"), blank=True, editable=False)

    PERMANENT_USERS = ["watcher", "deleted"]

    # managers
    objects = UserManager()

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        try:
            super().delete(*args, **kwargs)
        except Exception as e:
            if isinstance(e, InternalError):
                raise exceptions.ValidationError(str(e))
            else:
                raise e

    def save(self, *args, **kwargs):
        try:
            self.name = self.get_full_name()
            super().save(*args, **kwargs)
        except Exception as e:
            if isinstance(e, InternalError):
                # Handle the InternalError here
                raise exceptions.ValidationError(str(e))
            else:
                # Re-raise the exception if it's not an InternalError
                raise e


def unique_sign_up_email(value):
    if get_user_model()._default_manager.filter(email=value).exists():
        raise forms.ValidationError(
            _("A user with this email already exists.")
        )


def unique_sign_up_username(value):
    if get_user_model()._default_manager.filter(username=value).exists():
        raise forms.ValidationError(
            _("A user with this username already exists.")
        )


class SignUp(BaseMixin, TimestampMixin, AcceleratorMixin):
    class Meta:
        verbose_name = _("sign up request")
        verbose_name_plural = _("sign up requests")

    is_verified = models.BooleanField(_("verified"), default=False)
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    username = models.CharField(
        _("username"),
        unique=True,
        max_length=50,
        validators=[unique_sign_up_username],
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        max_length=254,
        validators=[unique_sign_up_email],
    )

    error = fields.TextNullField(_("error"))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_verified and self.request:
            self.register(request=self.request)

    @property
    def user_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
        }

    def register(self, request):
        self.request = request
        success = None

        with transaction.atomic():
            try:
                adapter = get_adapter()
                user = adapter.new_user(request)
                self.cleaned_data = self.user_dict
                user = adapter.save_user(request, user, self, commit=False)
                user.save()
                user.set_unusable_password()
                setup_user_email(request, user, [])
                success = user
            except Exception as e:
                self.error = str(e)
                self.save()

        if success:
            send_email_confirmation(request=request, user=success, signup=True)
            self.delete()


class Notification(BaseMixin, TimestampMixin, UserMixin, AcceleratorMixin):
    MESSAGE_SERIALIZER = (
        "accounts.consumers.serializers.NotificationSerializer"
    )
    VIEWSET_READONLY = True

    class Meta:
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")

    INFO, WARNING, DANGER = "Information", "Warning", "Danger"
    LEVEL_CHOICES = (
        (INFO, INFO),
        (WARNING, WARNING),
        (DANGER, DANGER),
    )

    title = models.TextField(_("title"))
    level = models.CharField(
        _("level"), choices=LEVEL_CHOICES, default=INFO, max_length=50
    )
    content = models.TextField(_("content"))


class Device(BaseMixin, TimestampMixin, UserMixin, AcceleratorMixin):
    VIEWSET_READONLY = True

    class Meta:
        verbose_name = _("device")
        verbose_name_plural = _("devices")

    user_agent = fields.TextNullField(_("user agent"))
    ip_address = models.GenericIPAddressField(
        _("ip address"), blank=True, null=True, unpack_ipv4=True
    )


NEW_DEVICE_CONTENT = """A new sign-in has been detected:

User-agent: {user_agent}
IP: {ip_address}

You can ignore this email if it was you;
If not, reset your password now.

"""


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def save_user_agent_data(sender, request, user, **kwargs):
    user_agent = request.META.get("HTTP_USER_AGENT")
    # Use REMOTE_ADDR for the client's IP address
    ip_address = get_client_ip(request)

    if (
        user_agent
        and not user.device_set.filter(
            user_agent=user_agent, ip_address=ip_address
        ).exists()
    ):
        user.email_user(
            subject="New device detected!",
            message=NEW_DEVICE_CONTENT.format(
                user_agent=user_agent, ip_address=ip_address
            ),
            from_email=getattr(settings, "EMAIL_HOST_USER", "root@localhost"),
        )
        user.device_set.create(user_agent=user_agent, ip_address=ip_address)


allauth_user_logged_in.connect(save_user_agent_data)
django_user_logged_in.connect(save_user_agent_data)
