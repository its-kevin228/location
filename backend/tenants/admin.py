from django.contrib import admin
from .models import Tenant, Lease


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'phone', 'profession', 'user')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('profession',)
    readonly_fields = ('created_at',)


@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'property', 'start_date', 'end_date', 'rent_amount', 'status')
    list_filter = ('status',)
    search_fields = ('tenant__first_name', 'tenant__last_name', 'property__title')
    readonly_fields = ('created_at', 'updated_at')
