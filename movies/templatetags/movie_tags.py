from django import template

register = template.Library()

@register.filter
def star_range(value):
    return range(value)

@register.filter 
def empty_star_range(value):
    return range(5 - value)
