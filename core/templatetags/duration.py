from django import template

from core.utils import format_length

register = template.Library()

@register.filter
def duration(length):
    return format_length(length)