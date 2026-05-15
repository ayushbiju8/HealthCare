from django.contrib import admin
from .models import AILog


@admin.register(AILog)
class AILogAdmin(admin.ModelAdmin):
	list_display = ('context', 'user', 'tokens_used', 'created_at')
	search_fields = ('user__email', 'context')
	list_filter = ('context',)
	ordering = ('-created_at',)
