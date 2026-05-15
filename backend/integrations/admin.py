from django.contrib import admin
from .models import APILog


@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
	list_display = ('integration_name', 'endpoint', 'status_code', 'duration_ms', 'created_at')
	search_fields = ('integration_name', 'endpoint')
	list_filter = ('status_code',)
	ordering = ('-created_at',)
