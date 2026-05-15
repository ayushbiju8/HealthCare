from django.contrib import admin
from .models import User, HealthProfile, EmergencyContact


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')
	search_fields = ('email', 'username', 'first_name', 'last_name')
	list_filter = ('is_active', 'is_staff', 'is_superuser')
	ordering = ('email',)


@admin.register(HealthProfile)
class HealthProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'blood_group', 'height_cm', 'weight_kg', 'updated_at')
	search_fields = ('user__email', 'user__username')
	list_filter = ('blood_group',)
	ordering = ('-updated_at',)


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
	list_display = ('name', 'relation', 'phone_number', 'user', 'created_at')
	search_fields = ('name', 'relation', 'phone_number', 'user__email')
	list_filter = ('relation',)
	ordering = ('-created_at',)
