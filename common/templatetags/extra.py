from django import template
from account import settings
from account.models import _account_logo_name


register = template.Library()
@register.filter
def user_avatar(user):
    if isinstance(user, long):
        return _account_logo_name(user)
    return settings.AVATAR_STUB
