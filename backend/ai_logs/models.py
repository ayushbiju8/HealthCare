import uuid
from django.db import models
from django.conf import settings

class AILog(models.Model):
    CONTEXT_CHOICES = (
        ('OCR_SUMMARY', 'OCR Summary'),
        ('GENERAL_CHAT', 'General Chat'),
        ('HEALTH_INSIGHT', 'Health Insight'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_logs')
    context = models.CharField(max_length=50, choices=CONTEXT_CHOICES)
    prompt = models.TextField()
    response = models.TextField()
    tokens_used = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AILog {self.get_context_display()} - {self.created_at}"
