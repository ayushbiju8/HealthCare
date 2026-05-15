from rest_framework import serializers
from django.utils import timezone
from .models import MedicalReport

class MedicalReportSerializer(serializers.ModelSerializer):
    date_issued = serializers.DateField(default=timezone.localdate)

    class Meta:
        model = MedicalReport
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at',
                            'ocr_extracted_text', 'ai_summary', 'processing_status']
