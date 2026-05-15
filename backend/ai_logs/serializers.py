from rest_framework import serializers
from .models import AILog

class AILogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AILog
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at']
