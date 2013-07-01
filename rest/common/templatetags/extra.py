from django import template
from django.core.files import storage
from account import settings
from account.models import _account_logo_name


register = template.Library()
@register.filter
def user_avatar(user):
    path = None
    if isinstance(user, long):
        path = _account_logo_name(user)
    if path is None:
        path = settings.AVATAR_STUB
    return path
