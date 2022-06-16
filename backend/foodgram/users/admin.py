from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Subscribtion


class CustomUserAdmin(UserAdmin):
    model = CustomUser


class SubscribtionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'subscribed')
    search_fields = ('user', 'subscribed')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subscribtion, SubscribtionAdmin)
