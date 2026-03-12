from django.contrib import admin
from .models import Payment, Expense, AuditLog


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('lease', 'amount', 'due_date', 'paid_date', 'status', 'method')
    list_filter = ('status', 'method')
    search_fields = ('lease__tenant__first_name', 'lease__tenant__last_name', 'reference')
    readonly_fields = ('created_at',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('property', 'category', 'amount', 'date')
    list_filter = ('category',)
    search_fields = ('property__title', 'description')
    readonly_fields = ('created_at',)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'model_name', 'object_id')
    list_filter = ('action', 'model_name')
    search_fields = ('user__username', 'model_name', 'object_id')
    readonly_fields = ('timestamp', 'user', 'action', 'model_name', 'object_id', 'old_value', 'new_value')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
