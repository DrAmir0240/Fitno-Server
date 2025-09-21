from django.contrib import admin

from communications.models import Ticket, Notification, Announcement


# Register your models here.
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    class Meta:
        list_display = '__all__'
        search_fields = '__all__'