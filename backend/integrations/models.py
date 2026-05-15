import uuid
from django.db import models

class APILog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    integration_name = models.CharField(max_length=255)
    endpoint = models.CharField(max_length=500)
    status_code = models.IntegerField(null=True, blank=True)
    request_payload = models.JSONField(null=True, blank=True)
    response_payload = models.JSONField(null=True, blank=True)
    duration_ms = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.integration_name} API Call - {self.status_code}"
