import json
from web.restaurants.serializers import CountRestaurantWhenUseFilterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from web.models.restaurants import Restaurant, FilterFood, FilterAdvantage, Tag


FilterMapping = {
    "filter_foods": FilterFood,
    "filter_advantages": FilterAdvantage,
    "filter_tags": Tag
}


class CountRestaurantWhenUseFilters(APIView):
    def get(self, request):
        restaurants = Restaurant.objects.filter(is_active=True)
        checked = bool(request.GET.get("checked", False))
        reset = request.GET.get("reset", False)
        filter_id = request.GET.get("filter_id")

        if filter_id:
            filter_name, id = filter_id.split("-")
            filter_object = FilterMapping[filter_name]
            filter_session = request.session.get(filter_name, [])
            if request.session.get(filter_name):
                if checked and int(id) not in filter_session:
                    filter_session.append(int(id))
                else:
                    filter_session.remove(int(id))
            else:
                filter_object_id = filter_object.objects.get(pk=int(id)).id
                filter_session = [filter_object_id]

            request.session[filter_name] = filter_session

        keys = list(FilterMapping.keys())
        if request.session.get(keys[0]):
            if reset:
                del request.session[keys[0]]
            else:
                restaurants = restaurants.filter(filter_foods__id__in=request.session.get(keys[0])).distinct()
        if request.session.get(keys[1]):
            if reset:
                del request.session[keys[1]]
            else:
                restaurants = restaurants.filter(filter_advantages__id__in=request.session.get(keys[1])).distinct()
        if request.session.get(keys[2]):
            if reset:
                del request.session[keys[2]]
            else:
                restaurants = restaurants.filter(tags__id__in=request.session.get(keys[2])).distinct()

        count_restaurants = {"count": restaurants.count()}
        return Response(CountRestaurantWhenUseFilterSerializer(count_restaurants).data)


count_restaurants = CountRestaurantWhenUseFilters.as_view()
