from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicalReportViewSet, OCRView

router = DefaultRouter()
router.register(r'reports', MedicalReportViewSet, basename='medical-report')

urlpatterns = [
    path('ocr/', OCRView.as_view(), name='medical-report-ocr'),
    path('', include(router.urls)),
]
