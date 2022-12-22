import folium
import json

from django.core.exceptions import ValidationError
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point

from datetime import datetime
from typing import List

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
from django.shortcuts import redirect

from web.front.functions import mobile
from web.models.restaurants import Restaurant, Tag
from web.restaurants.serializers import (
    RestaurantDetailsSerializer,
    RestaurantsListSerializer,
)

User = get_user_model()


class RestaurantListView(ListView):
    model = Restaurant
    serializer_class = RestaurantsListSerializer
    distance_max = False
    paginate_by = 2
    template_name = "restaurants/desktop/restaurants.html"

    def get_template_names(self):
        if mobile(self.request):
            self.template_name = self.template_name.replace("desktop", "mobile")
        return self.template_name

    def get_context_object_name(self, model):
        return "restaurants"

    def get_queryset(self):
        if self.request.GET.get("search"):
            self.request.session["sorted"] = "name"
            search = self.request.GET.get("search")
            self.distance_max = False
            queryset = self.__restaurants_search(search)
            return RestaurantsListSerializer(queryset, many=True).data

        if self.request.GET.getlist("tags"):
            tags = self.request.GET.getlist("tags")
            tags = [int(x) for x in tags]
            queryset = Restaurant.objects.filter(
                tags__in=tags, is_active=True
            ).distinct()
            serializer = RestaurantsListSerializer(queryset, many=True)
            return serializer.data

        if self.request.GET.get("sorted"):
            queryset = Restaurant.objects.filter(is_active=True)
            sort_parametr = self.request.GET["sorted"]
            if sort_parametr == "distance":
                # TODO Testujemy DIstance
                longitude = self.request.GET.get("lon")
                latitude = self.request.GET.get("lat")
                place_name = self.request.GET.get("place_name")
                if not longitude or not latitude:
                    messages.error(self.request, f"Błąd lokalizacji")
                else:
                    user_location = Point(float(longitude), float(latitude), srid=4326)
                    self.request.session["user_location"] = (longitude, latitude, place_name)
                    restaurants = Restaurant.objects.annotate(
                        distance=Distance("location", user_location)
                    ).order_by("distance")
                    return RestaurantsListSerializer(restaurants, many=True).data

            if sort_parametr == "name":
                self.request.session["sorted"] = "name"
                return RestaurantsListSerializer(queryset, many=True).data

            if sort_parametr == "start-time":
                self.request.session["sorted"] = "start-time"
                return RestaurantsListSerializer(queryset, many=True).data

            if sort_parametr == "end-time":
                self.request.session["sorted"] = "end-time"
                return RestaurantsListSerializer(queryset, many=True).data

            if sort_parametr == "favorite-dishes":
                self.request.session["sorted"] = "favorite-dishes"
                return RestaurantsListSerializer(queryset, many=True).data

        self.distance_max = False
        self.request.session["sorted"] = "name"
        queryset = Restaurant.objects.filter(is_active=True)
        return RestaurantsListSerializer(queryset, many=True).data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("sorted") == "distance":
            if self.request.session.get("location_form") or self.distance_max:
                context["map"] = self.__create_folium_map()
            # else:
            #     context["address_form"] = AddressForm()
        context["place_name"] = self.request.GET.get("place_name")
        context["header_white"] = True
        context["distance_max"] = self.distance_max
        context["tags"] = Tag.objects.all()
        return context

    def __restaurants_search(self, search: str) -> List[Restaurant]:
        restaurants = Restaurant.objects.filter(is_active=True)
        restaurants_search = restaurants.filter(name__icontains=search)
        products_search = []
        for restaurant in restaurants:
            categories = []
            for category in restaurant.categories:
                products_filtered = category.products.filter(name__icontains=search)
                if products_filtered:
                    category.products_filtered = products_filtered
                    categories.append(category)
            if categories:
                restaurant.categories_filtered = categories
                products_search.append(restaurant)
        queryset = set(products_search) | set(restaurants_search)
        queryset_sorted = sorted(queryset, key=lambda d: d.name)
        return queryset_sorted


