from rest_framework import serializers
from .models import WearableIntegration, DailyFitnessSummary

class WearableIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WearableIntegration
        fields = '__all__'
        read_only_fields = ['id', 'user']

class DailyFitnessSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyFitnessSummary
        fields = '__all__'
        read_only_fields = ['id', 'user']
