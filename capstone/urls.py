from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pixels", views.pixels_app, name="pixels"),

    # API Routes
    # path("saved_images", views.get_saved_images, name="saved_images"),
]
