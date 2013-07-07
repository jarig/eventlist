from django import template
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


@register.filter
def flatten_arrayOfDict(iArray, key):
    res = []
    for el in iArray:
        res.append(el[key])
    return res

@register.filter
def sum_array(iArray):
    result = 0
    for el in iArray:
        result += float(el)
    return result