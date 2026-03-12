from rest_framework.routers import DefaultRouter

from .views import DocumentViewSet, NotificationViewSet


router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register(r'documents', DocumentViewSet, basename='documents')

urlpatterns = router.urls
