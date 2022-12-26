from web.models.restaurants import FilterFood, FilterAdvantage, Tag


FilterMapping = {
    "filter_foods": FilterFood,
    "filter_advantages": FilterAdvantage,
    "filter_tags": Tag
}


def get_object_list_filtered(request, object_list, reset=False):
    keys = list(FilterMapping.keys())
    if request.session.get(keys[0]):
        if reset:
            del request.session[keys[0]]
        else:
            object_list = object_list.filter(filter_foods__id__in=request.session.get(keys[0])).distinct()
    if request.session.get(keys[1]):
        if reset:
            del request.session[keys[1]]
        else:
            object_list = object_list.filter(filter_advantages__id__in=request.session.get(keys[1])).distinct()
    if request.session.get(keys[2]):
        if reset:
            del request.session[keys[2]]
        else:
            object_list = object_list.filter(tags__id__in=request.session.get(keys[2])).distinct()
    return object_list
