import pytest


class TestRestaurantView:
    @pytest.fixture(autouse=True)
    def set_up(self, client, restaurants_data):
        self.client = client
        self.restaurants_data = restaurants_data

    @pytest.mark.django_db
    def test_restaurant_list_view(self):
        restaurants_expected = self.restaurants_data
        response = self.client.get("/restauracje/", HTTP_USER_AGENT="Chrome")
        object_list = response.context_data["object_list"]

        assert response.status_code == 200
        assert isinstance(response.context_data["object_list"], list)
        assert len(restaurants_expected) == len(object_list)

    @pytest.mark.django_db
    def test_active_restaurant_list_view(self):
        restaurants_expected = self.restaurants_data
        restaurant_not_active = restaurants_expected.last()
        restaurant_not_active.is_active = False
        restaurant_not_active.save()
        response = self.client.get("/restauracje/", HTTP_USER_AGENT="Chrome")
        object_list = response.context_data["object_list"]

        assert response.status_code == 200
        assert isinstance(response.context_data["object_list"], list)
        assert (len(restaurants_expected) - 1) == len(object_list)

    @pytest.mark.django_db
    def test_search_in_restaurant_list_view(self):
        restaurants_expected = self.restaurants_data
        restaurant_expected = restaurants_expected.last()
        response = self.client.get(
            f"/restauracje/?search={restaurant_expected.name}",
            HTTP_USER_AGENT="Chrome",
        )
        object_list = response.context_data["object_list"]
        assert len(object_list) == 1
        assert object_list[0]["name"] == restaurant_expected.name

    @pytest.mark.django_db
    def test_search_products_in_restaurant_list_view(self):
        product_expected = self.__get_product_expected()
        product_expected.name = "Szukany produkt"
        product_expected.save()
        response = self.client.get(f"/restauracje/?search={product_expected.name}")
        object_list = response.context_data["object_list"]
        for restaurant in object_list:
            for category in restaurant["categories_filtered"]:
                for product in category["products_filtered"]:
                    assert product["name"] == product_expected.name

    def __get_product_expected(self):
        return self.restaurants_data.last().categories[0].products[0]
