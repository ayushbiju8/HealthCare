import uuid
from django.db import models
from django.conf import settings
from records.models import MedicalReport

class HealthMetric(models.Model):
    METRIC_TYPES = (
        ('GLUCOSE', 'Glucose'),
        ('CHOLESTEROL', 'Cholesterol'),
        ('BP_SYS', 'Blood Pressure (Systolic)'),
        ('BP_DIA', 'Blood Pressure (Diastolic)'),
        ('HEART_RATE', 'Heart Rate'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='metrics')
    report = models.ForeignKey(MedicalReport, on_delete=models.SET_NULL, null=True, blank=True, related_name='extracted_metrics')
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES)
    value_numeric = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    measured_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'metric_type', 'measured_at']),
        ]
        constraints = [
            models.CheckConstraint(condition=models.Q(value_numeric__gt=0), name='value_numeric_positive')
        ]

    def __str__(self):
        return f"{self.get_metric_type_display()} - {self.value_numeric} {self.unit} ({self.user.email})"
