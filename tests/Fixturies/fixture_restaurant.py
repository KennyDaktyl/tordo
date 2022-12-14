import random
import factory
from factory.fuzzy import BaseFuzzyAttribute, FuzzyText
from faker import Faker

from django.contrib.gis.geos import Point
from web.models import Restaurant
from web.models.restaurants import Tag

fake = Faker()


class FuzzyPoint(BaseFuzzyAttribute):
    def fuzz(self):
        return Point(
            random.uniform(-180.0, 180.0), random.uniform(-90.0, 90.0)
        )


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = FuzzyText(length=5, prefix="Tags_")


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Restaurant

    name = FuzzyText(length=5, prefix="Restaurant_")
    motto = FuzzyText(length=15, prefix="Nasze motto to: ")
    location = FuzzyPoint()
    street = FuzzyText(length=15, prefix="Ulica ")
    house = FuzzyText(length=2)
    city = FuzzyText(length=5, prefix="Miasto_")
    post_code = "31-926"
    location = FuzzyPoint()
    phone_number = FuzzyText(length=12)
    is_located = True
    is_active = True
    geo_data = FuzzyText(length=12)
    home_page = "http://www.example.com"
    description = FuzzyText()
    likes_counter = 0
    image_listing_photo = factory.django.ImageField(color="blue")
    image_logo_photo = factory.django.ImageField(color="yellow")
    image_main_photo_desktop = factory.django.ImageField(color="red")
    image_main_photo_mobile = factory.django.ImageField(color="black")
    thumbnails_cache = {}
