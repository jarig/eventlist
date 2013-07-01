import urlparse
from account import settings
from django.contrib.auth.models import User
from account.models import Account

from hashlib import md5

class Vkontakte:

    def authenticate(self, identity=None, request=None):
        if identity is None or request is None: return None
        # check cookies
        if not self.validate(request): return None
        try:
            user = Account.objects.get(identity=identity, provider=settings.BACKENDS["VKONTAKTE"]["NAME"])
            return user
        except Account.DoesNotExist:
            raise User.DoesNotExist
    
    def validate(self, request):
        cookie_name = "vk_app_%s" % str(settings.BACKENDS["VKONTAKTE"]["APP_ID"])
        try:
            cookie_data = urlparse.parse_qs(request.COOKIES[cookie_name])
            value = ""
            for i in ('expire', 'mid', 'secret', 'sid'):
                value += "%s=%s" % (i, cookie_data[i][0])

            if cookie_data['sig'][0] == md5(value + settings.BACKENDS["VKONTAKTE"]["SECRET"]).hexdigest():
                self.identity = cookie_data['mid'][0]
                return True
            else:
                raise ValueError()
        except (KeyError, IndexError, AttributeError, ValueError):
            return False
  