class RestaurantsListMapView(TemplateView):
    template_name = "restaurants/desktop/restaurants_map_list.html"

    def get_template_names(self):
        if mobile(self.request):
            self.template_name = self.template_name.replace("desktop", "mobile")
        return self.template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get("user_location"):
            longitude, latitude, place_name = self.request.session["user_location"]
            user_location = Point(float(latitude), float(longitude), srid=4326)
            zoom = 12
            context["longitude"] = longitude
            context["latitude"] = latitude
            context["place_name"] = place_name
        else:
            user_location = None
            zoom = 6

        restaurants = Restaurant.objects.all()
        context["restaurants"] = restaurants
        context["map"] = self.__create_folium_map(user_location, restaurants, zoom)
        return context

    def __create_folium_map(self, user_location, restaurants, zoom):
        if not user_location:
            user_location = Point(52.237049, 21.017532, srid=4326)
        map = folium.Map(
            location=[user_location[0], user_location[1]],
            width="100%",
            position="relative",
            zoom_start=zoom,
        )

        if (
            "bootstrap_css",
            "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css",
        ) in map.default_css:
            map.default_css.remove(
                (
                    "bootstrap_css",
                    "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css",
                )
            )
        # if ('leaflet_css', 'https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css') in map.default_css:
        #     map.default_css.remove(('leaflet_css', 'https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css'))
        tooltip = "Lokalizacja adresu"
        marker = folium.Marker(
            [user_location[0], user_location[1]],
            popup="<i>Twoja lokalizacja</i>",
            tooltip=tooltip,
            icon=folium.Icon(color="red", icon="info-sign"),
        )
        marker.add_to(map)

        for restaurant in restaurants:
            tooltip = restaurant.name
            marker = folium.Marker(
                [restaurant.location[1], restaurant.location[0]],
                popup=f"<a href='{restaurant.get_absolute_url()}'>" + restaurant.name + "</a>",
                tooltip=tooltip,
            )
            marker.add_to(map)

        return map.get_root().render()


class RestaurantMapView(TemplateView):
    template_name = "restaurants/desktop/restaurant_map.html"

    def get_template_names(self):
        if mobile(self.request):
            self.template_name = self.template_name.replace("desktop", "mobile")
        return self.template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = Restaurant.objects.get(pk=self.kwargs["pk"])
        context["restaurant"] = restaurant
        context["map"] = self.__create_folium_map(restaurant.location, restaurant.name)
        return context

    def __create_folium_map(self, loc, name):
        map = folium.Map(
            location=[loc[1], loc[0]],
            width="100%",
            position="relative",
        )
        tooltip = name
        if (
            "bootstrap_css",
            "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css",
        ) in map.default_css:
            map.default_css.remove(
                (
                    "bootstrap_css",
                    "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css",
                )
            )
        folium.Marker(
            [loc[1], loc[0]],
            popup=f"<i>{name}</i>",
            tooltip=tooltip,
        ).add_to(map)
        return map.get_root().render()


class RestaurantDetailsView(DetailView):
    template_name = "restaurants/desktop/restaurant_details.html"
    model = Restaurant
    serializer_class = RestaurantDetailsSerializer

    def get_template_names(self):
        if mobile(self.request):
            self.template_name = self.template_name.replace("desktop", "mobile")
        return self.template_name

    def get_context_object_name(self, model):
        return "restaurant"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_white"] = True
        context["current_weekday_number"] = datetime.today().isoweekday()

        search = self.request.GET.get("search")
        menu_category = self.request.GET.get("menu_category")

        if search:
            categories = []
            for category in self.object.categories:
                filtered_products = category.products.filter(name__icontains=search)
                if filtered_products:
                    category.products_filtered = filtered_products
                    categories.append(category)
            if categories:
                self.object.categories_filtered = categories
                context["restaurant"] = RestaurantDetailsSerializer(self.object).data
        return context


class DeleteLocation(View):

    def get(self, request):
        del self.request.session["user_location"]
        return redirect('restaurants')


def get_unique_elements(elements, key):
    unique_elements = []
    for el in elements:
        if el[key] not in unique_elements:
            unique_elements.append(el[key])
    return unique_elements


restaurants = RestaurantListView.as_view()
restaurants_map = RestaurantsListMapView.as_view()
restaurant_details = RestaurantDetailsView.as_view()
restaurant_map = RestaurantMapView.as_view()
delete_location = DeleteLocation.as_view()
