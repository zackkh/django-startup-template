from django.conf import settings
from django.urls import include, path
from rest_framework import routers

from accounts.api.viewsets import (
    GroupModelViewSet,
    ReadOnlyDeviceModelViewSet,
    ReadOnlyNotificationModelViewSet,
    ReadOnlyPermissionModelViewSet,
    SignUpModelViewSet,
    UserModelViewSet,
)

router = routers.DefaultRouter() if settings.DEBUG else routers.SimpleRouter()


router.register(
    "groups",
    getattr(GroupModelViewSet, "_method", GroupModelViewSet),
    basename="group",
)

router.register(
    "permissions",
    getattr(
        ReadOnlyPermissionModelViewSet,
        "_method",
        ReadOnlyPermissionModelViewSet,
    ),
    basename="permission",
)

router.register(
    "users",
    getattr(UserModelViewSet, "_method", UserModelViewSet),
    basename="user",
)

router.register(
    "sign_ups",
    getattr(SignUpModelViewSet, "_method", SignUpModelViewSet),
    basename="sign_up",
)

router.register(
    "notifications",
    getattr(
        ReadOnlyNotificationModelViewSet,
        "_method",
        ReadOnlyNotificationModelViewSet,
    ),
    basename="notification",
)

router.register(
    "devices",
    getattr(ReadOnlyDeviceModelViewSet, "_method", ReadOnlyDeviceModelViewSet),
    basename="device",
)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
]
