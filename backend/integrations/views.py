from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import APILog
from .serializers import APILogSerializer

class APILogViewSet(viewsets.ReadOnlyModelViewSet):
    """APILog has no user FK — it's an internal integration audit log."""
    permission_classes = [IsAuthenticated]
    serializer_class = APILogSerializer

    def get_queryset(self):
        return APILog.objects.all().order_by('-created_at')
