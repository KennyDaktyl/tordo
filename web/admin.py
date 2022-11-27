from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from web.models.restaurants import Restaurant, OpeningHours, Tag
from web.models.products import Category, Product, RestaurantMenu
from web.models.images import Thumbnail


@admin.register(Restaurant)
class RestaurantAdmin(OSMGeoAdmin):
    list_display = ("name", "location", "is_located", "geo_data")
    search_fields = ("name",)
    list_display_links = ("name",)
    list_filter = ["is_located"]


@admin.register(RestaurantMenu)
class RestaurantMenuAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "product")
    search_fields = (
        "restaurant",
        "product",
    )
    list_display_links = ("restaurant", "product")
    list_filter = ["restaurant", "product"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)
    list_display_links = ("name",)
    list_filter = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_display_links = ("name",)
    list_filter = ["name"]


@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = [f.name for f in OpeningHours._meta.fields]
    search_fields = ("restaurant",)
    list_display_links = (
        "id",
        "restaurant",
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Tag._meta.fields]
    search_fields = ("name",)
    list_display_links = (
        "id",
        "name",
    )


@admin.register(Thumbnail)
class ThumbnailAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Thumbnail._meta.fields]
    search_fields = ("id", "photo", )
    list_display_links = (
        "id",
    )
    list_filter = [
        "status"
    ]
