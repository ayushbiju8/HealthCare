import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import HealthProfile

User = get_user_model()

# Create superuser
if not User.objects.filter(email='ayushbiju8').exists():
    User.objects.create_superuser(email='ayushbiju8', password='ayushbiju8', username='ayushbiju8')
    print("Superuser ayushbiju8 created successfully.")
else:
    print("Superuser ayushbiju8 already exists.")

# Create normal user
normal_email = 'testuser@example.com'
if not User.objects.filter(email=normal_email).exists():
    user = User.objects.create_user(email=normal_email, password='testpass123', username=normal_email, first_name='Test', last_name='User')
    HealthProfile.objects.create(
        user=user,
        date_of_birth='1990-01-01',
        blood_group='O+',
        height_cm=180.5,
        weight_kg=75.0,
        allergies=['Peanuts', 'Penicillin'],
        chronic_conditions=['Asthma']
    )
    print("Normal user testuser@example.com created with encrypted Health Profile.")
else:
    print("Normal user testuser@example.com already exists.")
