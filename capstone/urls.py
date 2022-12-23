from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # API Routes
    path("pixels", views.pixels_app, name="pixels"),
    path("spectral_info", views.spectral_info, name="spectral_info"),
]
