import uuid
from django.db import models
from django.conf import settings

class MedicalReport(models.Model):
    REPORT_TYPES = (
        ('UPLOAD_PDF', 'Uploaded PDF'),
        ('UPLOAD_IMG', 'Uploaded Image'),
        ('API_FETCH', 'API Fetch'),
        ('OCR_SCAN', 'OCR Scan'),
    )

    PROCESSING_STATUSES = (
        ('PENDING', 'Pending'),
        ('PROCESSED', 'Processed'),
        ('FAILED', 'Failed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    date_issued = models.DateField()
    source_hospital = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to='reports/', null=True, blank=True)
    raw_api_payload = models.JSONField(null=True, blank=True)
    ocr_extracted_text = models.TextField(null=True, blank=True)
    ai_summary = models.TextField(null=True, blank=True)
    processing_status = models.CharField(max_length=50, choices=PROCESSING_STATUSES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'date_issued']),
            models.Index(fields=['processing_status']),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.email}"
