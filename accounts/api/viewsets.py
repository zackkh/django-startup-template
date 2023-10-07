from accelerator.builder.decorators import register_viewset
from accelerator.builder.viewsets import (
    GeneratorModelViewSet,
    ReadOnlyGeneratorModelViewSet,
)
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.api.filters import (
    DeviceFilterSet,
    GroupFilterSet,
    NotificationFilterSet,
    PermissionFilterSet,
    SignUpFilterSet,
    UserFilterSet,
)
from accounts.api.serializers import (
    DeviceModelSerializer,
    GroupModelSerializer,
    NotificationModelSerializer,
    PermissionModelSerializer,
    SignUpModelSerializer,
    UserModelSerializer,
)


@register_viewset
class GroupModelViewSet(GeneratorModelViewSet):
    model = GroupModelSerializer.Meta.model
    queryset = model.objects.all()
    serializer_class = GroupModelSerializer
    filterset_class = GroupFilterSet


@register_viewset
class ReadOnlyPermissionModelViewSet(ReadOnlyGeneratorModelViewSet):
    model = PermissionModelSerializer.Meta.model
    queryset = model.objects.all()
    serializer_class = PermissionModelSerializer
    filterset_class = PermissionFilterSet


@register_viewset
class UserModelViewSet(GeneratorModelViewSet):
    model = UserModelSerializer.Meta.model
    queryset = model.objects.all()
    serializer_class = UserModelSerializer
    filterset_class = UserFilterSet


@register_viewset
class SignUpModelViewSet(GeneratorModelViewSet):
    model = SignUpModelSerializer.Meta.model
    queryset = model.objects.all()
    serializer_class = SignUpModelSerializer
    filterset_class = SignUpFilterSet

    @action(methods=["post"], detail=True, url_path="register")
    def register_signup(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.register(request=request)
        return Response(status=status.HTTP_204_NO_CONTENT)


@register_viewset
class ReadOnlyNotificationModelViewSet(ReadOnlyGeneratorModelViewSet):
    model = NotificationModelSerializer.Meta.model
    queryset = model.objects.none()
    serializer_class = NotificationModelSerializer
    filterset_class = NotificationFilterSet

    def get_queryset(self):
        return self.queryset.model._default_manager.filter(
            user=self.request.user
        )


@register_viewset
class ReadOnlyDeviceModelViewSet(ReadOnlyGeneratorModelViewSet):
    model = DeviceModelSerializer.Meta.model
    queryset = model.objects.none()
    serializer_class = DeviceModelSerializer
    filterset_class = DeviceFilterSet

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.model._default_manager.filter(
            user=self.request.user
        )
