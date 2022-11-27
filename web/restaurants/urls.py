from django.urls import path

from .views import restaurants

urlpatterns = [
    path("", restaurants, name="restaurants"),

]
