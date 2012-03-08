from django import template
from menu.models import Menu

register = template.Library()

@register.inclusion_tag('account_register_form.html')
def registerForm():
    return {"registerForm": "" }