from django.contrib import admin
from .models import WearableIntegration, DailyFitnessSummary


@admin.register(WearableIntegration)
class WearableIntegrationAdmin(admin.ModelAdmin):
	list_display = ('user', 'provider', 'is_active', 'token_expires_at')
	search_fields = ('user__email',)
	list_filter = ('provider', 'is_active')
	ordering = ('-token_expires_at',)


@admin.register(DailyFitnessSummary)
class DailyFitnessSummaryAdmin(admin.ModelAdmin):
	list_display = ('user', 'date', 'total_steps', 'avg_heart_rate', 'avg_spo2')
	search_fields = ('user__email',)
	list_filter = ('date',)
	ordering = ('-date',)
