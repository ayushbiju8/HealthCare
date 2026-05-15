from django.urls import path

from . import views

urlpatterns = [
    path("text/", views.MedicineTextView.as_view(), name="medicine-text"),
    path("image/", views.MedicineImageView.as_view(), name="medicine-image"),
    path("health/", views.HealthView.as_view(), name="health"),
]
