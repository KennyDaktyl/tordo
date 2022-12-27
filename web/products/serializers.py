from rest_framework import serializers
from rest_framework.fields import ListField

from web.models.products import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "slug",
            "price",
            "description",
            "thumbnails_cache",
            "images_listing_webp",
            "images_listing_jpg",
            "images_basket_webp",
            "images_basket_jpg",
            "is_active",
        ]
        # fields = "__all__"


class CategoryWithProductsSerializer(serializers.ModelSerializer):
    products_filtered = ListField(
        child=ProductSerializer(), required=False, allow_empty=True
    )

    class Meta:
        model = Category
        fields = ["restaurant", "name", "products_filtered"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["restaurant", "name", "products"]


class RestaurantMenuSerializer(serializers.ModelSerializer):
    id_product = serializers.IntegerField(source="product.pk")
    category = CategoryWithProductsSerializer(source="product.category")
    name = serializers.CharField(source="product.name")
    slug = serializers.SlugField(source="product.slug")
    price = serializers.DecimalField(
        source="product.price", decimal_places=2, max_digits=8
    )
    description = serializers.CharField(source="product.description")
    is_active = serializers.BooleanField(source="product.is_active")
    images_listing_webp = serializers.ImageField(
        source="product.images_mobile_listing_webp"
    )
    images_listing_jpg = serializers.ImageField(
        source="product.images_mobile_listing_jpg"
    )
    images_basket_webp = serializers.ImageField(source="product.images_basket_webp")
    images_basket_jpg = serializers.ImageField(source="product.images_basket_jpg")

    class Meta:
        model = Product
        fields = [
            "id_product",
            "category",
            "name",
            "slug",
            "price",
            "description",
            "images_listing_jpg",
            "images_listing_webp",
            "images_basket_webp",
            "images_basket_jpg",
            "is_active",
        ]
