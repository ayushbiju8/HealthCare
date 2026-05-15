from django.contrib import admin
from .models import MedicalReport


@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
	list_display = ('title', 'user', 'report_type', 'processing_status', 'date_issued', 'created_at')
	search_fields = ('title', 'user__email', 'source_hospital', 'file')
	list_filter = ('report_type', 'processing_status', 'date_issued')
	ordering = ('-created_at',)
