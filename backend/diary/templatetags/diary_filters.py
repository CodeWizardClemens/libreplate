from django import template

register = template.Library()


@register.filter(name="get_item")
def get_item(dictionary, key):
    """
    Safe dictionary lookup for Django templates.

    Usage:
        {{ my_dict|get_item:key }}
    """

    if not dictionary:
        return None

    try:
        return dictionary.get(key)
    except AttributeError:
        # If it's not a dict-like object
        return None
