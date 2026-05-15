from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import HealthMetric
from .serializers import HealthMetricSerializer

class HealthMetricViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HealthMetricSerializer

    def get_queryset(self):
        return HealthMetric.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
