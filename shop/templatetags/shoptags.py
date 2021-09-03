from django import template
from translate.models import Translate

register = template.Library()


# All custom template tag go here

@register.simple_tag
def t(key):
    # Your method definition
    return Translate.t(key)
