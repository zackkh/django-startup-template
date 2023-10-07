from accelerator.builder.serializers import FormModelSerializer
from rest_framework import serializers

from accounts.models import Device, Group, Notification, Permission, SignUp, User


class GroupModelSerializer(FormModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = ()


class PermissionModelSerializer(FormModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"
        read_only_fields = ()


class UserModelSerializer(FormModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ()


class SignUpModelSerializer(FormModelSerializer):
    class Meta:
        model = SignUp
        fields = "__all__"
        read_only_fields = ()


class NotificationModelSerializer(FormModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ()


class DeviceModelSerializer(FormModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"
        read_only_fields = ()
