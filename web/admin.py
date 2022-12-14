from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.gis.admin import GISModelAdmin

from web.models.accounts import Profile, UserPhoneNumber
from web.models.addresses import (
    City,
    CompanyData,
    DistrictWarsaw,
    PostCodeWarsaw,
    StreetWarsaw,
    SubDistrictWarsaw,
    UserAddress,
)
from web.models.restaurants import Restaurant, OpeningHours, Tag, FoodSupplier, Room, Advantage
from web.models.products import Category, Product, RestaurantMenu
from web.models.images import Thumbnail, Photo


@admin.register(Restaurant)
class RestaurantAdmin(GISModelAdmin):
    list_display = ("name", "location", "is_located", "geo_data")
    search_fields = ("name",)
    list_display_links = ("name",)
    list_filter = ["is_located"]


@admin.register(RestaurantMenu)
class RestaurantMenuAdmin(ModelAdmin):
    list_display = ("restaurant", "product")
    search_fields = (
        "restaurant",
        "product",
    )
    list_display_links = ("restaurant", "product")
    list_filter = ["restaurant", "product"]


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)
    list_display_links = ("name",)
    list_filter = ["name"]


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_display_links = ("name",)
    list_filter = ["name"]


@admin.register(OpeningHours)
class OpeningHoursAdmin(ModelAdmin):
    list_display = [f.name for f in OpeningHours._meta.fields]
    search_fields = ("restaurant",)
    list_display_links = (
        "id",
        "restaurant",
    )


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = [f.name for f in Tag._meta.fields]
    search_fields = ("name",)
    list_display_links = (
        "id",
        "name",
    )


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = [f.name for f in Profile._meta.fields]
    search_fields = ("user__username",)
    list_display_links = (
        "id",
        "user",
    )


@admin.register(UserAddress)
class UserAddressAdmin(GISModelAdmin):
    list_display = [f.name for f in UserAddress._meta.fields]
    search_fields = ("user__username",)
    list_display_links = (
        "id",
        "user",
    )


@admin.register(CompanyData)
class CompanyDataAdmin(GISModelAdmin):
    list_display = [f.name for f in CompanyData._meta.fields]
    search_fields = ("user__username", "compane_name")
    list_display_links = ("id", "user", "company_name")


@admin.register(UserPhoneNumber)
class UserPhoneNumberAdmin(ModelAdmin):
    list_display = [f.name for f in UserPhoneNumber._meta.fields]
    search_fields = ("phone_number",)
    list_display_links = (
        "id",
        "user",
    )


@admin.register(DistrictWarsaw)
class DistrictWarsawAdmin(ModelAdmin):
    list_display = [f.name for f in DistrictWarsaw._meta.fields]
    search_fields = ("name",)
    list_display_links = (
        "id",
        "name",
    )


@admin.register(SubDistrictWarsaw)
class SubDistrictWarsawAdmin(ModelAdmin):
    list_display = [f.name for f in SubDistrictWarsaw._meta.fields]
    search_fields = ("name",)
    list_display_links = (
        "id",
        "name",
    )
    list_filter = [
        "district",
    ]


@admin.register(PostCodeWarsaw)
class PostCodeWarsawAdmin(GISModelAdmin):
    list_display = [f.name for f in PostCodeWarsaw._meta.fields]
    search_fields = ("name",)
    list_display_links = (
        "id",
        "name",
    )
    list_filter = [
        "is_located",
    ]


@admin.register(City)
class CityAdmin(ModelAdmin):
    list_display = [f.name for f in City._meta.fields]
    search_fields = ("name",)
    list_display_links = (
        "id",
        "name",
    )


@admin.register(StreetWarsaw)
class StreetWarsawAdmin(ModelAdmin):
    list_display = [f.name for f in StreetWarsaw._meta.fields]
    search_fields = ("name",)
    list_display_links = (
        "id",
        "name",
    )


@admin.register(Thumbnail)
class ThumbnailAdmin(ModelAdmin):
    list_display = [f.name for f in Thumbnail._meta.fields]
    search_fields = ("id", "photo", )
    list_display_links = (
        "id",
    )
    list_filter = [
        "status"
    ]

@admin.register(Photo)
class PhotoAdmin(ModelAdmin):
    list_display = [f.name for f in Photo._meta.fields]
    search_fields = ("id", "image", )
    list_display_links = (
        "id",
    )
    list_filter = [
        "restaurant_id",
        "product_id",
    ]

@admin.register(FoodSupplier)
class FoodSupplierAdmin(ModelAdmin):
    list_display = [f.name for f in FoodSupplier._meta.fields]
    search_fields = ("id", "name", "image", )
    list_display_links = (
        "id",
    )
    

@admin.register(Room)
class RoomAdmin(ModelAdmin):
    list_display = [f.name for f in Room._meta.fields]
    search_fields = ("id", "name",)
    list_display_links = (
        "id",
    )


@admin.register(Advantage)
class AdvantageAdmin(ModelAdmin):
    list_display = [f.name for f in Advantage._meta.fields]
    search_fields = ("id", "name",)
    list_display_links = (
        "id",
    )
