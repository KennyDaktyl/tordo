import pytest
from django.test import Client

from tests.Fixturies.fixture_products import CategoryFactory, ProductFactory
from tests.Fixturies.fixture_restaurant import RestaurantFactory, TagFactory
from web.models import Restaurant


@pytest.fixture
def client():
    client = Client()
    client.defaults["HTTP_USER_AGENT"] = "Chrome"
    return client


@pytest.fixture
def restaurants_data():
    for rest_num in range(1, 5):
        restaurant = RestaurantFactory.create(name=f"Restaurant_{rest_num}")
        for category_num in range(1, 3):
            category = CategoryFactory.create(
                restaurant=restaurant, name=f"Kategoria_{category_num}"
            )
            for product_num in range(1, 5):
                ProductFactory.create(category=category, name=f"Produkt_{product_num}")
        for tag_num in range(1, 3):
            tag = TagFactory.create(name=f"Tag_{tag_num}")
            restaurant.tags.add(tag)
            restaurant.save()
    return Restaurant.objects.all()
