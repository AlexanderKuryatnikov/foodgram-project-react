from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Subscription


class CustomUserAdmin(UserAdmin):
    model = CustomUser


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'subscribed')
    search_fields = ('user', 'subscribed')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
