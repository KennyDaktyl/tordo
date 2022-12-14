import factory
from factory.fuzzy import FuzzyText

from tests.Fixturies.fixture_restaurant import RestaurantFactory
from web.models import Category, Product


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    restaurant = factory.SubFactory(RestaurantFactory)
    number = factory.Faker("pyint")
    name = FuzzyText(length=5, prefix="Kategoria_")
    slug = factory.Faker("slug")
    is_active = True


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    name = factory.Faker("word")
    slug = factory.Faker("slug")
    price = 9.99
    tax = factory.Faker("random_element", elements=[1, 2, 3, 4])
    description = factory.Faker("text")
    image_listing_jpg = factory.django.ImageField(color="blue")
    image_basket_jpg = factory.django.ImageField(color="green")
    thumbnails_cache = {}
    is_active = True
