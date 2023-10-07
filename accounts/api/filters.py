from accelerator.builder.utils import get_bool_choices, to_bool
from django.db.models import Q
from django_filters import rest_framework as filters

from accounts.models import Device, Group, Notification, Permission, SignUp, User


class GroupFilterSet(filters.FilterSet):
    user = filters.ModelMultipleChoiceFilter(
        field_name="user", queryset=User._default_manager.all()
    )

    unassigned = filters.MultipleChoiceFilter(
        choices=get_bool_choices(),
        field_name="user",
        lookup_expr="isnull",
        method="get_groups",
    )

    def get_groups(self, qs, field, value):
        values = [to_bool(v) for v in value]
        Qs = Q()

        for v in values:
            Qs |= Q(**{f"{field}__isnull": v})

        return qs.filter(Qs)

    class Meta:
        model = Group
        extra_fields = []
        fields = list(model.filterset_fields) + extra_fields


class PermissionFilterSet(filters.FilterSet):
    user = filters.ModelMultipleChoiceFilter(
        field_name="user", queryset=User._default_manager.all()
    )

    group = filters.ModelMultipleChoiceFilter(
        field_name="group", queryset=Group._default_manager.all()
    )

    class Meta:
        model = Permission
        extra_fields = []
        fields = list(model.filterset_fields) + extra_fields


class UserFilterSet(filters.FilterSet):
    groups = filters.ModelMultipleChoiceFilter(
        queryset=Group._default_manager.all(), field_name="groups"
    )
    access_type = filters.MultipleChoiceFilter(
        field_name="access_type",
        label="Access type",
        choices=(
            ("Superuser", "Superuser"),
            ("Staff", "Staff"),
            ("Member", "Member"),
        ),
    )
    is_superuser = filters.MultipleChoiceFilter(
        field_name="is_superuser",
        choices=get_bool_choices(),
        method="get_bools",
    )
    is_staff = filters.MultipleChoiceFilter(
        field_name="is_superuser",
        choices=get_bool_choices(),
        method="get_bools",
    )
    is_active = filters.MultipleChoiceFilter(
        field_name="is_superuser",
        choices=get_bool_choices(),
        method="get_bools",
    )

    unassigned = filters.MultipleChoiceFilter(
        choices=get_bool_choices(),
        field_name="groups",
        lookup_expr="isnull",
        method="get_bools",
    )

    def get_bools(self, qs, field, value):
        values = [to_bool(v) for v in value]
        Qs = Q()

        for v in values:
            Qs |= Q(**{f"{field}__isnull": v})

        return qs.filter(Qs)

    class Meta:
        model = User
        extra_fields = []
        fields = list(model.filterset_fields) + extra_fields


class SignUpFilterSet(filters.FilterSet):
    class Meta:
        model = SignUp
        extra_fields = []
        fields = list(model.filterset_fields) + extra_fields


class NotificationFilterSet(filters.FilterSet):
    class Meta:
        model = Notification
        extra_fields = []
        fields = list(model.filterset_fields) + extra_fields


class DeviceFilterSet(filters.FilterSet):
    class Meta:
        model = Device
        extra_fields = []
        fields = list(model.filterset_fields) + extra_fields
