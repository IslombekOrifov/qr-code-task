from django.contrib import admin

from .models import (
    TelegramUser, Pricing,
    UserQrCode
)


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'full_name')
    list_display_links = ('id', 'user_id', 'full_name')
    ordering = ('id', 'user_id', 'full_name')
    search_fields = ['user_id', 'full_name']


@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    list_display = ('id', 'price_per_hour', 'created_at', 'updated_at')


@admin.register(UserQrCode)
class UserQrCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_active', 'cost')
    ordering = ('id', 'user', 'is_active')
    search_fields = ['user',]
