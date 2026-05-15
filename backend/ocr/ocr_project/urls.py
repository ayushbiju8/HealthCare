from django.urls import path, include

urlpatterns = [
    path("api/", include("ocr_app.urls")),
]
