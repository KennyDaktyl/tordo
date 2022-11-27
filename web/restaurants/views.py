from django.views.generic.list import ListView
from web.front.functions import mobile
from django.contrib import messages

from web.models.restaurants import Restaurant, Tag
from web.restaurants.serializers import RestaurantSerializer, RestaurantWithProductsSerializer


class RestaurantListView(ListView):
    model = Restaurant
    serializer_class = RestaurantSerializer
    distance_max = False
    paginate_by = 25
    template_name = "restaurants/desktop/restaurants.html"

    def get_template_names(self):
        if mobile(self.request):
            self.template_name = self.template_name.replace(
                "desktop", "mobile")
        return self.template_name

    def get_context_object_name(self, model):
        return "restaurants"

    def get_queryset(self):
        if self.request.GET.get("search"):
            self.request.session["sorted"] = "name"
            search = self.request.GET.get("search")
            self.distance_max = False
            queryset = self.__restaurants_search(search)
            return RestaurantWithProductsSerializer(queryset, many=True).data

        if self.request.GET.getlist("tags"):
            tags = self.request.GET.getlist("tags")
            tags = [int(x) for x in tags]
            queryset = Restaurant.objects.filter(
                tags__in=tags, is_active=True
            ).distinct()
            serializer = RestaurantSerializer(queryset, many=True)
            return serializer.data

        if self.request.GET.get("sorted"):
            queryset = Restaurant.objects.filter(is_active=True)
            sort_parametr = self.request.GET["sorted"]
            if sort_parametr == "distance":
                self.request.session["sorted"] = "distance"
                if self.request.session.get("location_form"):
                    if self.request.session["location_form"]["distance"]:
                        messages.success(
                            self.request, f"Dane dla podanej lokalizacji.")
                    else:
                        messages.error(self.request, f"Zbyt duża odległość.")
                    return self.__get_restaurants_sorted_by_distance_by_location(
                        self.request.session.get("location_form")
                    )
                else:
                    if self.request.user.is_authenticated:
                        if self.request.user.profile.has_main_address:
                            address = self.request.user.profile.has_main_address
                            messages.success(
                                self.request,
                                f"Lokalizacja dla adresu: {address}",
                            )
                            return self.__get_restaurants_sorted_by_distance_by_user_address(
                                address.location,
                                address.distance_allowed,
                                address.nearest_point,
                            )
                        else:
                            messages.error(
                                self.request,
                                f"Nie posiadasz adresu głównego. Dodaj adres do swojego konta.",
                            )
                    else:
                        messages.error(
                            self.request, f"Nie posiadamy Twojej lokalizacji."
                        )

            if sort_parametr == "name":
                self.request.session["sorted"] = "name"
                return RestaurantSerializer(queryset, many=True).data

            if sort_parametr == "start-time":
                self.request.session["sorted"] = "start-time"
                return RestaurantSerializer(queryset, many=True).data

            if sort_parametr == "end-time":
                self.request.session["sorted"] = "end-time"
                return RestaurantSerializer(queryset, many=True).data

            if sort_parametr == "favorite-dishes":
                self.request.session["sorted"] = "favorite-dishes"
                return RestaurantSerializer(queryset, many=True).data

        self.distance_max = False
        self.request.session["sorted"] = "name"
        queryset = Restaurant.objects.filter(is_active=True)
        return RestaurantSerializer(queryset, many=True).data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("sorted") == "distance":
            if self.request.session.get("location_form") or self.distance_max:
                print(self.request.session.get(
                    "location_form"), self.distance_max)
                context["map"] = self.__create_folium_map()
            # else:
            #     context["address_form"] = AddressForm()

        context["header_white"] = True
        context["distance_max"] = self.distance_max
        context["tags"] = Tag.objects.all()
        return context

    def __restaurants_search(self, search):
        restaurants_search_in_name = Restaurant.objects.filter(
            name__icontains=search, is_active=True
        )

        products_data = Product.objects.filter(
            name__icontains=search, is_active=True
        ).values("pk")
        product_ids = [el["pk"] for el in products_data]
        restaurants_data = RestaurantMenu.objects.filter(
            product__in=product_ids
        ).values("restaurant")
        restaurant_ids = [el["restaurant"] for el in restaurants_data]
        restaurants_search_in_product = Restaurant.objects.filter(
            pk__in=restaurant_ids)
        for restaurant in restaurants_search_in_product:
            restaurant.categories = restaurant.categories_with_products_search(
                search)
        queryset = list(restaurants_search_in_product) + list(
            restaurants_search_in_name
        )
        return queryset


restaurants = RestaurantListView.as_view()
