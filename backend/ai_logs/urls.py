from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AILogViewSet

router = DefaultRouter()
router.register(r'logs', AILogViewSet, basename='ai-log')

urlpatterns = [
    path('', include(router.urls)),
]
