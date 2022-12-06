from django.urls import path

from .views import restaurants, restaurant_details

urlpatterns = [
    path("", restaurants, name="restaurants"),
    path(
        "<slug:slug>/<int:pk>",
        restaurant_details,
        name="restaurant_details",
    )
]
