from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    EquipmentViewSet,
    PropertyPhotoViewSet,
    PropertyTypeViewSet,
    PropertyViewSet,
    SaleViewSet,
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'property-types', PropertyTypeViewSet, basename='property-types')
router.register(r'equipments', EquipmentViewSet, basename='equipments')
router.register(r'properties', PropertyViewSet, basename='properties')
router.register(r'property-photos', PropertyPhotoViewSet, basename='property-photos')
router.register(r'sales', SaleViewSet, basename='sales')

urlpatterns = router.urls
