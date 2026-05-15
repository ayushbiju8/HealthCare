from rest_framework import serializers
from .models import MedicalReport

class MedicalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalReport
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
