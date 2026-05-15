from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import AILog
from .serializers import AILogSerializer

class AILogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AILogSerializer

    def get_queryset(self):
        return AILog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
