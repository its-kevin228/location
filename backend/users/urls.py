from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet, me_view, register_view


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('auth/register/', register_view, name='auth-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/me/', me_view, name='auth-me'),
]

urlpatterns += router.urls
