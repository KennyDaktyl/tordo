import folium
from datetime import datetime

from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
from django.shortcuts import redirect

from web.front.functions import mobile
from web.models.restaurants import Restaurant, Tag, FilterAdvantage, FilterFood
from web.restaurants.serializers import (
    RestaurantDetailsSerializer,
    RestaurantsListSerializer,
)
from .queries import (
    get_object_list_filtered,
    get_object_list_sorted,
    get_object_list_search,
    get_object_list_by_distance,
)

User = get_user_model()


class RestaurantListView(ListView):
    model = Restaurant
    serializer_class = RestaurantsListSerializer
    distance_max = False
    paginate_by = 5
    template_name = "restaurants/desktop/restaurants.html"

    def get_template_names(self):
        if mobile(self.request):
            self.template_name = self.template_name.replace(
                "desktop", "mobile")
        return self.template_name

    def get_queryset(self):
        queryset = Restaurant.objects.filter(is_active=True)
        if not self.request.GET.get("sorted"):
            if not self.request.session.get("sorted"):
                self.request.session["sorted"] = "name"
        else:
            self.request.session["sorted"] = self.request.GET["sorted"]
            if self.request.GET["sorted"] == "distance" and (
                self.request.GET.get("lon") and self.request.GET.get("lat")
            ):

                self.request.session["user_location"] = {
                    "longitude": self.request.GET.get("lon"),
                    "latitude": self.request.GET.get("lat"),
                    "place_name": self.request.GET.get("place_name"),
                }
        user_location = self.request.session.get("user_location")
        if user_location:
            queryset = get_object_list_by_distance(
                self.request, queryset, user_location
            )

        queryset = get_object_list_filtered(self.request, queryset)
        if self.request.GET.get("search") or self.request.session.get("search"):
            queryset = get_object_list_search(self.request, queryset)
            return RestaurantsListSerializer(queryset, many=True).data

        queryset = get_object_list_sorted(self.request, queryset)
        return RestaurantsListSerializer(queryset, many=True).data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get("user_location"):
            context["place_name"] = self.request.session.get("user_location")[
                "place_name"
            ]
        if self.request.session.get("search"):
            context["search"] = self.request.session.get("search")

        context["header_white"] = True
        context["tags"] = Tag.objects.all()
        context["filter_advantages"] = FilterAdvantage.objects.filter(is_active=True)[
            0:10
        ]
        context["filter_foods"] = FilterFood.objects.filter(is_active=True)[
            0:10]
        context["restaurants_count"] = super().get_queryset().count()
        return context


class RestaurantsListMapView(TemplateView):
    template_name = "restaurants/desktop/restaurants_map_list.html"

    def get_template_names(self):
        if mobile(self.request):
            self.template_name = self.template_name.replace(
                "desktop", "mobile")
        return self.template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Restaurant.objects.filter(is_active=True)

        if self.request.session.get("user_location"):
            zoom = 12
            user_location = self.request.session["user_location"]
            queryset = get_object_list_by_distance(
                self.request, queryset, self.request.session["user_location"]
            )
        else:
            user_location = None
            zoom = 6

        queryset = get_object_list_filtered(self.request, queryset)
        context["map"] = self.__create_folium_map(
            user_location, queryset, zoom)
        return context

    def __create_folium_map(self, user_location, restaurants, zoom):
        if not user_location:
            user_location = {
                "latitude": 52.237049,
                "longitude": 21.017532,
                "place_name": False,
            }
        map = folium.Map(
            location=[user_location["latitude"], user_location["longitude"]],
            width="100%",
            position="relative",
            zoom_start=zoom,
        )

        if (
            "bootstrap_css",
            "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css",  # type: ignore
        ) in map.default_css:
            map.default_css.remove(
                (
                    "bootstrap_css",
                    "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css",  # type: ignore
                )
            )
        if user_location["place_name"]:
            tooltip = "Lokalizacja adresu"
            marker = folium.Marker(
                [user_location["latitude"], user_location["longitude"]],
                popup="<i>Twoja lokalizacja</i>",
                tooltip=tooltip,
                icon=folium.Icon(color="red", icon="info-sign"),
            )
            marker.add_to(map)

        for restaurant in restaurants:
            tooltip = restaurant.name
            marker = folium.Marker(
                [restaurant.location[1], restaurant.location[0]],
                popup=f"<a href='{restaurant.get_absolute_url()}'>"
                + restaurant.name
                + "</a>",
                tooltip=tooltip,
            )
            marker.add_to(map)

        return map.get_root().render()


class RestaurantMapView(TemplateView):
    template_name = "restaurants/desktop/restaurant_map.html"

    def get_template_names(self):
        if mobile(self.request):
            self.template_name = self.template_name.replace(
                "desktop", "mobile")
        return self.template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = Restaurant.objects.get(pk=self.kwargs["pk"])
        context["restaurant"] = restaurant
        context["map"] = self.__create_folium_map(
            restaurant.location, restaurant.name)
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
            "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css",  # type: ignore
        ) in map.default_css:
            map.default_css.remove(
                (
                    "bootstrap_css",
                    "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css",  # type: ignore
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
            self.template_name = self.template_name.replace(
                "desktop", "mobile")
        return self.template_name

    def get_context_object_name(self, model):
        return "restaurant"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_white"] = True
        context["current_weekday_number"] = datetime.today().isoweekday()

        search = self.request.GET.get("search")
        # menu_category = self.request.GET.get("menu_category")

        if search:
            categories = []
            for category in self.object.categories:
                filtered_products = category.products.filter(
                    name__icontains=search)
                if filtered_products:
                    category.products_filtered = filtered_products
                    categories.append(category)
            if categories:
                self.object.categories_filtered = categories
                context["restaurant"] = RestaurantDetailsSerializer(
                    self.object).data
        return context


class DeleteLocation(View):
    def get(self, request):
        if self.request.session.get("user_location"):
            del self.request.session["user_location"]
        if self.request.session.get("place_name"):
            del self.request.session["place_name"]
        return redirect("restaurants")


class DeleteSearch(View):
    def get(self, request):
        del self.request.session["search"]
        return redirect("restaurants")


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
delete_search = DeleteSearch.as_view()
