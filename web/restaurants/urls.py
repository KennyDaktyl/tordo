from django.urls import path

from .views import restaurants, restaurant_details, restaurant_map

urlpatterns = [
    path("", restaurants, name="restaurants"),
    path(
        "<slug:slug>/<int:pk>",
        restaurant_details,
        name="restaurant_details",
    ),
    path(
        "<slug:slug>/mapa/<int:pk>",
        restaurant_map,
        name="restaurant_map",
    ),
]
