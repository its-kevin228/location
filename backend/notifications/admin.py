from django.contrib import admin
from .models import Notification, Document


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'title', 'is_read', 'created_at')
    list_filter = ('type', 'is_read')
    search_fields = ('user__username', 'title', 'message')
    readonly_fields = ('created_at',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('type', 'lease', 'payment', 'generated_at', 'sent_at')
    list_filter = ('type',)
    search_fields = ('lease__tenant__first_name', 'lease__tenant__last_name')
    readonly_fields = ('generated_at',)
