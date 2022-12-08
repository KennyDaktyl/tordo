from rest_framework import serializers

from web.models.restaurants import Restaurant, Tag, OpeningHours
from web.products.serializers import ProductSerializer, CategoryWithProductsSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class OpenHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = ["id", "weekday", "from_hour", "to_hour", "weekday_name"]


class RestaurantSerializer(serializers.ModelSerializer):
    id_restaurant = serializers.IntegerField(source="pk")
    from_hour = serializers.DateTimeField(format="%H:%M")
    to_hour = serializers.DateTimeField(format="%H:%M")
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Restaurant
        fields = [
            "name",
            "motto",
            "street",
            "house",
            "city",
            "post_code",
            "phone_number",
            "slug",
            "home_page",
            "description",
            "id_restaurant",
            "thumbnails_cache",
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
            "is_open",
        ]


class RestaurantWithProductsSerializer(serializers.ModelSerializer):
    id_restaurant = serializers.IntegerField(source="pk")
    from_hour = serializers.DateTimeField(format="%H:%M")
    to_hour = serializers.DateTimeField(format="%H:%M")
    tags = TagSerializer(read_only=True, many=True)
    categories = CategoryWithProductsSerializer(
        read_only=True, many=True, default=[])

    class Meta:
        model = Restaurant
        fields = [
            "name",
            "motto",
            "street",
            "house",
            "city",
            "post_code",
            "phone_number",
            "slug",
            "home_page",
            "description",
            "id_restaurant",
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
            "categories",
            "is_open"
        ]
        ordering = ['name']
