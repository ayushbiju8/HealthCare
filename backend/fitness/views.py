from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import WearableIntegration, DailyFitnessSummary
from .serializers import WearableIntegrationSerializer, DailyFitnessSummarySerializer

class WearableIntegrationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WearableIntegrationSerializer

    def get_queryset(self):
        return WearableIntegration.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DailyFitnessSummaryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DailyFitnessSummarySerializer

    def get_queryset(self):
        return DailyFitnessSummary.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
