from rest_framework import serializers
from .models import HealthMetric

class HealthMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthMetric
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at']
