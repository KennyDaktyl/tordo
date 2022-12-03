from django import template

register = template.Library()


@register.filter(name='get_width_from_key')
def get_width_from_key(value):
    return value.split("x")[0]


@register.simple_tag
def get_src_expected(images_data, size):
    images_data = dict(images_data)
    if images_data:
        return images_data.get(size)
    return None
