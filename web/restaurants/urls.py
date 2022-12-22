from django.urls import path

from .views import restaurants, restaurants_map, restaurant_details, restaurant_map

urlpatterns = [
    path("", restaurants, name="restaurants"),
    path("mapa_restaracji/", restaurants_map, name="restaurants_map"),
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
