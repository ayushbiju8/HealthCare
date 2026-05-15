import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class HealthProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    _allergies_encrypted = models.TextField(blank=True, null=True)
    _chronic_conditions_encrypted = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def allergies(self):
        if not self._allergies_encrypted: return []
        try:
            from cryptography.fernet import Fernet
            from django.conf import settings
            import base64, json
            key = base64.urlsafe_b64encode(settings.SECRET_KEY[:32].ljust(32, '0').encode('utf-8'))
            return json.loads(Fernet(key).decrypt(self._allergies_encrypted.encode()).decode())
        except Exception:
            return []

    @allergies.setter
    def allergies(self, value):
        from cryptography.fernet import Fernet
        from django.conf import settings
        import base64, json
        key = base64.urlsafe_b64encode(settings.SECRET_KEY[:32].ljust(32, '0').encode('utf-8'))
        self._allergies_encrypted = Fernet(key).encrypt(json.dumps(value).encode()).decode()

    @property
    def chronic_conditions(self):
        if not self._chronic_conditions_encrypted: return []
        try:
            from cryptography.fernet import Fernet
            from django.conf import settings
            import base64, json
            key = base64.urlsafe_b64encode(settings.SECRET_KEY[:32].ljust(32, '0').encode('utf-8'))
            return json.loads(Fernet(key).decrypt(self._chronic_conditions_encrypted.encode()).decode())
        except Exception:
            return []

    @chronic_conditions.setter
    def chronic_conditions(self, value):
        from cryptography.fernet import Fernet
        from django.conf import settings
        import base64, json
        key = base64.urlsafe_b64encode(settings.SECRET_KEY[:32].ljust(32, '0').encode('utf-8'))
        self._chronic_conditions_encrypted = Fernet(key).encrypt(json.dumps(value).encode()).decode()

    def __str__(self):
        return f"{self.user.email} - Health Profile"

class EmergencyContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=255)
    relation = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.relation}) - {self.user.email}"
