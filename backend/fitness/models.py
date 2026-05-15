import uuid
from django.db import models
from django.conf import settings

class WearableIntegration(models.Model):
    PROVIDERS = (
        ('APPLE_HEALTH', 'Apple Health'),
        ('GOOGLE_FIT', 'Google Fit'),
        ('GARMIN', 'Garmin'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wearable_integrations')
    provider = models.CharField(max_length=50, choices=PROVIDERS)
    access_token = models.TextField() # Should be encrypted at rest in production
    refresh_token = models.TextField() # Should be encrypted at rest in production
    token_expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_provider_display()} - {self.user.email}"

class DailyFitnessSummary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fitness_summaries')
    date = models.DateField()
    total_steps = models.IntegerField(default=0)
    avg_heart_rate = models.IntegerField(null=True, blank=True)
    calories_burned = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sleep_minutes = models.IntegerField(null=True, blank=True)
    avg_spo2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    raw_payload = models.JSONField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'date'], name='unique_user_date_fitness')
        ]

    def __str__(self):
        return f"Fitness {self.date} - {self.user.email}"
