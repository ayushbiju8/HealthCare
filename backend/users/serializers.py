from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import HealthProfile, EmergencyContact

User = get_user_model()

class HealthProfileSerializer(serializers.ModelSerializer):
    allergies = serializers.ListField(child=serializers.CharField(), required=False)
    chronic_conditions = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = HealthProfile
        fields = ['date_of_birth', 'blood_group', 'height_cm', 'weight_kg', 'allergies', 'chronic_conditions']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    health_profile = HealthProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'health_profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('health_profile', {})
        password = validated_data.pop('password')
        
        validated_data['username'] = validated_data.get('email')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        HealthProfile.objects.create(user=user, **profile_data)
        
        return user

class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ['id', 'name', 'relation', 'phone_number', 'created_at']
        read_only_fields = ['id', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    health_profile = HealthProfileSerializer(read_only=True)
    emergency_contacts = EmergencyContactSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'health_profile', 'emergency_contacts']
