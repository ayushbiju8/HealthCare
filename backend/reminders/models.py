import uuid
from django.db import models
from django.conf import settings

class Reminder(models.Model):
    TYPES = (
        ('MEDICINE', 'Medicine'),
        ('VACCINATION', 'Vaccination'),
        ('CHECKUP', 'Checkup'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reminders')
    type = models.CharField(max_length=50, choices=TYPES)
    title = models.CharField(max_length=255)
    due_datetime = models.DateTimeField()
    recurrence_rule = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_triggered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.email}"
