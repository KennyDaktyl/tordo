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
    from_hour = serializers.TimeField()
    to_hour = serializers.TimeField()
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Restaurant
        fields = [
            "name",
            "street",
            "house",
            "post_code",
            "slug",
            "home_page",
            "description",
            "id_restaurant",
            "thumbnails_cache",
            "images_listing_webp",
            "images_listing_jpg",
            "images_main_webp_desktop",
            "images_main_jpg_desktop",
            "images_main_webp_mobile",
            "images_main_jpg_mobile",
            "images_logo_webp",
            "images_logo_jpg",
            "from_hour",
            "to_hour",
            "weekday",
            "tags",
            "likes_counter",
            "is_open",
        ]


class RestaurantWithProductsSerializer(serializers.HyperlinkedModelSerializer):
    id_restaurant = serializers.IntegerField(source="pk")
    from_hour = serializers.TimeField()
    to_hour = serializers.TimeField()
    tags = TagSerializer(read_only=True, many=True)
    categories = CategoryWithProductsSerializer(
        read_only=True, many=True, default=[])

    class Meta:
        model = Restaurant
        fields = [
            "name",
            "street",
            "house",
            "post_code",
            "slug",
            "home_page",
            "description",
            "id_restaurant",
            "images_listing_webp",
            "images_listing_jpg",
            "images_main_webp_desktop",
            "images_main_jpg_desktop",
            "images_main_webp_mobile",
            "images_main_jpg_mobile",
            "images_logo_webp",
            "images_logo_jpg",
            "from_hour",
            "to_hour",
            "weekday",
            "tags",
            "likes_counter",
            "categories",
            "is_open"
        ]
