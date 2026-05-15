from django.contrib import admin
from .models import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
	list_display = ('title', 'user', 'type', 'due_datetime', 'is_active', 'created_at')
	search_fields = ('title', 'user__email')
	list_filter = ('type', 'is_active')
	ordering = ('-due_datetime',)
