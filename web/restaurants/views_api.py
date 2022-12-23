from web.models.restaurants import Restaurant
from web.restaurants.serializers import CountRestaurantWhenUseFilterSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from web.models.restaurants import FilterFood, FilterAdvantage, Tag


class CountRestaurantWhenUseFilters(APIView):
    def get(self, request, format=None):
        checked = request.GET.get("checked")

        filter_food_id = request.GET.get("filter_food_id")
        filter_foods_session = request.session.get("filter_foods")

        filter_advantage_id = request.GET.get("filter_advantage_id")
        filter_advantages_session = request.session.get("filter_advantages")
        
        filter_tag_id = request.GET.get("filter_tag_id")
        filter_tags_session = request.session.get("filter_tags")
        
        restaurants = Restaurant.objects.filter(is_active=True)
        if filter_food_id:
            if filter_foods_session:
                if checked and int(filter_food_id) not in filter_foods_session:
                    filter_foods_session.append(int(filter_food_id))
                else:
                    if filter_food_id:
                        filter_foods_session.remove(int(filter_food_id))
                request.session["filter_foods"] = filter_foods_session
            else:
                filter_food = FilterFood.objects.get(pk=filter_food_id)
                request.session["filter_foods"] = [filter_food.id]
                filter_foods_session = request.session["filter_foods"]
            if filter_foods_session:
                restaurants = restaurants.filter(filter_food__id__in=filter_foods_session).distinct()
        
        if filter_advantage_id:
            if filter_advantages_session:
                if checked and int(filter_advantage_id) not in filter_advantages_session:
                    filter_advantages_session.append(int(filter_advantage_id))
                else:
                    if filter_advantage_id:
                        filter_advantages_session.remove(int(filter_advantage_id))
                request.session["filter_advantages"] = filter_advantages_session
            else:
                filter_advantage = FilterAdvantage.objects.get(pk=filter_advantage_id)
                request.session["filter_advantages"] = [filter_advantage.id]
                filter_advantages_session = request.session["filter_advantages"]

        if filter_tag_id:
            if filter_tags_session:
                if checked and int(filter_tag_id) not in filter_tags_session:
                    filter_tags_session.append(int(filter_tag_id))
                else:
                    if filter_tag_id:
                        filter_tags_session.remove(int(filter_tag_id))
                request.session["filter_tags"] = filter_tags_session
            else:
                filter_tag = Tag.objects.get(pk=filter_tag_id)
                request.session["filter_tags"] = [filter_tag.id]
                filter_tags_session = request.session["filter_tags"]

        if filter_foods_session:
            restaurants = restaurants.filter(filter_food__id__in=filter_foods_session).distinct()
        if filter_advantages_session:
            restaurants = restaurants.filter(filter_advantages__id__in=filter_advantages_session).distinct()
        if filter_tags_session:
            restaurants = restaurants.filter(filter_advantages__id__in=filter_tags_session).distinct()

        count_restaurants = {"count": restaurants.count()}
        # del self.request.session["filter_foods"]
        print(filter_foods_session)
        print(filter_advantages_session)
        print(filter_tags_session)
        return Response(CountRestaurantWhenUseFilterSerializer(count_restaurants).data)


count_restaurants = CountRestaurantWhenUseFilters.as_view()
