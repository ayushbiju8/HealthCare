from django.contrib import admin
from .models import HealthMetric


@admin.register(HealthMetric)
class HealthMetricAdmin(admin.ModelAdmin):
	list_display = ('user', 'metric_type', 'value_numeric', 'unit', 'measured_at', 'created_at')
	search_fields = ('user__email', 'metric_type')
	list_filter = ('metric_type',)
	ordering = ('-measured_at',)
