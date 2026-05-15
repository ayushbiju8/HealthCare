from django.urls import path

from . import views

urlpatterns = [
    path("ocr/", views.OCRView.as_view(), name="ocr"),
    path("health/", views.HealthView.as_view(), name="health"),
]
