from rest_framework import serializers

from web.models.restaurants import Restaurant, Tag, OpeningHours
from web.products.serializers import (
    CategoryWithProductsSerializer,
)


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
        ]
        ordering = ["name"]


class RestaurantDetailsSerializer(serializers.ModelSerializer):
    from_hour = serializers.DateTimeField(format="%H:%M")
    to_hour = serializers.DateTimeField(format="%H:%M")
    tags = TagSerializer(read_only=True, many=True)
    categories_filtered = CategoryWithProductsSerializer(
        read_only=True, many=True, default=[]
    )

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
        ]
        ordering = ["name"]
