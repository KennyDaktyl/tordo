from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

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


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Profile._meta.fields]
    search_fields = ("user__username",)
    list_display_links = (
        "id",
        "user",
    )


@admin.register(UserAddress)
class UserAddressAdmin(OSMGeoAdmin):
    list_display = [f.name for f in UserAddress._meta.fields]
    search_fields = ("user__username",)
    list_display_links = (
        "id",
        "user",
    )


@admin.register(CompanyData)
class CompanyDataAdmin(OSMGeoAdmin):
    list_display = [f.name for f in CompanyData._meta.fields]
    search_fields = ("user__username", "compane_name")
    list_display_links = ("id", "user", "company_name")


@admin.register(UserPhoneNumber)
class UserPhoneNumberAdmin(admin.ModelAdmin):
    list_display = [f.name for f in UserPhoneNumber._meta.fields]
    search_fields = ("phone_number",)
    list_display_links = (
        "id",
        "user",
    )


@admin.register(DistrictWarsaw)
class DistrictWarsawAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DistrictWarsaw._meta.fields]
    search_fields = ("name",)
    list_display_links = (
        "id",
        "name",
    )


@admin.register(SubDistrictWarsaw)
class SubDistrictWarsawAdmin(admin.ModelAdmin):
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
class PostCodeWarsawAdmin(OSMGeoAdmin):
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
class CityAdmin(admin.ModelAdmin):
    list_display = [f.name for f in City._meta.fields]
    search_fields = ("name",)
    list_display_links = (
        "id",
        "name",
    )


@admin.register(StreetWarsaw)
class StreetWarsawAdmin(admin.ModelAdmin):
    list_display = [f.name for f in StreetWarsaw._meta.fields]
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
