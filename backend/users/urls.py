from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, UserProfileViewSet, HealthProfileViewSet, EmergencyContactViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='user-profile')
router.register(r'health-profile', HealthProfileViewSet, basename='health-profile')
router.register(r'emergency-contacts', EmergencyContactViewSet, basename='emergency-contacts')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
