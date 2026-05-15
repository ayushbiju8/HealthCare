from rest_framework import serializers
from django.utils import timezone
from .models import HealthMetric

class HealthMetricSerializer(serializers.ModelSerializer):
    measured_at = serializers.DateTimeField(default=timezone.now)

    class Meta:
        model = HealthMetric
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at']
