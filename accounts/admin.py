from django.contrib import admin

from accounts.models import APIKey, PlatformSettings, PlatformManager, Customer, User, GymManager


# Register your models here.

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'


@admin.register(PlatformSettings)
class PlatformSettingsAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'


@admin.register(PlatformManager)
class PlatformManagerAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'


@admin.register(GymManager)
class GymManagerAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'
