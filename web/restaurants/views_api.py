from web.restaurants.serializers import CountRestaurantWhenUseFilterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from web.models.restaurants import Restaurant

from .queries import get_object_list_filtered
from web.restaurants.queries import FilterMapping


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

        restaurants = get_object_list_filtered(request, restaurants, reset)

        count_restaurants = {"count": restaurants.count()}
        return Response(CountRestaurantWhenUseFilterSerializer(count_restaurants).data)


count_restaurants = CountRestaurantWhenUseFilters.as_view()
