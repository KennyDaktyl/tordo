from web.models.restaurants import FilterFood, FilterAdvantage, Tag
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

from django.conf import settings
from typing import List
from django.db import models
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
    
    if request.session["sorted"] == "name":
        return object_list.order_by("name")
    
    if request.session["sorted"] == "distance":
        return object_list.order_by("distance")

    if request.session["sorted"] == "earliest_open":
        object_list_not_None = [obj for obj in object_list if obj.from_hour is not None]
        object_list_sorted = sorted(object_list_not_None, key=lambda obj: obj.from_hour)
        return object_list_sorted

    if request.session["sorted"] == "longest_open":
        object_list_not_None = [obj for obj in object_list if obj.to_hour is not None]
        object_list_sorted = sorted(object_list_not_None, key=lambda obj: obj.to_hour, reverse=True)
        return object_list_sorted
    return object_list


def get_object_list_filtered(request, object_list, reset=False):
    keys = list(FilterMapping.keys())
    if request.session.get(keys[0]):
        if reset:
            del request.session[keys[0]]
        else:
            object_list = object_list.filter(
                filter_foods__id__in=request.session.get(keys[0])
            ).distinct()
    if request.session.get(keys[1]):
        if reset:
            del request.session[keys[1]]
        else:
            object_list = object_list.filter(
                filter_advantages__id__in=request.session.get(keys[1])
            ).distinct()
    if request.session.get(keys[2]):
        if reset:
            del request.session[keys[2]]
        else:
            object_list = object_list.filter(
                tags__id__in=request.session.get(keys[2])
            ).distinct()
    return object_list


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
        return sorted(object_list, key=lambda d: d.distance)
    
    if request.session["sorted"] == "earliest_open":
        object_list_not_None = [obj for obj in object_list if obj.from_hour is not None]
        object_list_sorted = sorted(object_list_not_None, key=lambda obj: obj.from_hour)
        return object_list_sorted

    if request.session["sorted"] == "longest_open":
        object_list_not_None = [obj for obj in object_list if obj.from_hour is not None]
        object_list_sorted = sorted(object_list_not_None, key=lambda obj: obj.from_hour)
        return object_list_sorted

    return object_list


def __restaurants_search(search, object_list):
        restaurants_search = object_list.filter(name__icontains=search)
        products_search = []
        for restaurant in object_list:
            categories = []
            for category in restaurant.categories:
                products_filtered = category.products.filter(name__icontains=search)
                if products_filtered:
                    category.products_filtered = products_filtered
                    categories.append(category)
            if categories:
                restaurant.categories_filtered = categories
                products_search.append(restaurant)
        return set(products_search) | set(restaurants_search)
