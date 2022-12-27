from django import template

register = template.Library()


@register.filter(name="get_width_from_key")
def get_width_from_key(value):
    return value.split("x")[0]


@register.simple_tag
def get_src_expected(images_data, size):
    images_data = dict(images_data)
    if images_data:
        return images_data.get(size)
    return None


@register.simple_tag
def get_thumbnails_by_type(images_data, size, mimetype):
    images_data = dict(images_data)
    if images_data:
        images_data_type = images_data.get(mimetype)
        if images_data_type:
            return images_data_type.get(size)
    return None
