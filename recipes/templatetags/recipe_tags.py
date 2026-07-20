from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def get_nested(dictionary, key):
    if not dictionary:
        return {}

    return dictionary.get(key, {})


@register.filter
def get_nutrient(dictionary, nutrient):
    if not dictionary:
        return Decimal("0")

    return dictionary.get(nutrient, Decimal("0"))