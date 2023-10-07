from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from accounts.models import Device, Group, Notification, User, _Group

# Register your models here.


@admin.register(User)
class UserAdmin(_UserAdmin):
    pass


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["title", "user"]
    list_select_related = ["user"]
    list_filter = ["user"]


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ["user_agent", "ip_address", "user"]
    list_select_related = ["user"]
    list_filter = ["user"]


admin.site.unregister(_Group)
admin.site.register(Group)
