from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WearableIntegrationViewSet, DailyFitnessSummaryViewSet

router = DefaultRouter()
router.register(r'integrations', WearableIntegrationViewSet, basename='wearable-integration')
router.register(r'daily-summaries', DailyFitnessSummaryViewSet, basename='daily-summary')

urlpatterns = [
    path('', include(router.urls)),
]
