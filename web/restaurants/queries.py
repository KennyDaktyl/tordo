from web.models.restaurants import FilterFood, FilterAdvantage, Tag
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

from django.conf import settings
from typing import List
from django.db.models import Count
from django.db.models.query import QuerySet
from web.models.restaurants import Restaurant

FilterMapping = {
    "filter_foods": FilterFood,
    "filter_advantages": FilterAdvantage,
    "filter_tags": Tag,
}


def get_object_list_by_distance(request, object_list, user_location):
    longitude, latitude, place_name = (
        user_location["longitude"],
        user_location["latitude"],
        user_location["place_name"],
    )
    user_location = Point(float(longitude), float(latitude), srid=4326)
    object_list = (
        object_list.annotate(distance=Distance("location", user_location))
        .filter(location__distance_lte=(user_location, D(km=settings.MAX_DISTANCE)))
        .order_by("name")
    )
    return object_list


def get_object_list_sorted(request, object_list):
    a = request.session["sorted"]
    if request.session["sorted"] == "name":
        return object_list.order_by("name")

    if request.session["sorted"] == "distance":
        if request.session.get("user_location"):
            return object_list.order_by("distance")
        else:
            request.session["sorted"] = "name"
            return object_list.order_by("name")

    if request.session["sorted"] == "earliest_open":
        object_list_not_None = [
            obj for obj in object_list if obj.from_hour is not None]
        object_list_sorted = sorted(
            object_list_not_None, key=lambda obj: obj.from_hour)
        restaurant_queryset = Restaurant.objects.filter(
            pk__in=[r.pk for r in object_list_sorted])
        return restaurant_queryset

    if request.session["sorted"] == "longest_open":
        object_list_not_None = [
            obj for obj in object_list if obj.to_hour is not None]
        object_list_sorted = sorted(
            object_list_not_None, key=lambda obj: obj.to_hour, reverse=True
        )
        restaurant_queryset = Restaurant.objects.filter(
            pk__in=[r.pk for r in object_list_sorted])
        return restaurant_queryset

    return object_list


def get_object_list_filtered(request, restaurants, reset=False):
    keys = list(FilterMapping.keys())
    restaurants_foods = []
    restaurants_advantages = []

    if request.session.get(keys[0]):
        if reset:
            del request.session[keys[0]]
        else:
            restaurants_foods = restaurants
            for id in request.session.get(keys[0]):
                restaurants_foods = restaurants_foods.filter(
                    filter_foods__id__in=[id])
            if not restaurants_foods:
                return restaurants_foods

    if request.session.get(keys[1]):
        if reset:
            del request.session[keys[1]]
        else:
            restaurants_advantages = restaurants
            for id in request.session.get(keys[1]):
                restaurants_advantages = restaurants_advantages.filter(
                    filter_advantages__id__in=[id])
            restaurants_advantages = restaurants_advantages
            if not restaurants_advantages:
                return restaurants_advantages

    if isinstance(restaurants_foods, QuerySet) and isinstance(
        restaurants_advantages, QuerySet
    ):
        restaurants = restaurants_foods & restaurants_advantages
    else:
        if isinstance(restaurants_foods, QuerySet) and isinstance(
            restaurants_advantages, list
        ):
            restaurants = restaurants_foods
        elif isinstance(restaurants_foods, list) and isinstance(
            restaurants_advantages, QuerySet
        ):
            restaurants = restaurants_advantages

    if request.session.get(keys[2]):
        if reset:
            del request.session[keys[2]]
        else:
            restaurants_tags = restaurants.filter(
                tags__id__in=request.session.get(keys[2])
            ).distinct()
            if not restaurants_tags:
                return restaurants_tags

    return restaurants


def get_object_list_search(request, object_list):
    search = (
        request.GET.get("search")
        if request.GET.get("search")
        else request.session.get("search")
    )
    request.session["search"] = search
    object_list = __restaurants_search(search, object_list)

    if request.session["sorted"] == "name":
        return sorted(object_list, key=lambda d: d.name)

    if request.session["sorted"] == "distance":
        if request.session.get("user_location"):
            return sorted(object_list, key=lambda d: d.distance)
        else:
            request.session["sorted"] = "name"
            return sorted(object_list, key=lambda d: d.name)

    if request.session["sorted"] == "earliest_open":
        object_list_not_None = [
            obj for obj in object_list if obj.from_hour is not None]
        object_list_sorted = sorted(
            object_list_not_None, key=lambda obj: obj.from_hour)
        return object_list_sorted

    if request.session["sorted"] == "longest_open":
        object_list_not_None = [
            obj for obj in object_list if obj.from_hour is not None]
        object_list_sorted = sorted(
            object_list_not_None, key=lambda obj: obj.from_hour)
        return object_list_sorted

    return object_list


def __restaurants_search(search, object_list):
    restaurants_search = object_list.filter(name__icontains=search)
    products_search = []
    for restaurant in object_list:
        categories = []
        for category in restaurant.categories:
            products_filtered = category.products.filter(
                name__icontains=search)
            if products_filtered:
                category.products_filtered = products_filtered
                categories.append(category)
        if categories:
            restaurant.categories_filtered = categories
            products_search.append(restaurant)
    return set(products_search) | set(restaurants_search)
