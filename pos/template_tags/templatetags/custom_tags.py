from django import template
import re

from django.urls import reverse

register = template.Library()


@register.simple_tag
def active(request, pattern, active_class):
    url = reverse(pattern)
    if re.search(url, request.path):
        return str(active_class)
    return ''
