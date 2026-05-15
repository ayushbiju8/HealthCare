from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import APILogViewSet

router = DefaultRouter()
router.register(r'logs', APILogViewSet, basename='api-log')

urlpatterns = [
    path('', include(router.urls)),
]
