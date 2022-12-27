from rest_framework import serializers

from web.models.restaurants import (
    Restaurant,
    Tag,
    OpeningHours,
    FilterAdvantage,
    FilterFood,
)
from web.products.serializers import (
    CategoryWithProductsSerializer,
)
from django.contrib.gis.measure import Distance


class DistanceField(serializers.Field):
    def to_representation(self, obj):
        if obj is None:
            return None
        distance_float = obj.km
        return str(round(distance_float, 2))

    def to_internal_value(self, data):
        if data is None:
            return None
        return Distance(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class OpenHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = ["id", "weekday", "from_hour", "to_hour", "weekday_name"]


class RestaurantsListSerializer(serializers.ModelSerializer):
    from_hour = serializers.DateTimeField(format="%H:%M")
    to_hour = serializers.DateTimeField(format="%H:%M")
    tags = TagSerializer(read_only=True, many=True)
    categories_filtered = CategoryWithProductsSerializer(
        read_only=True, many=True, default=[]
    )
    distance = DistanceField(allow_null=True)

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "name",
            "slug",
            "city",
            "location",
            "listing_webp",
            "listing_jpg",
            "from_hour",
            "to_hour",
            "weekday",
            "tags",
            "likes_counter",
            "categories_filtered",
            "is_open",
            "distance",
        ]
        ordering = ["name"]


class RestaurantDetailsSerializer(serializers.ModelSerializer):
    from_hour = serializers.DateTimeField(format="%H:%M")
    to_hour = serializers.DateTimeField(format="%H:%M")
    tags = TagSerializer(read_only=True, many=True)
    categories_filtered = CategoryWithProductsSerializer(
        read_only=True, many=True, default=[]
    )
    distance = DistanceField(allow_null=True)

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "name",
            "slug",
            "motto",
            "street",
            "house",
            "city",
            "post_code",
            "location",
            "phone_number",
            "slug",
            "home_page",
            "description",
            "listing_webp",
            "listing_jpg",
            "main_webp_desktop",
            "main_jpg_desktop",
            "main_webp_mobile",
            "main_jpg_mobile",
            "logo_webp",
            "logo_jpg",
            "from_hour",
            "to_hour",
            "weekday",
            "tags",
            "food_suppliers",
            "our_advantages",
            "our_rooms",
            "likes_counter",
            "categories_filtered",
            "is_open",
            "distance",
        ]
        ordering = ["name"]


class CountRestaurantWhenUseFilterSerializer(serializers.Serializer):
    count = serializers.IntegerField(read_only=True)


class FilterAdvantageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterAdvantage
        fields = [
            "id",
            "name",
        ]


class FilterFoodListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterFood
        fields = [
            "id",
            "name",
        ]
