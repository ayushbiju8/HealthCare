from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import APILog
from .serializers import APILogSerializer

class APILogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = APILogSerializer

    def get_queryset(self):
        return APILog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
