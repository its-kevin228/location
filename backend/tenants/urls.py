from rest_framework.routers import DefaultRouter

from .views import LeaseViewSet, TenantViewSet


router = DefaultRouter()
router.register(r'tenants', TenantViewSet, basename='tenants')
router.register(r'leases', LeaseViewSet, basename='leases')

urlpatterns = router.urls
