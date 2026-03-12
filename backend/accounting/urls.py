from rest_framework.routers import DefaultRouter

from .views import AuditLogViewSet, ExpenseViewSet, PaymentViewSet


router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'expenses', ExpenseViewSet, basename='expenses')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-logs')

urlpatterns = router.urls
